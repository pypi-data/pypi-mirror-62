About The Spectral Library Tool
===============================

The Spectral Library Tool software package is both a QGIS plugin and stand-alone python package that provides a suite of
processing tools for multi- and hyperspectral spectral libraries.

The software is based on VIPER Tools: code written for ENVI/IDL and released in 2007.
Several updates have been released since and now it has been ported to PyQGIS in the period 2017 - 2020.
The original VIPER Tools is now split over two python/QGIS tools: Spectral Library Tools and MESMA.

**Spectral Library Tool** provides the following:
 - Creating spectral libraries interactively (selecting spectra from an image or using regions of interest) and managing
   the metadata (developed by HU Berlin)
 - Optimizing spectral libraries with Iterative Endmember Selection, Ear-Masa-Cob or CRES
 - Website: https://spectral-libraries.readthedocs.io
 - Repository: https://bitbucket.org/kul-reseco/spectral-libraries

**MESMA** provides the following:
 - Running SMA and MESMA (with multi-level fusion, stable zone unmixing, ...)
 - Post-processing of the MESMA results (visualisation tool, shade normalisation, ...)
 - Website: https://mesma.readthedocs.io
 - Repository: https://bitbucket.org/kul-reseco/mesma

The software has now been developed in the open source environment to encourage further development of the tool.

Referencing The Spectral Library Tool
=====================================

When using The Spectral Library Tool, please use the following citation:

Crabbé, A. H., Jakimow, B., Somers, B., Roberts, D. A., Halligan, K., Dennison, P., Dudley, K. (2019).
Spectral Library QGIS Plugin (Version x) [Software]. Available from https://bitbucket.org/kul-reseco/spectral-libraries.

Acknowledgements
================

The software and user guide are based on VIPER Tools 2.0 (UC Santa Barbara, VIPER Lab):
Roberts, D. A., Halligan, K., Dennison, P., Dudley, K., Somers, B., Crabbe, A., 2018, Viper Tools User Manual,
Version 2, 91 pp.

MESMA also makes use of the QGISPluginSupport python packages developed by Benjamin Jakimow  (Benjamin Jakimow,
HU Berlin): https://bitbucket.org/jakimowb/qgispluginsupport

This revision is funded primarily through BELSPO (the Belgian Science Policy Office) in the framework
of the STEREO III Programme – Project LUMOS - SR/01/321.

Logo's were created for free at https://logomakr.com.

Software Licence
================

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General
Public License as published by the Free Software Foundation; either version 3 of the License, or any later version.

What is new in the MESMA tool 1.0?
==================================

Differences between Viper Tools 2.0 and the MESMA tool 1.0:
 - The migration to PyQGIS is not just a translation from IDL to Python, but also a serious re-write of the code and a
   revision of the GUI to match the look and feel of other QGIS tools.
 - The output of the MESMA tools has been optimized, breaking backwards compatibility with the IDL tools.
 - A tool for visualisation of the MESMA results has been introduced. A first draft of this tool had been proposed for
   Viper 2.0, however this was not yet user-friendly and therefore later removed again. The visualisation tool included
   in this version is a revision of the former tool, with a focus on user friendliness and GIS.
 - The post-processing tool for integration with DEM has been removed.
 - Extra post-processing tool: Soft to Hard Classification (transforms the fractions image into a classification image)

