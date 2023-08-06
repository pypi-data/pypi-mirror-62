"""
| ----------------------------------------------------------------------------------------------------------------------
| Date                : August 2018
| Copyright           : (C) 2018 by Ann Crabbé (KU Leuven)
| Email               : ann.crabbe@kuleuven.be
| Acknowledgements    : Translated from VIPER Tools 2.0 (UC Santa Barbara, VIPER Lab).
|                       Dar Roberts, Kerry Halligan, Philip Dennison, Kenneth Dudley, Ben Somers, Ann Crabbé
|
| This program is free software; you can redistribute it and/or modify it under the terms of the GNU
| General Public License as published by the Free Software Foundation; either version 3 of the
| License, or any later version.
| ----------------------------------------------------------------------------------------------------------------------
"""
import copy
import numpy as np
from functools import partial
from multiprocessing import cpu_count, dummy


class Ies:
    """
    Iterative Endmember Selection (IES) based on a square array. IES is used to identify the spectral library
    subset that provides the best class separability. The basis for this is the kappa coefficient. In an iterative
    manner, endmembers are added and removed from the subset until the kappa coefficient no longer improves.

    Citations:

    Schaaf, A.N., Dennison, P.E., Fryer, G.K., Roth, K.L., and Roberts, D.A., 2011, Mapping Plant Functional Types at
    Multiple Spatial Resolutions using Imaging Spectrometer Data, GIScience Remote Sensing, 48, p. 324-344.

    Roth, K.L., Dennison, P.E., and Roberts, D.A., 2012, Comparing endmember selection techniques for accurate mapping
    of plant species and land cover using imaging spectrometer data, Remote Sensing of Environment, 127, p. 139-152.
    """

    def __init__(self):
        self.rmse_band = None
        self.mask = None
        self.original_classes = None
        self.original_classes_multiplied = None
        self.forced_list = None
        self.n_endmembers = None
        self.n_classes = None
        self.multiprocessing = False
        self.summary = {}

    def _confusion_matrix(self, modeled_classes: np.array) -> np.array:
        """
        :param modeled_classes: the classes modeled based on a subset of models
        :return: confusion matrix (= 2D histogram) of the original vs. modeled classes
        """

        # self.original_classes_multiplied is the original classes multiplied by (n_classes +1)
        # by adding the modeled classes, we can create a n_classes^2 separate histogram bins
        confusion_matrix = self.original_classes_multiplied + modeled_classes
        # create a 1D histogram
        confusion_matrix = np.bincount(confusion_matrix, minlength=(self.n_classes + 1) ** 2)
        # reshape to 2D histogram
        return confusion_matrix.reshape([self.n_classes + 1, self.n_classes + 1]).T

    def _kappa(self, confusion_matrix: np.array) -> np.float32:
        """
        :param confusion_matrix: the confusion matrix
        :return: kappa coefficient: a measure of class separability
        """

        theta1 = np.float32(np.trace(confusion_matrix)) / self.n_endmembers
        theta2 = np.float32(np.sum(np.dot(confusion_matrix, confusion_matrix))) / (self.n_endmembers ** 2)
        return np.float32((theta1 - theta2) / (1 - theta2))

    def _add_model(self, current_selection: np.array):
        """ Routine for adding a new model to the selection, if it provides a better kappa than the previous situation
        :param current_selection: current pool of models
        :return: the kappa and index of the newly found model
        """

        n_models = current_selection.shape[0]
        selected_classes = self.original_classes[current_selection]

        # get the current min RMSE and model for each spectrum
        if n_models == 1:
            current_min_rmse = self.rmse_band[current_selection][0]
            current_modeled_classes = np.repeat(selected_classes, self.n_endmembers)
            current_modeled_classes[self.mask[current_selection][0]] = self.n_classes

        else:
            current_min_rmse = np.amin(self.rmse_band[current_selection], axis=0)
            min_index_current = np.argmin(self.rmse_band[current_selection], axis=0)
            min_index_current[np.all(self.mask[current_selection], axis=0)] = -1
            selected_classes = np.append(selected_classes, self.n_classes)
            current_modeled_classes = selected_classes[min_index_current]

        # calculate the kappa array
        if not self.multiprocessing:
            # avoid adding a model that is already in the current pool
            potential_indices = np.arange(self.n_endmembers)
            potential_indices = np.delete(potential_indices, current_selection)

            # try adding each model in an iterative way
            kappa_array = np.zeros(self.n_endmembers, dtype=np.float32)
            for i in potential_indices:
                kappa_array[i] = self._add_model_thread(i, min_rmse=current_min_rmse,
                                                        modeled_classes=current_modeled_classes)
        else:
            # not used for now - has no improvements
            pool = dummy.Pool(cpu_count())
            temp = partial(self._add_model_thread, min_rmse=current_min_rmse, modeled_classes=current_modeled_classes)
            kappa_array = pool.map(temp, np.arange(self.n_endmembers))
            kappa_array = np.array(kappa_array)
            kappa_array[current_selection] = 0

        # return only the model with the best kappa, and its index
        return kappa_array.max(), np.argmax(kappa_array)

    def _add_model_thread(self, i, min_rmse=None, modeled_classes=None):
        # the indices where the new model has a lower RMSE
        new_model_indices = np.where(self.rmse_band[i] < min_rmse)

        # change the current modeled classes where the new model has a better RMSE
        modeled_classes = copy.deepcopy(modeled_classes)
        modeled_classes[new_model_indices] = self.original_classes[i]

        confusion_matrix = self._confusion_matrix(modeled_classes)
        return self._kappa(confusion_matrix)

    def _remove_model(self, current_selection: np.array):
        """ Routine for removing a model from a selection, if it provides a better kappa than the previous situation
        :param current_selection: current pool of models
        :return: the kappa and index of the model to remove
        """

        n_models = current_selection.shape[0]
        # create these before the loop to save some time
        mask = np.ones(n_models, dtype=bool)
        current_rmse = self.rmse_band[current_selection]
        current_mask = self.mask[current_selection]
        current_classes = self.original_classes[current_selection]

        # calculate the kappa array
        if not self.multiprocessing:
            # try adding each model in an iterative way
            kappa_array = np.zeros(n_models, dtype=np.float32)
            for i in np.arange(n_models):
                kappa_array[i] = self._remove_model_thread(i, ones=mask, mask=current_mask, rmse=current_rmse,
                                                           classes=current_classes)
        else:
            pool = dummy.Pool(cpu_count())
            temp = partial(self._remove_model_thread, ones=mask, mask=current_mask, rmse=current_rmse,
                           classes=current_classes)
            kappa_array = pool.map(temp, np.arange(n_models))
            kappa_array = np.array(kappa_array)

        # no subtracting forced models
        kappa_array[np.where(np.in1d(current_selection, self.forced_list))] = 0

        # return only the model with the best kappa, and its index
        return kappa_array.max(), np.argmax(kappa_array)

    def _remove_model_thread(self, i, ones=None, mask=None, rmse=None, classes=None):
        # find the modeled classes after removing one model
        ones = copy.deepcopy(ones)
        ones[i] = False
        min_index_removed = np.argmin(rmse[ones], axis=0)
        min_index_removed[np.all(mask[ones], axis=0)] = -1
        classes_removed = np.append(classes[ones], self.n_classes)
        modeled_classes_removed = classes_removed[min_index_removed]

        # confusion matrix and kappa
        confusion_matrix = self._confusion_matrix(modeled_classes_removed)
        return self._kappa(confusion_matrix)

    def _evaluate_selection(self, selection: np.array):
        """ Routine for evaluating the kappa and confusion matrix of a given selection of models
        :param selection: current pool of models
        :return: the kappa and confusion matrix for this selection
        """

        n_models = selection.shape[0]
        selected_classes = self.original_classes[selection]

        # get the current min RMSE and model for each spectrum
        if n_models == 1:
            current_modeled_classes = np.repeat(selected_classes, self.n_endmembers)
            current_modeled_classes[self.mask[selection][0]] = self.n_classes

        else:
            min_index_current = np.argmin(self.rmse_band[selection], axis=0)
            min_index_current[np.all(self.mask[selection], axis=0)] = -1
            selected_classes = np.append(selected_classes, self.n_classes)
            current_modeled_classes = selected_classes[min_index_current]

        confusion_matrix = self._confusion_matrix(current_modeled_classes)
        kappa = self._kappa(confusion_matrix)

        # return the kappa and confusion matrix the model with the best kappa, and its index
        return kappa, confusion_matrix

    def execute(self, rmse_band: np.array, class_list: np.array, constraints_band: np.array,
                forced_list: np.array = None,
                forced_location: int = None, multiprocessing: bool = False, summary: bool = False, p=None):
        """
        Execute the IES algorithm. The result is a 1-D numpy array of selected endmembers. In case a summary is
        requested, it is delivered as a second output variable.

        :param rmse_band: RMSE band from the square array
        :param class_list: int array with the *numerical* class for each spectrum (e.g. GV = 1, SOIL = 2)
        :param constraints_band: constraints band from the square array
        :param forced_list: int array with indices of the endmembers that should be forcefully included
        :param forced_location: the loop in which the forced_list should be included (starting from 0)
        :param multiprocessing: use multiprocessing or not
        :param summary: return a summary of the process or not
        :param QProgressBar p: a reference to the GUI progress bar
        :return: numpy array with the indices of the selected endmembers [+ summary as a dict in case requested]
        """

        # give useful messages to the user
        print('IES calculations started')
        if p is None:
            p = _ProgressBar(0)
        else:
            p.setValue(0)

        # store the variables
        self.original_classes = class_list
        self.n_endmembers = self.original_classes.shape[0]
        self.n_classes = self.original_classes.max() + 1
        self.original_classes_multiplied = class_list * (self.n_classes + 1)  # for later use in the confusion matrix
        self.mask = constraints_band > 0
        self.rmse_band = rmse_band
        self.rmse_band[self.mask] = 9999

        self.forced_list = forced_list
        self.multiprocessing = multiprocessing

        stop_adding = 0
        stop_removing = 0

        # find the first endmember: the modeled class with 1 model is always the model itself, except constraint breach,
        # unless we have to use the forced library right away
        if forced_location == 0:
            selected_indices = forced_list
            max_kappa, confusion_matrix = self._evaluate_selection(selected_indices)
            print("0: forced library entered: " + np.array2string(forced_list, separator=", ") +
                  " - Kappa at this point: " + str(max_kappa))
            p.setValue(p.value() + 1)
            if summary:
                self.summary[0] = {'add': forced_list, 'kappa': max_kappa, 'confusion_matrix': confusion_matrix}
        else:
            modeled_classes_one_model = np.repeat(self.original_classes, self.n_endmembers).reshape((self.n_endmembers,
                                                                                                     self.n_endmembers))
            modeled_classes_one_model[self.mask] = self.n_classes

            kappa_array = np.zeros(self.n_endmembers, dtype=np.float32)
            for i in np.arange(self.n_endmembers):
                confusion_matrix = self._confusion_matrix(modeled_classes_one_model[i])
                kappa_array[i] = self._kappa(confusion_matrix)

            max_kappa = kappa_array.max()
            new_index = np.argmax(kappa_array)
            selected_indices = np.array([new_index])
            print("0: new endmember: " + str(new_index) + " - Kappa at this point: " + str(max_kappa))
            p.setValue(p.value() + 1)
            if summary:
                self.summary[0] = {'add': new_index, 'kappa': max_kappa,
                                   'confusion_matrix': self._confusion_matrix(modeled_classes_one_model[new_index])}

        # find the second endmember, unless we have to use the forced library in this step or unless we already have 2
        if forced_location == 1:
            selected_indices = np.sort(np.append(selected_indices, forced_list))
            max_kappa, confusion_matrix = self._evaluate_selection(selected_indices)
            print("1: forced library entered: " + np.array2string(forced_list, separator=", ") +
                  " - Kappa at this point: " + str(max_kappa))
            p.setValue(p.value() + 1)
            if summary:
                self.summary[1] = {'add': forced_list, 'kappa': max_kappa, 'confusion_matrix': confusion_matrix}
        elif selected_indices.shape[0] < 2:
            new_kappa, new_index = self._add_model(selected_indices)

            if new_kappa > max_kappa:
                max_kappa = new_kappa
                selected_indices = np.sort(np.append(selected_indices, new_index))
                print("1: new endmember: " + str(new_index) + " - Kappa at this point: " + str(max_kappa))
                p.setValue(p.value() + 1)
                if summary:
                    self.summary[1] = {'add': new_index, 'kappa': max_kappa,
                                       'confusion_matrix': self._evaluate_selection(selected_indices)[1]}
            else:
                print("No second endmember found. Returning without result.")
                p.setValue(p.value() + 1)
                return None
        else:
            print("1: second loop skipped because forced library contained more than one endmember")
            p.setValue(p.value() + 1)
            if summary:
                self.summary[1] = {'add': None}

        # IES loop
        loop_counter = 2
        while stop_adding == 0 or stop_removing == 0:

            if loop_counter == 100:
                pass

            if forced_location == loop_counter:
                selected_indices = np.sort(np.append(selected_indices, forced_list))
                max_kappa, confusion_matrix = self._evaluate_selection(selected_indices)
                print(str(loop_counter) + ": forced library entered: " + np.array2string(forced_list, separator=", ") +
                      " - Kappa at this point: " + str(max_kappa))
                p.setValue(p.value() + 1 if p.value() < 99 else 0)
                if summary:
                    self.summary[loop_counter] = {'add': forced_list, 'kappa': max_kappa,
                                                  'confusion_matrix': confusion_matrix}
            else:
                # process of adding a new model
                new_kappa, new_index = self._add_model(selected_indices)

                if new_kappa > max_kappa:
                    max_kappa = new_kappa
                    selected_indices = np.sort(np.append(selected_indices, new_index))
                    print(str(loop_counter) + ": new endmember: " + str(new_index) +
                          " - Kappa at this point: " + str(max_kappa))
                    p.setValue(p.value() + 1 if p.value() < 99 else 0)
                    stop_adding = 0
                    if summary:
                        self.summary[loop_counter] = {'add': new_index, 'kappa': max_kappa,
                                                      'confusion_matrix': self._evaluate_selection(selected_indices)[1]}
                else:
                    stop_adding = 1

                # process of subtracting a selected model
                new_kappa, remove_index = self._remove_model(selected_indices)

                if new_kappa > max_kappa:
                    max_kappa = new_kappa
                    print(str(loop_counter) + ": removed endmember: " + str(selected_indices[remove_index]) +
                          " - Kappa at this point: " + str(max_kappa))
                    p.setValue(p.value() + 1 if p.value() < 99 else 0)
                    selected_indices = np.delete(selected_indices, remove_index)
                    stop_removing = 0
                    if summary:
                        self.summary[loop_counter] = {'remove': selected_indices[remove_index], 'r_kappa': max_kappa,
                                                      'r_confusion_matrix':
                                                          self._evaluate_selection(selected_indices)[1]}

                else:
                    stop_removing = 1

            loop_counter += 1
        if summary:
            return selected_indices, self.summary
        else:
            return selected_indices


