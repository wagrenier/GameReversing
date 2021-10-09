# Import Statements
from StandardFileOperations.FileReadOperation import get_uint_from_byte, get_uint32, get_float32
from Vertex_Points import VertexPoints

# Global SGD File Values
sgd_header = b'\x10\x50\x00\x00'
mdl_parts_num_offset = 0x6  # uint32 value indicating the number of parts in this model
texture_offset_info = 0xC
vertex_offset_info = 0x10  # uint32 value indicating the offset from the header to the vertices header start
num_vertices_offset_info = 0x2C  # 0x28 (?)
vertices_points_offset_info = 0x40


class Sgd:
    def __init__(self, file_start_offset, mdl_id):
        self._file_start_offset = file_start_offset
        self._vertices = VertexPoints()
        self._num_parts = 0
        self._num_vertices = 0
        self._mdl_id = mdl_id
        self._parts_address = []

    def build_sgd(self, file):
        self.__get_num_parts(file)
        self.__build_vertices(file)

    def __get_num_parts(self, file):
        file.seek(self._file_start_offset + mdl_parts_num_offset)

        self._num_parts = get_uint_from_byte(file)

    def __build_vertices(self, file):
        file.seek(self._file_start_offset + vertex_offset_info)
        mdl_coord_address = get_uint32(file)
        file.seek(self._file_start_offset + mdl_coord_address + num_vertices_offset_info)

        self._num_vertices = get_uint32(file) / 16
        if self._num_vertices == 0:
            file.seek(self._file_start_offset + mdl_coord_address + 0xC)
            self._num_vertices = self._num_vertices = get_uint32(file) / 16
            file.seek(self._file_start_offset + mdl_coord_address + vertices_points_offset_info)
            self.__get_vertices_points(file, self._num_vertices)
        else:
            file.seek(self._file_start_offset + mdl_coord_address + vertices_points_offset_info)
            self.__get_vertices_points(file, self._num_vertices)

    def __get_vertices_points(self, file, num_vertices, skip_last_float=True):
        points_read = 0

        while points_read < num_vertices:
            x = get_float32(file)
            y = get_float32(file)
            z = get_float32(file)

            if skip_last_float:
                unknown_value = get_float32(file)

            self._vertices.add_point(x, y, z)

            points_read += 1
