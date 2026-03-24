#!/usr/bin/python
# -*- coding: utf-8 -*-

# Authors: Krzysztof Czarnecki, Szymon Niemiec, Marek Kulawiak
# Gdansk University of Technology,
# Faculty of Electronics, Telecommunications and Informatics, Department of Geoinformatics)

# This script provides an introduction to the automation of operations performed within the QGIS application.
# NOTE! Tasks to be carried out are listed at the end of the script.

# In orded to begin, you should run the QGIS application and enter the Python Console.
# The console can be found in the Plugins section.

# Then import the sys module with the following command:
# import sys
# and check the paths provided by the sys.path variable, e.g. like this:
# print(sys.path)

# In order to use this script, it must be either copied to one of the locations indicated by the sys.path variable,
# or its location must be added to this variable in the following manner:
# sys.path.append("path/to/directory/containing/this/script").
# Alternatively, you can also create a symbolic link in the operating system.
# In Linux-based systems, this can be done with the use of the system shell:
#   mkdir -p /home/sznie/.local/share/QGIS/QGIS3/profiles/default/python/
#   ln -s  ~/Dydaktyka/PyQGIS/geoi.py ~/.local/share/QGIS/QGIS3/profiles/default/python/geoi.py

# From this moment, it is possible to import the geoi module with the following line:
# import geoi


# Each function defined in this file can be called from the console like this:
# geoi.function_name(), e.g. geoi.hello()

# Each time the script is modified, it must be re-imported by using the built-in reload() function.
# In order to use it, first the importlib must be loaded:
# import importlib
# Then the function can be called in the following way:
# importlib.reload(geoi)


# A simple function used to test this module.
def hello():
    print("Hello! This is test lab module!")


# The following entry will cause the hello() function to run when the module is loaded:
hello()

# The following variable should point to the directory with data files:
import os

path = os.path.dirname(__file__) + "/data/"

# The following is used to import required modules:
import sys, qgis


# Helper function used for printing error messages on the screen.
def error(info):
    sys.stderr.write("Error: " + info)


# Function for setting layer data source encoding:
def fixEncoding(vlayer, encoding="UTF-8"):
    vlayer.setProviderEncoding(encoding)
    vlayer.dataProvider().setEncoding(encoding)


# Function used for reading a vector layer with the map of Poland.
def polska():
    # path to the .shp file (can be different depending on the file system):
    filepath = path + "POL_adm0.shp"
    print("Reading layer from file:", filepath)

    # read the layer and store its contents in the vlayer variable:
    vlayer = qgis.core.QgsVectorLayer(filepath, "Polska", "ogr")

    # validate the layer:
    if not vlayer.isValid():
        error("Layer failed to load!")

    # register the layer in the interface (it will be displayed automatically):
    qgis.core.QgsProject.instance().addMapLayer(vlayer)

    # return an object representing the layer:
    return vlayer
    # Depending on how the module was loaded, the above object can be obtained either like this:
    #    l = poland()
    # or like this:
    #    l = geoi.poland()


# Function used for reading a map of Poland divided into voivodeships.
def regions():
    filepath = path + "POL_adm1.shp"

    # please note how text containing unicode characters should be handled:
    vlayer = qgis.core.QgsVectorLayer(filepath, "Województwa", "ogr")
    if not vlayer.isValid():
        error("Layer failed to load!")
    fixEncoding(vlayer)
    qgis.core.QgsProject.instance().addMapLayer(vlayer)
    return vlayer


# Function used for removing a loaded layer from QGIS interface.
def remove(layer):
    # obtain layer ID:
    layer_id = layer.id()

    # remove the layer:
    qgis.core.QgsProject.instance().removeMapLayer(layer_id)

    # refresh the interface:
    qgis.utils.iface.mapCanvas().refresh()


# Function used for removing all loaded layers from QGIS interface.
def clear():
    # iterate over all layers:
    for item in qgis.core.QgsProject.instance().mapLayers().items():
        layer_id = item[1].id()
        qgis.core.QgsProject.instance().removeMapLayer(layer_id)

    qgis.utils.iface.mapCanvas().refresh()


