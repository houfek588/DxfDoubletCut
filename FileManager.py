from dxfwrite import DXFEngine as dxf
import Shapes
import Geometry
import numpy as np

class File:
    def __init__(self, measurements):
        self.drawing = dxf.drawing('doublet.dxf')
        self.drawing.add_layer('MESH', color=3, linetype='CONTINUOUS')
        self.drawing.add_layer('BASIC_CONTOUR', color=6, linetype='CONTINUOUS')

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
        SR = self.measurements["ŠR"]

        doublet_length = DZ + 12

        neck_width = (OH/20)+3
        armpit_point = ((self.mesh_width / 2) + 1, -HP)
        shoulder_armhole = (SZ/2, 0)

        # --------------------------------------------------------------------
        # back part
        up_back = dxf.polyline([(SZ/2, 0),
                                (neck_width, 3),
                                # (neck_width, 0),
                                (0, -HP/2),
                                (0, -HP),
                                (2, -DZ),
                                (0, -doublet_length),
                                (OB/4,-doublet_length),
                                ((OP/4)+2-1, -DZ),
                                armpit_point],
                                layer=self.basic_contour.get_layer())

        self.back_armhole(neck_width, armpit_point)
        self.drawing.add(up_back)

        # --------------------------------------------------------------------
        # front part
        x0 = self.mesh_width - (SP / 2)
        y0 = -5
        arc1 = [(self.mesh_width - (SP / 2), -HP), HP-5]
        arc2 = [(self.mesh_width - neck_width, 1), SR]
        front_shoulder_armhole = Geometry.circle_circle_intersection(arc1, arc2, x0, y0)

        up_front = dxf.polyline([front_shoulder_armhole,
                                (self.mesh_width - neck_width, 1),
                                (self.mesh_width, -neck_width - 1),
                                (self.mesh_width + 3, -HP),
                                (self.mesh_width - 1, -DZ),
                                (self.mesh_width, -doublet_length),
                                (self.mesh_width - (OB/4), -doublet_length),
                                (self.mesh_width - 1 - (OP / 4), -DZ),
                                armpit_point],
                                layer=self.basic_contour.get_layer())

        self.front_armhole(neck_width, armpit_point, front_shoulder_armhole)
        self.drawing.add(up_front)


    def back_armhole(self, neck_width, armpit_point):
        SZ = self.measurements["ŠZ"]

        # shoulder line
        shoulder_armhole = Geometry.line_circle_intersection([(neck_width, 3), (SZ/2, 0)], [(neck_width, 3), 5])
        print('a = ')
        print(shoulder_armhole)


        # shoulder_armhole = self.shoulder_armhole_point(neck_width, 5)

        back_slope = (3 - 0) / (neck_width - SZ / 2)
        size = 10
        back_shoulder_vector = [size, back_slope*size]
        shoulder_armhole_vector = [back_shoulder_vector[1], -back_shoulder_vector[0]]

        # armhole
        bezier = dxf.bezier(layer=self.basic_contour.get_layer())
        bezier.start(shoulder_armhole, tangent=tuple(shoulder_armhole_vector))
        bezier.append(armpit_point, tangent1=(-9, 1), tangent2=(6, 0))

        self.drawing.add(bezier)

    def front_armhole(self, neck_width, armpit_point, front_shoulder_armhole_point):
        front_slope = (front_shoulder_armhole_point[1] - 1) / (front_shoulder_armhole_point[0] - (self.mesh_width - neck_width))
        front_size = 15
        front_shoulder_vector = [front_size, front_slope * front_size]
        front_shoulder_armhole_vector = [front_shoulder_vector[1], -front_shoulder_vector[0]]
        shoulder_armhole1 = Geometry.line_circle_intersection(
            [front_shoulder_armhole_point, (self.mesh_width - neck_width, 1)], [(self.mesh_width - neck_width, 1), 5])

        # armhole
        bezier_front = dxf.bezier(layer=self.basic_contour.get_layer())
        bezier_front.start(shoulder_armhole1, tangent=tuple(front_shoulder_armhole_vector))
        bezier_front.append(armpit_point, tangent1=(15, -2), tangent2=(10, 0))

        self.drawing.add(bezier_front)