class _ProgressBar:

    def __init__(self, initial_value: int = 0):
        self._value = initial_value

    def value(self):
        return self._value

    @staticmethod
    def setValue(value: int):
        """ Replacement for real progress bar: print """
        print('{}%..'.format(value), end='')


""" MODIFICATION HISTORY:
2009 08 [IDL]: Written by Philip Dennison, University of Utah, revised by Keely Roth & Seth Peterson, UCSB
2012 08 [IDL]: Modified by Philip Dennison: change selection method for initial endmember (kappa maximization instead
               of comparing all pairs)
2012 09 [IDL]: Modified by Philip Dennison: accommodate a spectral library containing forced endmembers
2013 11 [IDL]: Modified by Philip Dennison: improve run time (still has bug)
2014 03 [IDL]: Modified by Ann Crabbé: Restructured v5 + v6 to incorporate in VIPER II tool, based on a GUI,
               fixed previous bug, data input via GUI instead of via control file, bug fix (step_num and loop_counter),
               lay-out of summary file was altered for readability, add-loop only allow endmembers not yet in the
               selection to be added, remove-loop don't remove endmembers from forced library,
2014 02 [IDL]: Modified by Austin Coates: added threading
2014 09 [IDL]: Modified by Kenneth Dudley: computational improvements to add and subtract loops greatly reducing runtime
               (threaded/non), added threading to IES GUI, more robust error checking for square array and input
               libraries, status window to IES process, added setup summary to output summary file, changed layout of
               summary file such that confusion matrices are aligned properly, added column/row labels to certain
               confusion matrix outputs in summary file
2014 11 [IDL]: Modified by Kenneth Dudley: changed IES subtract process to subtract out models whose removal does not
               decrease kappa. Previously models would only be removed if, by removing it, kappa improved. This gets rid
               of very similar models which may build up over the course of IES.
2015 08 [IDL]: Modified by Kenneth Dudley: fixed several issues with rmse array copying which caused several variables
               to hold repeat data and needlessly exacerbate memory usage. This should reduce memory consumption by 1/3
               when using threading + when exporting metadata the operation "print, b, string(newMetadata, /print)"
               would occasionally print the second row of metadata on the first line instead of a hard break. Resulting
               in a mismatch between .sli and metadata. + fixed issue with wrong spectrum name output to summary file
               when an endmember was subtracted. This also solved a program error, if the index of the spectrum name
               fell out of bounds. + changed location of some SetVar invariant variables to reduce overall number of
               calls and speed up threading (minor)
2018-03 [Python] Ported to QGIS/Python by Ann Crabbé, incl. significant re-write of code
"""
