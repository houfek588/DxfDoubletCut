from dxfwrite import DXFEngine as dxf
import FileManager
import Shapes

measurements = {
    "OH": 100,
    "OP": 82,
    "OB": 100,
    "DZ": 42,
    "HP": 20,
    "HB": 22,
    "ŠZ": 41,
    "ŠP": 42,
}

draft = FileManager.File(measurements)

draft.draw_mesh()
draft.draw_basic_contour()

draft.save()


