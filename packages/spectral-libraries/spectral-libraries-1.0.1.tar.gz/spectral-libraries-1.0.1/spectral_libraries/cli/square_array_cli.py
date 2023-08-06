"""
| ----------------------------------------------------------------------------------------------------------------------
| Square Array Command Line Interface. Available when installing viper with pip. Type 'viper-square -h' for help.
|
| Date                : July 2018
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
import argparse
import numpy as np
import time
from vipertools.scripts.square_array import SquareArray
from vipertools.io import imports, exports


def create_parser():
    """ The parser for the CLI command parameters. """
    parser = argparse.ArgumentParser(description=str(SquareArray.__doc__))

    # library
    parser.add_argument('library', metavar='input', help='spectral library file')
    parser.add_argument('--reflectance-scale', metavar='\b', type=int,
                        help='reflectance scale factor (default: derived from data as 1, 1 000 or 10 000)')

    # constraints
    parser.add_argument('--min-fraction', metavar='\b', type=float, default=-0.05,
                        help='minimum allowable fraction (default -0.05), use -9999 for no constraint')
    parser.add_argument('--max-fraction', metavar='\b', type=float, default=1.05,
                        help='maximum allowable fraction (default 1.05), use -9999 for no constraint')
    parser.add_argument('--max-rmse', metavar='\b', type=float, default=0.025,
                        help='maximum allowable RMSE (default 0.025), use -9999 for no constraint')
    parser.add_argument('-u', '--unconstrained', action='store_true', default=False,
                        help='create a square array without constraints')
    parser.add_argument('-r', '--reset-off', action='store_true', default=False,
                        help='do not reset fractions to the min/max when they surpass them, RMSE is then calculated '
                             'with these corrected values (ignored when no constraints are set) (default on)')

    # output
    parser.add_argument('-o', '--output', metavar='\b',
                        help="output ENVI file with square array (default: in same folder with extension '_sq.sqr'")

    # bands
    parser.add_argument('--exclude-rmse', action='store_true', default=False,
                        help='exclude rmse band (default: included)')
    parser.add_argument('--exclude-constraints', action='store_true', default=False,
                        help='exclude constraints band (default: included, ignored no constraints are set)')
    parser.add_argument('--include-fractions', action='store_true', default=False,
                        help='include fractions band (default: excluded)')
    parser.add_argument('--include-shade', action='store_true', default=False,
                        help='include shade band (default: excluded)')
    parser.add_argument('--include-angle', action='store_true', default=False,
                        help='include spectral angle band (default: excluded)')

    return parser


def run_square_array(args):
    """
    Documentation: viper-square -h
    """

    spectral_library = imports.import_library(args.library)

    if spectral_library is None or spectral_library.featureCount() == 0:
        return

    library = np.asarray([x.values()['y'] for x in spectral_library.profiles()]).T
    spectra_names = [x.name().strip() for x in spectral_library.profiles()]

    # divide the library by the reflectance scale
    if args.reflectance_scale:
        library = library / args.reflectance_scale
    else:
        scale = imports.detect_reflectance_scale_factor(library)
        library = library / scale
        print('Reflectance scale factor: ' + str(scale))

    # get the constraints
    if args.unconstrained:
        constraints = (-9999, -9999, -9999)
    else:
        constraints = (args.min_fraction, args.max_fraction, args.max_rmse)

    use_reset = not args.reset_off

    # output preferences
    out_rmse = not args.exclude_rmse
    if sum(constraints) == -29997:
        out_constraints = False
    else:
        out_constraints = not args.exclude_constraints
    out_angle = args.include_angle
    out_fractions = args.include_fractions
    out_shade = args.include_shade

    # Run square_array.py
    start = time.time()
    square_array = SquareArray().execute(library=library, constraints=constraints, reset=use_reset, out_rmse=out_rmse,
                                         out_constraints=out_constraints, out_fractions=out_fractions,
                                         out_shade=out_shade, out_angle=out_angle)
    duration = np.float16(time.time() - start)

    # output name
    if args.output:
        output_file = args.output
    else:
        path_no_extension = os.path.splitext(args.library)[0]
        output_file = path_no_extension + '_sq.sqr'

    exports.save_square_to_envi(square_array=square_array, outfile_path=output_file, spectra_names=spectra_names,
                                library_name=os.path.basename(args.library), constraints=constraints, reset=use_reset,
                                duration=duration, ngb=library.shape[0])


def main():
    """ Function called by CLI. """
    parser = create_parser()
    run_square_array(parser.parse_args())


if __name__ == '__main__':
    main()
