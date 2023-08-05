"""
References:
    https://github.com/lohriialo/photoshop-scripting-python/blob/master/ActiveLayer.py

"""
import photoshop as ps

app = ps.Application()

if len(app.documents) < 1:
    docRef = app.documents.add()
else:
    docRef = app.activeDocument

if len(docRef.layers) < 2:
    docRef.artLayers.add()

activeLayerName = docRef.activeLayer.name
SetLayerName = ''
if docRef.activeLayer.name != app.activeDocument.layers.item(len(docRef.layers)).name:
    docRef.activeLayer = docRef.layers.item(len(docRef.layers))
else:
    docRef.activeLayer = docRef.layers.item(1)
