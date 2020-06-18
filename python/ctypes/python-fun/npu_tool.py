import os,sys,cv2,json,convert_class
from ctypes import *
import numpy as np

class yolo:

#	def __init__(self):
#	def __del__(self):

	detect_so = CDLL('/usr/lib/libnn_detect.so')
	image = convert_class.image()
	pix_fmt = convert_class.det_pixel_format.PIX_FMT_RGB888
	DetectResult = convert_class.DetectResult()
	det_yolo_v3 = convert_class.det_model_type.DET_YOLO_V3

	def release_model(self, det_type) :
		det_release_model = self.detect_so.det_release_model
		det_release_model.argtypes = [c_int]
		det_release_model(c_int(det_type))

	def set_model(self, det_type):
		SET_MODEL_STATUS = self.detect_so.det_set_model(det_type)
		if SET_MODEL_STATUS :
			sys.exit('open libnn_detect.so fail'
					+ ',please check the share libaray had install first!')

	def get_model_size(self, det_type, width,height,channel):
		det_get_model_size = self.detect_so.det_get_model_size
		det_get_model_size.argtypes = [c_int,POINTER(c_int),POINTER(c_int),POINTER(c_int)]
		GET_MODEL_SIZE_STATUS = det_get_model_size(c_int(det_type),
				pointer(width),pointer(height),pointer(channel))
		if GET_MODEL_SIZE_STATUS :
			sys.exit('get model size fail !')
		return width,height,channel

	def set_input(self, image, det_type):
		det_set_input = self.detect_so.det_set_input
		det_set_input.argtypes = [convert_class.image,c_int]
		SET_INPUT_STATUS = det_set_input(self.image,c_int(det_type))
		if SET_INPUT_STATUS :
			self.release_model(det_type)
			sys.exit('set input faild !!!')

	def get_result(self, detectResult, det_type):
		det_get_result = self.detect_so.det_get_result
		det_get_result.argtypes = [POINTER(convert_class.DetectResult),c_int]
		GET_RESULT_STATUS = det_get_result(pointer(detectResult),c_int(det_type))
		if GET_RESULT_STATUS :
			self.release_model(det_type)
			sys.exit('det_get_result failure  !!!')

	def generate_list(self, detectResult, img_width, img_height):
		result_list = []
		for i in range(0,detectResult.detect_num) :
			left = detectResult.point[i].point.rectPoint.left*img_width
			right = detectResult.point[i].point.rectPoint.right*img_width
			top = detectResult.point[i].point.rectPoint.top*img_height
			bottom = detectResult.point[i].point.rectPoint.bottom*img_height
			if top<50 :
				top = 50
				left += 10
			convert_dict = {'name':bytes.decode(detectResult.class_name[i].class_name),
				'possibility':detectResult.class_name[i].possibility,
				'location':[left,top,right,bottom]}
			result_list.append(convert_dict)
		return result_list


	def run_detect_model(self, frame):
		nn_width = c_int(0)
		nn_height = c_int(0)
		nn_channel = c_int(0)
		
		self.set_model(self.det_yolo_v3.value)

		nn_width,nn_height,nn_channel = self.get_model_size(self.det_yolo_v3.value,nn_width,nn_height,nn_channel)	
		matrix = cv2.resize(frame,(nn_width.value,nn_height.value))
		self.image.data = matrix.data.tobytes()
		self.image.width = matrix.shape[1]
		self.image.height = matrix.shape[0]
		self.image.channel = matrix.shape[2]
		self.image.pixel_format = self.pix_fmt.value

		self.set_input(self.image, self.det_yolo_v3.value)

		self.get_result(self.DetectResult, self.det_yolo_v3.value)

		result_list = self.generate_list(self.DetectResult, frame.shape[1], frame.shape[0])

		self.release_model(self.det_yolo_v3.value)
		return result_list

	def disc_picture(self, frame):
		return self.run_detect_model(frame)