# Function used for setting layer transparency, with the default value set to 0.5.
def setTransparency(layer, tval=0.5):
    # transparency can be of any value from 0 to 1:
    if tval < 0.0:
        tval = 0
    if tval > 1.0:
        tval = 1

    tval = 1.0 - tval

    myRenderer = layer.renderer()
    mySymbol = myRenderer.symbol()
    mySymbol.setOpacity(tval)

    qgis.utils.iface.mapCanvas().refreshAllLayers()


# Import required QT modules:
from qgis.PyQt import QtGui as qtg
from qgis.PyQt import QtCore as qtc

# Palette of visually distinct colours used for categorized rendering.
_PALETTE = [
    (166, 206, 227),
    (31, 120, 180),
    (178, 223, 138),
    (51, 160, 44),
    (251, 154, 153),
    (227, 26, 28),
    (253, 191, 111),
    (255, 127, 0),
    (202, 178, 214),
    (106, 61, 154),
    (255, 255, 153),
    (177, 89, 40),
    (141, 211, 199),
    (255, 255, 179),
    (190, 186, 218),
    (251, 128, 114),
]


# Function that applies a different fill colour to each feature of a vector
# layer using a categorized symbol renderer keyed on the given field name.
def setCategorizedColors(vlayer, field_name="NAME_1", opacity=1.0):
    categories = []
    features = list(vlayer.getFeatures())

    for i, feat in enumerate(features):
        value = feat[field_name]
        r, g, b = _PALETTE[i % len(_PALETTE)]

        symbol = qgis.core.QgsSymbol.defaultSymbol(vlayer.geometryType())
        symbol.setColor(qtg.QColor(r, g, b))
        symbol.setOpacity(opacity)

        category = qgis.core.QgsRendererCategory(value, symbol, str(value))
        categories.append(category)

    renderer = qgis.core.QgsCategorizedSymbolRenderer(field_name, categories)
    vlayer.setRenderer(renderer)
    vlayer.triggerRepaint()
    qgis.utils.iface.layerTreeView().refreshLayerSymbology(vlayer.id())


# Function used for setting layer color.
# r - red, g - green, b - blue (integer values in range 0-255)
def setColor(layer, r=0, g=0, b=0):
    r = max(0, min(255, int(r)))
    g = max(0, min(255, int(g)))
    b = max(0, min(255, int(b)))

    myRenderer = layer.renderer()
    mySymbol = myRenderer.symbol()

    mySymbol.setColor(qtg.QColor(r, g, b))

    qgis.utils.iface.mapCanvas().refreshAllLayers()

    qgis.utils.iface.layerTreeView().refreshLayerSymbology(layer.id())


# Various functions used for setting the map zoom.
def fix():
    qgis.utils.iface.mapCanvas().zoomToFullExtent()


def zoom(factor=0.5):
    qgis.utils.iface.mapCanvas().zoomByFactor(factor)


def zoomToLayer(layer):
    canvas = qgis.utils.iface.mapCanvas()
    extent = layer.extent()
    canvas.setExtent(extent)


# Function used for renaming a layer.
def name(layer, name):
    layer.setName(name)


# Sample code:
#    l = poland()
#    geoi.name(l, "new name")


# Test function. Reads a layer, modifies its transparency and changes the zoom level.
def test():
    l = polska()
    setTransparency(l, 0.2)
    fix()
    zoom(2.0)
    return l


# Fun fact!
# In Python console, the last returned value can be obtained with the "_" character:
#    import geoi
#    geoi.test()
#    geoi.remove(_)
# which is equivalent to this:
#    import geoi
#    l = geoi.test()
#    geoi.remove(l)


# Function used for printing the number of elements and fields of a vector layer.
def numbers(vlayer):
    # obtain vector layer data:
    provider = vlayer.dataProvider()

    print("Number of Elements:", provider.featureCount())
    print("Number of Fields:", provider.fields().count())

    return provider.featureCount(), provider.fields().count()


# Function used for printing information about vector layer fields.
def fields(vlayer):
    provider = vlayer.dataProvider()

    # obtain dictionary with fields:
    ftab = provider.fields()

    # print field names:
    print("Field names:")
    for f in range(provider.fields().count()):
        print(ftab[f].name())


