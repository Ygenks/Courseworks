#!/usr/bin/python

import os.path							#Importing OS functions
from PIL import Image 					#Importing image processing module 

class PictureProcessing():
	"""Image processing class"""
	def __init__(self):
		self.path = None			#Path to current image
		self.bitmapped = False 		#Bitmapped status
		self.bitmap_path = None		#Path to bitmapped image
		self.output_path = None		#Path to output file
		self.bitmap_opt = {}		#Bitmap options dictionaty
		self.trace_opt = {}			#Trace options dictionaty
	def convert_to(self, extension):
		"""Converting image"""
		img = Image.open(self.path)			#Opening current image
		if extension != None:				#Cheking for extension existence
			new_image = self.path.split('.')[0] + '.' + extension #Parsing image name and adding new format
			self.path = new_image	
		else:
			new_image = self.path				#Saving case
		img.save(new_image)						#Converting image to new format
	def save_image(self, new_name, extension):
		"""Saving image"""
		img = Image.open(self.path)				#Opening current image
		img.save(new_name + '.' + extension)	#Saving with new extension
	def make_bitmap(self):
		"""Making bitmap"""
		new_path = self.path.split('.')[0] + '.' + "pbm"						#Calculating bitmap path
		opt_string = self.dict_to_string(self.bitmap_opt)						#Getiing string with bitmap options from dictionary	
		os.system('mkbitmap %s %s -o %s' % (opt_string, self.path, new_path))	#Starting bitmap
		self.bitmap_path = new_path												#Setting bitmap path 
	def trace_bitmap(self):
		"""Tracing bitmap"""
		opt_string = self.dict_to_string(self.trace_opt)						#Getiing string with trace options from dictionary	
		os.system('potrace %s %s' % (opt_string, self.bitmap_path))				#Tracing bitmap
	def dict_to_string(self, dict):
		"""Extract options from dictionary to string"""
		first_step = map(lambda x :(x[0], str(x[1])) if isinstance(x[1], str) is not True 
							else x, dict.items()) 					 #[(str, int),(str, int), ..] => [(str, str),(str, str), ..] 
		second_step = map(lambda x : ' '.join(x), first_step)		 #[(str, str),(str, str), ..] => [str, str, ..]
		result = ' '.join(second_step)								 #[str, str, ..] => "str str ..."	
		return result 												 #Returning result string 
			