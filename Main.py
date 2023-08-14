from dxfwrite import DXFEngine as dxf

DZ = 42
HP = 20
HB = 22
OH = 100
OP = 82
OB = 100

mesh_width = (OH/2)+3

drawing = dxf.drawing('doublet.dxf')
drawing.add_layer('MESH', color=7, linetype='CONTINUOUS')

# chest_line = dxf.rectangle((0, 0), mesh_width, -DZ, layer='MESH')
# waist_line = dxf.rectangle((0, 0), mesh_width, -HP, layer='MESH')
hip_line = dxf.rectangle((0, 0), mesh_width, -(DZ+HB), layer='MESH')
chest_line = dxf.line((0, -HP), (mesh_width, -HP), layer='MESH')
waist_line = dxf.line((0, -DZ), (mesh_width, -DZ), layer='MESH')
side_line = dxf.line(((mesh_width/2)+1, -HP), ((mesh_width/2)+1, -(DZ+HB)), layer='MESH')



drawing.add(chest_line)
drawing.add(waist_line)
drawing.add(hip_line)
drawing.add(side_line)

drawing.save()