# Function used for checking the type of a geometric object.
def getGeometryName(feat):
    if feat.geometry() == None:
        return "Not a shape!"

    if feat.geometry().type() == qgis.core.QgsWkbTypes.PointGeometry:
        return "Point"
    elif feat.geometry().type() == qgis.core.QgsWkbTypes.LineGeometry:
        return "Line"
    elif feat.geometry().type() == qgis.core.QgsWkbTypes.PolygonGeometry:
        return "Polygon"
    elif feat.geometry().type() == qgis.core.QgsWkbTypes.UnknownGeometry:
        return "Unknown geometry"
    else:
        print("Unknown code")
    # Note: the geometry() function returns an object representing basic geometric information,
    # such as vertex arrangement. Among other things, this object also features the area() function.


# Function used for transforming the coordinate system. Useful for converting degrees to meters.
def transformCoordinates(featGeometry, sourceEpsg=4326, destEpsg=2180):
    geomClone = qgis.core.QgsGeometry(featGeometry)
    sourceCrs = qgis.core.QgsCoordinateReferenceSystem(sourceEpsg)
    destCrs = qgis.core.QgsCoordinateReferenceSystem(destEpsg)
    tr = qgis.core.QgsCoordinateTransform(
        sourceCrs, destCrs, qgis.core.QgsProject.instance()
    )
    geomClone.transform(tr)
    return geomClone


# Function used for printing information about layer attributes at index indicated by the nr parameter.
def features(vlayer, nr=6):
    provider = vlayer.dataProvider()

    # obtain an iterator for all features:
    feature_list = provider.getFeatures()

    # variable used for each feature returned by the iterator:
    feat = qgis.core.QgsFeature()

    # iterate over all features:
    while feature_list.nextFeature(feat):
        print(
            "Element no. ",
            feat.id(),
            ":",
            getGeometryName(feat),
            " - represents ",
        )
        attrs = feat.attributes()
        print(attrs[nr].encode("utf-8"))


# Function used for adding a new layer field called "area".
def addArea(vlayer):

    # turn on layer editing:
    if not vlayer.isEditable():
        vlayer.startEditing()
        print("Start editing!")
    else:
        print("Editing session already in progress!")

    provider = vlayer.dataProvider()
    caps = provider.capabilities()

    # add a field of type Double:
    if caps & qgis.core.QgsVectorDataProvider.AddAttributes:
        res = vlayer.dataProvider().addAttributes(
            [qgis.core.QgsField("area", qtc.QVariant.Double)]
        )
        print("Success:", res)
    else:
        print("No")

    # save changes:
    vlayer.commitChanges()


# Function used for modifying the contents of the first element in the provided layer.
# The second parameter indicates which attribute is to be changed.
def fillArea(vlayer, nr=9):
    if not vlayer.isEditable():
        vlayer.startEditing()
        print("Start editing!")
    else:
        print("Editing session already in progress!")

    # change value for element at index 0:
    res = vlayer.changeAttributeValue(0, nr, 72.5)
    print("Success:", res)
    vlayer.commitChanges()


# Function used for removing a layer attribute.
def delArea(vlayer, nr=9):
    # Turn on layer editing mode:
    if not vlayer.isEditable():
        vlayer.startEditing()
        print("Start editing!")
    else:
        print("Editing session already in progress!")

    # remove the attribute at index indicated by the nr variable:
    res = vlayer.deleteAttribute(nr)
    vlayer.commitChanges()
    print("Success:", res)


##############################################################################################################################################################
##############################################################################################################################################################
##############################################################################################################################################################

# Tasks to be carried out:

# Task 1 (2.5 points)
# Create Python code which will:
# 1. remove any existing layers from QGIS interface
# 2. add 3 new layers from the following files:
#    - WORLD_RG_10M_2010.shp
#    - POL_adm1.shp
#    - POL_adm2.shp
# 3. set the names, colors, transparencies and order of these layers so that:
#    - Poland is clearly divided into voivodeships and counties
#    - the color of Poland is different from all other countries on the map
# 4. adjust the zoom to make Poland cover most of the visible map


