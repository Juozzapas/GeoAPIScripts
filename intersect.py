from qgis.core import *
import sys
import json

# Supply path to qgis install location
QgsApplication.setPrefixPath('C:/OSGEO4W1/apps/qgis', True)

# Create a reference to the QgsApplication.  Setting the
# second argument to False disables the GUI.
qgs = QgsApplication([], False)

# Load providers
qgs.initQgis()
sys.path.append('C:\\OSGeo4W64\\apps\\qgis\\python\\plugins')
from qgis.analysis import QgsNativeAlgorithms
import processing
from processing.core.Processing import Processing

Processing.initialize()
QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())


# Write your code here to load some layers, use processing
# algorithms, etc.

def execute():
    if len(sys.argv) == 3:
        ats = runProcessingNativeIntersect(sys.argv[1], sys.argv[2])
        vl1 = ats['OUTPUT']
        print(sys.argv[2])
        features = vl1.getFeatures()
        exporter = QgsJsonExporter()
        print("GEOJSON", exporter.exportFeatures(features))
    else:
        print("wrong parameters", len(sys.argv))


def runProcessingNativeIntersect(inputLayer, overlayLayer):
    processing.algorithmHelp("native:intersection")
    return processing.run("native:intersection",
                          {'INPUT': inputLayer,
                           'OVERLAY': overlayLayer,
                           'INPUT_FIELDS': [],
                           'OVERLAY_FIELDS': [],
                           'OVERLAY_FIELDS_PREFIX': '',
                           'OUTPUT': 'TEMPORARY_OUTPUT'})


execute()

# Finally, exitQgis() is called to remove the
# provider and layer registries from memory

qgs.exitQgis()
