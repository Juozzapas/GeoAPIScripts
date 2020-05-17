@ECHO off

set OSGEO4W_ROOT=C:\OSGeo4W64

call "%OSGEO4W_ROOT%\bin\o4w_env.bat"
call "%OSGEO4W_ROOT%\bin\qt5_env.bat"

path %OSGEO4W_ROOT%\apps\qgis\bin;%PATH%


set PYTHONPATH=C:\Users\Username\PycharmProjects\Praktika

set PYTHONPATH=%PYTHONPATH%;%OSGEO4W_ROOT%\apps\qgis\python

set QGIS_PREFIX_PATH=%OSGEO4W_ROOT%\apps\qgis

start "PyCharm Aware QGIS" /B "C:\OSGeo4W64\apps\Python37\python.exe" %*