def task1():
    # 1. remove existing layers
    clear()

    # 2. load layers
    world_path = path + "WORLD_RG_10M_2010.shp"
    voiv_path = path + "POL_adm1.shp"
    county_path = path + "POL_adm2.shp"

    world_layer = qgis.core.QgsVectorLayer(world_path, "World", "ogr")
    voiv_layer = qgis.core.QgsVectorLayer(voiv_path, "Województwa", "ogr")
    county_layer = qgis.core.QgsVectorLayer(county_path, "Powiaty", "ogr")

    for lyr in (world_layer, voiv_layer, county_layer):
        if not lyr.isValid():
            error("Layer failed to load: " + lyr.name())
            return
        fixEncoding(lyr)

    qgis.core.QgsProject.instance().addMapLayer(world_layer)
    qgis.core.QgsProject.instance().addMapLayer(voiv_layer)
    qgis.core.QgsProject.instance().addMapLayer(county_layer)

    # 3. set colors and transparencies
    setColor(world_layer, 180, 180, 180)
    setTransparency(world_layer, 0.0)

    setCategorizedColors(voiv_layer, field_name="NAME_1", opacity=0.7)

    setColor(county_layer, 0, 80, 200)
    setTransparency(county_layer, 0.5)

    # 4. zoom to Poland
    zoomToLayer(voiv_layer)
    qgis.utils.iface.mapCanvas().refresh()

    print("Task 1 done.")
    return world_layer, voiv_layer, county_layer


# Task 2 (2.5 points)
# Create Python code which will:
# 1. remove any existing layers from QGIS interface
# 2. add a vector layer representing the map of Poland divided into voivodeships
# 3. obtain polygons representing all voivodeships, calculate the area of each polygon
#    and store the results, along with voivodeship names, in a new text file
# 4. create a new "area" field in this layer and fill it with corresponding polygon areas


def task2():
    # 1. remove existing layers
    clear()

    # 2. load voivodeships layer
    voiv_path = path + "POL_adm1.shp"
    vlayer = qgis.core.QgsVectorLayer(voiv_path, "Województwa", "ogr")
    if not vlayer.isValid():
        error("Layer failed to load!")
        return
    fixEncoding(vlayer)
    qgis.core.QgsProject.instance().addMapLayer(vlayer)
    setCategorizedColors(vlayer, field_name="VARNAME_1", opacity=0.7)

    provider = vlayer.dataProvider()
    feature_list = provider.getFeatures()
    feat = qgis.core.QgsFeature()

    field_names = [
        provider.fields()[i].name() for i in range(provider.fields().count())
    ]
    name_idx = field_names.index("VARNAME_1") if "VARNAME_1" in field_names else 4

    # 3. calculate areas and write to file
    results = []
    while feature_list.nextFeature(feat):
        voiv_name = feat.attributes()[name_idx]
        geom_metric = transformCoordinates(
            feat.geometry(), sourceEpsg=4326, destEpsg=2180
        )
        area_km2 = geom_metric.area() / 1_000_000
        results.append((feat.id(), voiv_name, area_km2))
        print(f"  {voiv_name}: {area_km2:.2f} km²")

    out_path = os.path.dirname(__file__) + "/voivodeships_areas.txt"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("id\tname\tarea_km2\n")
        for fid, vname, akm2 in results:
            f.write(f"{fid}\t{vname}\t{akm2:.2f}\n")
    print(f"Areas written to: {out_path}")

    # 4. add area field and fill it
    existing_names = [
        provider.fields()[i].name() for i in range(provider.fields().count())
    ]
    if "area" in existing_names:
        delArea(vlayer, existing_names.index("area"))

    addArea(vlayer)

    provider = vlayer.dataProvider()
    updated_names = [
        provider.fields()[i].name() for i in range(provider.fields().count())
    ]
    area_field_idx = updated_names.index("area")

    vlayer.startEditing()
    for fid, _vname, akm2 in results:
        vlayer.changeAttributeValue(fid, area_field_idx, akm2)
    vlayer.commitChanges()

    label_settings = qgis.core.QgsPalLayerSettings()
    label_settings.fieldName = "area"
    label_settings.isExpression = False
    labeling = qgis.core.QgsVectorLayerSimpleLabeling(label_settings)
    vlayer.setLabeling(labeling)
    vlayer.setLabelsEnabled(True)
    vlayer.triggerRepaint()

    print("Task 2 done.")
    return vlayer
