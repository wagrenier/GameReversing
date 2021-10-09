def _append_points(main_list, sublist):
    for item in sublist:
        main_list.append(item)


class VertexPoints:
    def __init__(self):
        self.x = []
        self.y = []
        self.z = []

    def add_point(self, x, y, z):
        self.x.append(x)
        self.y.append(y)
        self.z.append(z)

    def add_points(self, x_list, y_list, z_list):
        _append_points(self.x, x_list)
        _append_points(self.y, y_list)
        _append_points(self.z, z_list)


if __name__ == '__main__':
    a = [1, 2, 3, 4]
    b = [5, 6, 7, 8]
    c = [5, 6, 7, 8]
    d = VertexPoints()
    d.add_points(a, b, c)
    print(d.x)
