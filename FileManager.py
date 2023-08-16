from dxfwrite import DXFEngine as dxf
import Shapes
import math
import numpy as np

class File:
    def __init__(self, measurements):
        self.drawing = dxf.drawing('doublet.dxf')
        self.drawing.add_layer('MESH', color=7, linetype='CONTINUOUS')
        self.drawing.add_layer('BASIC_CONTOUR', color=3, linetype='CONTINUOUS')

        self.measurements = measurements
        self.mesh = Shapes.BasicShapes(self.drawing, 'MESH')
        self.basic_contour = Shapes.BasicShapes(self.drawing, 'BASIC_CONTOUR')

        self.mesh_width = 0;

    def save(self):
        self.drawing.save()

    def draw_mesh(self):
        mesh_width = (self.measurements["OH"] / 2) + 3

        HP = self.measurements["HP"]
        DZ = self.measurements["DZ"]
        HB = self.measurements["HB"]
        SZ = self.measurements["ŠZ"]
        SP = self.measurements["ŠP"]

        hip = self.mesh.rectangle(0, 0, mesh_width, -(DZ + HB))
        chest = self.mesh.line(0, -HP, mesh_width, -HP)
        waist = self.mesh.line(0, -DZ, mesh_width, -DZ)
        side = self.mesh.line((mesh_width / 2) + 1, -HP, (mesh_width / 2) + 1, -(DZ + HB))
        back_width = self.mesh.line(SZ/2, 0, SZ/2, -HP)
        front_width = self.mesh.line(mesh_width - (SP / 2), 0, mesh_width - (SP / 2), -HP)

        self.mesh_width = mesh_width

    def draw_basic_contour(self):
        OH = self.measurements["OH"]
        OP = self.measurements["OP"]
        OB = self.measurements["OB"]

        HP = self.measurements["HP"]
        DZ = self.measurements["DZ"]
        HB = self.measurements["HB"]
        SZ = self.measurements["ŠZ"]
        SP = self.measurements["ŠP"]

        doublet_length = DZ + 12

        neck_width = (OH/20)+3
        armpit_point = ((self.mesh_width / 2) + 1, -HP)
        shoulder_armhole = (SZ/2, 0)

        # --------------------------------------------------------------------
        # back part
        up_back = dxf.polyline([(SZ/2, 0),
                                (neck_width, 3),
                                (neck_width, 0),
                                (0, 0),
                                (0, -HP),
                                (2, -DZ),
                                (0, -doublet_length),
                                (OB/4,-doublet_length),
                                ((OP/4)+2-1, -DZ),
                                armpit_point])

        # shoulder line
        shoulder_armhole = self.shoulder_armhole_point(neck_width, 5)

        tan = (3 - 0) / (neck_width - SZ / 2)
        size = 10
        shoulder_vector = [size, tan*size]
        shoulder_armhole_vector = [shoulder_vector[1], -shoulder_vector[0]]

        # armhole
        bezier = dxf.bezier()
        bezier.start(shoulder_armhole, tangent=tuple(shoulder_armhole_vector))
        bezier.append(armpit_point, tangent1=(-9, 0), tangent2=(6, 0))

        # --------------------------------------------------------------------
        # front part
        up_front = dxf.polyline([(self.mesh_width - neck_width, 1),
                                (self.mesh_width, -neck_width - 1),
                                (self.mesh_width + 3, -HP),
                                (self.mesh_width - 1, -DZ),
                                (self.mesh_width, -doublet_length),
                                (self.mesh_width - (OB/4), -doublet_length),
                                (self.mesh_width - 1 - (OP / 4), -DZ),
                                armpit_point])

        self.drawing.add(bezier)
        self.drawing.add(up_back)
        self.drawing.add(up_front)

    def shoulder_armhole_point(self, neck_width, shoulder_len):
        SZ = self.measurements["ŠZ"]

        tan = (3 - 0) / (neck_width - SZ / 2)
        mov = 0 - tan * SZ / 2

        a_sq = (1 - tan * tan)
        b_sq = 2 * (tan * mov - neck_width - tan * 3)
        c_sq = pow(neck_width, 2) + pow(3, 2) + pow(mov, 2) - pow(shoulder_len, 2) - 2 * mov * 3

        xx = np.roots([a_sq, b_sq, c_sq])

        print(neck_width)
        print(xx[0])

        if(xx[0] > neck_width): xx1 = xx[0]
        else: xx1 = xx[1]

        yy = tan*xx1 + mov

        return [xx1, yy]

