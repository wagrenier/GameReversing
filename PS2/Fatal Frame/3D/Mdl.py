# Logic for a Project Zero MDL file
from Sgd import Sgd
import numpy as np
import open3d as o3d

# Model, Start Offset, End Offset,   Size
# Hand,     0x562A0,       0x58990,   224
# Face,     0x349E0,       0x3B530,   714
# Body,     0x25D0,       0x3B530,   2769

# body offset for mdl offset: 0x6B0  cx
# arm offset for mdl offset: 0x790

# Size : Offset: 0x5C, Size = read 4 bytes then divide by 16 -> number of points

# Texture UV Header (?) : 00 00 00 20 D0 D0 D0 D0


# Global MDL File Values
from StandardFileOperations.FileReadOperation import get_uint32

num_mdl_in_file_offset_info = 0x0  # Only first time is non zero
next_model_file_offset_info = 0x10
sgd_file_start_offset = 0x20


class Mdl:
    def __init__(self, folder, file):
        self._file = open(f'{folder}/{file}', 'rb')
        self._sgd_files = []
        self._num_mdl = get_uint32(self._file)
        self.__create_Sgd()
        self._file.close()

    def render_mdl(self):
        for sgd in self._sgd_files:
            print(f'Model #{sgd._mdl_id}, at position: {sgd._file_start_offset}, num coords: {sgd._num_vertices}, num parts: {sgd._num_parts}')
            render_points(sgd._vertices.x, sgd._vertices.y, sgd._vertices.z)

    def __create_Sgd(self):
        sgd = Sgd(sgd_file_start_offset, 0)
        sgd.build_sgd(self._file)
        self._sgd_files.append(sgd)
        self._file.seek(0)

        while len(self._sgd_files) < self._num_mdl:
            self._file.seek(next_model_file_offset_info, 1)
            curr_pos = self._file.tell()
            jump_address = get_uint32(self._file)
            sgd = Sgd(curr_pos + jump_address + sgd_file_start_offset, len(self._sgd_files))
            sgd.build_sgd(self._file)
            self._sgd_files.append(sgd)
            self._file.seek(curr_pos + jump_address)


def render_points(x_data, y_data, z_data):
    points = []

    index = 0
    while index < len(x_data):
        points.append([x_data[index], y_data[index], z_data[index]])
        index += 1

    pcl = o3d.geometry.PointCloud()
    pcl.points = o3d.utility.Vector3dVector(points)

    viewer = o3d.visualization.Visualizer()
    viewer.create_window()
    viewer.add_geometry(pcl)
    opt = viewer.get_render_option()
    opt.show_coordinate_frame = True
    opt.background_color = np.asarray([0.5, 0.5, 0.5])
    viewer.run()
    viewer.destroy_window()


if __name__ == '__main__':
    folderf = 'D:/DecompressFiles/Fatal Frame Undub/mdl'
    filef = '1064.out'

    a = Mdl(folderf, filef)
    a.render_mdl()
