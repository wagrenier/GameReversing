# Import Statements
import struct
import numpy as np
import open3d as o3d


# Global params
folder = 'D:/DecompressFiles/Fatal Frame Undub/mdl'
file = '1064.out'

# Model, Start Offset, End Offset,   Size
# Hand,     0x562A0,       0x58990,   224
# Face,     0x349E0,       0x3B530,   714
# Body,     0x25D0,       0x3B530,   2769

# body offset for mdl offset: 0x6B0  cx
# arm offset for mdl offset: 0x790

# Size : Offset: 0x5C, Size = read 4 bytes then divide by 16 -> number of points

# Texture UV Header (?) : 00 00 00 20 D0 D0 D0 D0


def render_mdl():
    file_r = open(f'{folder}/{file}', 'rb')
    global_mdl = []
    num_mdl = struct.unpack('<I', file_r.read(0x4))[0]

    file_r.seek(0x10)

    curr_mdl_index = 0
    file_r.seek(0x10)

    while curr_mdl_index < num_mdl:
        curr_pos = file_r.tell()
        jump_address = struct.unpack('<I', file_r.read(0x4))[0]

        file_r.seek(0x1C, 1)
        mdl_coord_address = struct.unpack('<I', file_r.read(0x4))[0]
        file_r.seek(mdl_coord_address, 1)
        temp_backward = file_r.tell()

        file_r.seek(0x18, 1)
        num_mdl_coord = struct.unpack('<I', file_r.read(0x4))[0] / 16

        if num_mdl_coord == 0:
            file_r.seek(temp_backward - 0x8)
            num_mdl_coord = struct.unpack('<I', file_r.read(0x4))[0] / 16
            file_r.seek(0x30, 1)

        file_r.seek(0x10, 1)

        curr_mdl = get_points_from_file(file_r, [file_r.tell(), num_mdl_coord], [0.0, 0.0, 0.0])

        file_r.seek(curr_pos)
        file_r.seek(jump_address + 0x10, 1)

        if num_mdl_coord > 0:
            global_mdl = append_mdl(global_mdl, curr_mdl)

            render_points(curr_mdl[0], curr_mdl[1], curr_mdl[2])

        print(f'Model #{curr_mdl_index}, at position: {curr_pos}, num coords: {num_mdl_coord}')
        curr_mdl_index += 1

    file_r.close()
    render_points(global_mdl[0], global_mdl[1], global_mdl[2])


def get_points_from_file(file_r, model_info, coord_offsets, skip_last_float=True):
    file_r.seek(model_info[0])

    x_points = []
    y_points = []
    z_points = []

    points_read = 0

    while points_read < model_info[1]:
        x_points.append(struct.unpack('f', file_r.read(0x4))[0] + coord_offsets[0])
        y_points.append(struct.unpack('f', file_r.read(0x4))[0] + coord_offsets[1])
        z_points.append(struct.unpack('f', file_r.read(0x4))[0] + coord_offsets[2])

        if skip_last_float:
            unknown_value = struct.unpack('f', file_r.read(0x4))

        points_read += 1

    return x_points, y_points, z_points


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


def append_mdl(mdl_a, mdl_b):
    if len(mdl_a) <= 0:
        return mdl_b
    return [append_coord(mdl_a[0], mdl_b[0]), append_coord(mdl_a[1], mdl_b[1]), append_coord(mdl_a[2], mdl_b[2])]


def append_coord(coord_a, coord_b):
    for coord in coord_b:
        coord_a.append(coord)

    return coord_a


if __name__ == '__main__':
    #render_mdl()
    file = open(f'{folder}/{file}', 'rb')
    x, y, z = get_points_from_file(file, [0x16488, 181], [0.0, 0.0, 0.0], False)

    render_points(x,y,z)
    file.close()
