from qgis.core import Qgsproject, QgsMapLayer, QgsFeature
from qgis.utils import iface


def layerExists(layerName, typeName):
    layers = QgsProject.instance().mapLayersByName(layerName)
    if len(layers) == 0:
        return False

    if typeName.lower() == 'raster':
        layerType = QgsMapLayer.RasterLayer
    elif typeName.lower() == 'vector':
        layerType = QgsMapLayer.VectorLayer

    for l in layers:
        if l.name().lower() == layerName.lower() and l.type() == layerType:
            return True

    return False


def addFeature():
    layer = iface.activeLayer()
    provider = layer.dataProvider()
    f = QgsFeature()
    f.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(8.6866, 45.7940)))
    provider.addFeature(f)
    l.commitChanges()
    l.updateExtents()
    return True


def checkFeatureCount(count):
    layer = iface.activeLayer()
    return layer.featureCount() == int(count)