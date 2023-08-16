from dxfwrite import DXFEngine as dxf


class BasicShapes:
    def __init__(self, drawing, input_layer):
        self.layer = input_layer
        self.drawing = drawing

    def line(self, x0, y0, x1, y1):
        line = dxf.line((x0, y0), (x1, y1), layer=self.layer)
        self.drawing.add(line)

        return line

    def rectangle(self, x0, y0, x1, y1):
        rect = dxf.rectangle((x0, y0), x1, y1, layer=self.layer)
        self.drawing.add(rect)

        return rect
