from qgis.core import *
import sys

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

from qgis.PyQt.QtCore import QVariant
# create layer
vl = QgsVectorLayer("Polygon", "poly", "memory")
pr = vl.dataProvider()

# add fields
pr.addAttributes([QgsField("name", QVariant.String),
                    QgsField("age",  QVariant.Int),
                    QgsField("size", QVariant.Double)])
vl.updateFields() # tell the vector layer to fetch changes from the provider

# add a feature
fet = QgsFeature()
points = [QgsPointXY(50,50),QgsPointXY(50,150),QgsPointXY(100,150),QgsPointXY(100,50)]
fet.setGeometry(QgsGeometry.fromPolygonXY([points]))
fet.setAttributes(["Johny", 2, 0.3])
pr.addFeatures([fet])

# update layer's extent when new features have been added
# because change of extent in provider is not propagated to the layer
vl.updateExtents()
QgsProject.instance().addMapLayers([vl])

print('\n'.join(map(str, [alg.id() for alg in QgsApplication.processingRegistry().algorithms()])))


processing.algorithmHelp("native:selectbylocation")
ats=processing.run("native:selectbylocation",
               {'INPUT':vl,
                'PREDICATE':[0],
                'INTERSECT':vl,
                'METHOD':0})

vl1=ats['OUTPUT']

features = vl1.getFeatures()
#exporting features
exporter = QgsJsonExporter()
print("features",exporter.exportFeature(vl1.getFeature(0)))

print(exporter.exportFeatures(features))
for fet in features:
    print("F:", fet.id(), fet.attributes(), fet.geometry().asPolygon())
    print(fet.geometry())

print("fields:", len(pr.fields()))
print("features:", pr.featureCount())
e = vl.extent()
print("extent:", e.xMinimum(), e.yMinimum(), e.xMaximum(), e.yMaximum())

# iterate over features
features = vl.getFeatures()
for fet in features:
    print("F:", fet.id(), fet.attributes(), fet.geometry().asPolygon())

# Finally, exitQgis() is called to remove the
# provider and layer registries from memory

qgs.exitQgis()