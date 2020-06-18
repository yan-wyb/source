from ctypes import *
from enum import Enum, unique

MAX_LABEL_LENGTH = 64
MAX_DETECT_NUM = 10

class det_pixel_format(Enum):
	PIX_FMT_GRAY8 = 0
	PIX_FMT_YUV420P = 1
	PIX_FMT_NV12 = 2
	PIX_FMT_NV21 = 3
	PIX_FMT_BGRA8888 = 4
	PIX_FMT_BGR888 = 5
	PIX_FMT_RGBA8888 = 6
	PIX_FMT_RGB888 = 7

class det_position_type(Enum):
	DET_SINGLEPOINT_TYPE = 1
	DET_RECTANGLE_TYPE = 2
	DET_CIRCLE_TYPE = 3
	DET_IMAGE_TYPE = 4


class det_model_type(Enum):
	DET_YOLOFACE_V2 = 0
	DET_YOLO_V2 = 1
	DET_YOLO_V3 = 2
	DET_YOLO_TINY = 3
	DET_SSD = 4
	DET_MTCNN_V1 = 5
	DET_MTCNN_V2 = 6
	DET_FASTER_RCNN = 7
	DET_DEEPLAB_V1 = 8
	DET_DEEPLAB_V2 = 9
	DET_DEEPLAB_V3 = 10
	DET_FACENET = 11
	DET_BUTT = 12

class box(Structure):
	_fields_ = [
		('x',c_float),
		('y',c_float),
		('w',c_float),
		('h',c_float),
		('prob_obj',c_float)
	]

class det_rect_point_t(Structure):
	 _fields_ = [
		('left', c_float),
		('top', c_float),
		('right', c_float),
		('bottom', c_float),
		('score', c_float)
	]

class det_circle_point_t(Structure):
	 _fields_ = [
	 	('center', c_float),
		('radius', c_float),
		('score', c_float)
	]

class det_single_point_t(Structure):
	 _fields_ = [
		('x', c_float),
		('y', c_float),
		('param', c_float)
	]

class image(Structure):
	_fields_ = [
		('data',c_char_p),
		('pixel_format',c_int),
		('width',c_int),
		('height',c_int),
		('channel',c_int)
	]

class det_classify_result_t(Structure):
	_fields_ = [
		('lable_id',c_int),
		('lable_name',c_char*MAX_LABEL_LENGTH)
	]

class det_class_result_t(Structure):
	_fields_ = [
		('possibility',c_float),
		('class_name',c_char*MAX_LABEL_LENGTH)
	]

class point(Union):
	_fields_ = [
		('rectPoint', det_rect_point_t),
		('circlePoint', det_circle_point_t),
		('singlePoint', det_single_point_t),
		('imageData', image)
	]

class face_pts(Structure):
	_fields_ = [
		('floatX', c_float*5),
		('floatY', c_float*5)
	]

class det_position_float_t(Structure):
	_fields_ = [
		('type', c_int),
		('point', point),
		('tpts', face_pts),
		('reserved', c_char*4)
	]

class DetectResult(Structure):
	_fields_ = [
		('detect_num', c_int),
		('facenet_result', c_float*128),
		('result_name', det_classify_result_t*MAX_DETECT_NUM),
		('class_name', det_class_result_t*MAX_DETECT_NUM),
		('point', det_position_float_t*MAX_DETECT_NUM)
	]






