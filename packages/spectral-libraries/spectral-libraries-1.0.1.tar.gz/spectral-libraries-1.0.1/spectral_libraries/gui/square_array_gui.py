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
import os
import sys
import time
import numpy as np
from qgis.gui import QgsFileWidget
from qgis.utils import iface
from qgis.PyQt.uic import loadUi
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QDialog, QDialogButtonBox
from vipertools.io.imports import import_library, detect_reflectance_scale_factor
from vipertools.io.exports import save_square_to_envi, EmittingStream
from vipertools.gui.logo_gui import LogoWidget
from vipertools.scripts.square_array import SquareArray


class SquareArrayWidget(QDialog):
    """ QDialog to interactively set up the Square Array input and output. """

    def __init__(self):
        super(SquareArrayWidget, self).__init__()
        loadUi(os.path.join(os.path.dirname(__file__), 'square_array.ui'), self)
        sys.stdout = EmittingStream(self.tabWidget)
        sys.stderr = EmittingStream(self.tabWidget)

        # Logo
        self.logoLayout.addWidget(LogoWidget(parent=self.logoWidget))

        # Library
        self.browseLibrary.lineEdit().setReadOnly(True)
        self.browseLibrary.fileChanged.connect(self._library_browse)

        # Constraints
        self.constraintsGroup.clicked.connect(self._main_constraints_clicked)
        self.minFracCheck.clicked.connect(self._sub_constraints_clicked)
        self.maxFracCheck.clicked.connect(self._sub_constraints_clicked)
        self.maxRMSECheck.clicked.connect(self._sub_constraints_clicked)

        # Output
        self.browseOut.lineEdit().setReadOnly(True)
        self.browseOut.lineEdit().setPlaceholderText('The SquareArray file (.sqr) ...')
        self.browseOut.setStorageMode(QgsFileWidget.SaveFile)

        # Open in QGIS?
        try:
            iface.activeLayer
        except AttributeError:
            self.openInQGIS.setChecked(False)
            self.openInQGIS.setDisabled(True)

        # Run or Cancel
        self.OKClose.button(QDialogButtonBox.Ok).setText("Run")
        self.OKClose.accepted.connect(self._run_square_array)
        self.OKClose.rejected.connect(self.close)

        # SquareArrayWidget variables
        self.library = None
        self.spectra_names = None

    def __del__(self):
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    def _library_browse(self, path):
        """ When the users browses for a library, set the reflectance scale factor and output file automatically.
        :param path: the absolute path to the Spectral Library
        """

        if path == '':
            return

        try:
            spectral_library = import_library(path)
        except Exception as e:
            print(str(e), file=sys.stderr)
            self.browseLibrary.setFilePath('')
            return

        self.library = np.asarray([x.values()['y'] for x in spectral_library.profiles()]).T
        self.spectra_names = [x.name().strip() for x in spectral_library.profiles()]

        # set the library reflectance scale factor
        self.libraryScaleValue.setValue(detect_reflectance_scale_factor(self.library))

        # set default output name
        path_no_extension = os.path.splitext(path)[0]
        self.browseOut.lineEdit().setText(path_no_extension + '_sq.sqr')

    def _main_constraints_clicked(self, checked):
        """ Disable the constraints band when no constraints are chosen in general.
        :param checked: state of the checkbox
        """
        if checked is False:
            self.outConstrCheck.setCheckState(Qt.Unchecked)
            self.outConstrCheck.setEnabled(False)
        else:
            self.outConstrCheck.setEnabled(True)

    def _sub_constraints_clicked(self):
        """ Disable the constraints band and reset option when all individual constraints are checked off. """

        min_frac = self.minFracCheck.isChecked()
        max_frac = self.maxFracCheck.isChecked()
        max_rmse = self.maxRMSECheck.isChecked()

        if not min_frac and not max_frac and not max_rmse:
            self.outConstrCheck.setCheckState(Qt.Unchecked)
            self.outConstrCheck.setEnabled(False)
            self.resetCheck.setEnabled(False)
        else:
            self.outConstrCheck.setEnabled(True)
            self.resetCheck.setEnabled(True)

    def _run_square_array(self):
        """ Read all parameters and pass them on to the SquareArray class. """

        # Check that a library is given
        if self.library is None:
            print('Choose a spectral library.', file=sys.stderr)
            return

        # Read the constraints
        constraints = [-9999, -9999, -9999]
        if self.constraintsGroup.isChecked():
            if self.minFracCheck.isChecked():
                constraints[0] = self.minFracValue.value()
            if self.maxFracCheck.isChecked():
                constraints[1] = self.maxFracValue.value()
            if self.maxRMSECheck.isChecked():
                constraints[2] = self.maxRMSEValue.value()
        constraints = tuple(constraints)
        use_reset = self.resetCheck.isChecked()

        # Get output preferences
        out_rmse = self.outRmseCheck.isChecked()
        out_constraints = self.outConstrCheck.isChecked()
        out_angle = self.outAngleCheck.isChecked()
        out_fractions = self.outFracCheck.isChecked()
        out_shade = self.outShadeCheck.isChecked()
        if not out_rmse and not out_constraints and not out_angle and not out_fractions and not out_shade:
            print('At least one output band must be selected.', file=sys.stderr)
            return

        # Run square_array.py
        start = time.time()
        square_array = SquareArray().execute(library=self.library/self.libraryScaleValue.value(), reset=use_reset,
                                             constraints=constraints, out_rmse=out_rmse, out_fractions=out_fractions,
                                             out_constraints=out_constraints, out_shade=out_shade, out_angle=out_angle,
                                             p=self.progressBar)
        duration = np.float16(time.time() - start)
        print('Process finished in ' + str(duration) + ' seconds')

        print("Writing to disk...")
        save_square_to_envi(square_array=square_array, outfile_path=self.browseOut.filePath(), duration=duration,
                            spectra_names=self.spectra_names, constraints=constraints, reset=use_reset,
                            library_name=os.path.basename(self.browseLibrary.filePath()), ngb=self.library.shape[0])
        print("Done.")
        if self.openInQGIS.isChecked():
            iface.addRasterLayer(self.browseOut.filePath(), "Square Array")


def _run():
    from qgis.core import QgsApplication
    app = QgsApplication([], True)
    app.initQgis()

    z = SquareArrayWidget()
    z.show()

    app.exec_()


if __name__ == '__main__':
    _run()
