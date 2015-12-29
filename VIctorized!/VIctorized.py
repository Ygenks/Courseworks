#!/usr/bin/python

from gi.repository import Gtk			#Importing Gtk module
from PicProc import PictureProcessing

class MainWindow:
	def __init__(self):				
		self.gladefile = "VIctorized.glade"					#Importing Glade-xml file
		self.builder = Gtk.Builder()						#Starting interface builder
		self.builder.add_from_file(self.gladefile)			#Adding Glade file
		
		self.builder.connect_signals(self)					#Connecting signals
	
		self.button_build()									#Building buttons 
		self.spin_button_build()							#Building spin-buttons 
		self.menu_build()									#Building menu 
		self.switch_build()									#Building switch 
		self.statusbar_build()								#Building statusbar 

		self.picture = PictureProcessing()					#Creating image object

		self.window = self.builder.get_object("window")		#Building main window
		self.window.show()									#Displaying main window 	

	def load_image(self, image, path):
		"""Loading image from file to widget"""							
		self.image = self.builder.get_object("preview_image") 
		self.image.set_from_file(path)	

	def on_window_destroy(self, object, data = None):
		"""Destroying main window"""
		print "Window destroyed: " + object.get_name()
		Gtk.main_quit()

	def on_quit_activate(self, menuitem, data = None):
		"""Exiting from program"""
		print "Quit pressed: " + menuitem.get_label()
		Gtk.main_quit()

	def error_dialog(self, widget, error_info):
		"""Displaying error message"""
		err_dialog = Gtk.MessageDialog(None, Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT, 
			Gtk.MessageType.ERROR,Gtk.ButtonsType.CANCEL, "Error")	#Creating error dialog									
		err_dialog.format_secondary_text(error_info)				#Adding error message
		print("Error occured")	
		err_dialog.run()									
		err_dialog.destroy()

	def statusbar_build(self):
		"""Building statusbar"""
		self.statusbar = self.builder.get_object("statusbar")
		self.statusbar_context_id = self.statusbar.get_context_id("Program starting")
		self.statusbar.push(self.statusbar_context_id, "Open image to start")		 #Displaying start message

	def menu_build(self):
		"""Building menu"""
		self.open = self.builder.get_object("open")
		self.save = self.builder.get_object("save")
		self.save_as = self.builder.get_object("save_as")
		self.about_dialog = self.builder.get_object("about_dialog")	
		self.save.set_sensitive(False)								#Turning save & save_as off  					
		self.save_as.set_sensitive(False)
		
	def spin_button_build(self):
		"""Building spinbuttons"""
		self.filter_spin_button = self.builder.get_object("filter_spinbutton")
		self.scale_spin_button = self.builder.get_object("scale_spinbutton")
		self.threshold_spin_button = self.builder.get_object("threshold_spinbutton")
		self.alphamax_spin_button = self.builder.get_object("alphamax_spinbutton")
		self.tolerance_spin_button = self.builder.get_object("tolerance_spinbutton")
		self.turdsize_spin_button = self.builder.get_object("turdsize_spinbutton")

	def switch_build(self):
		"""Building switch"""
		self.longcurve_switch = self.builder.get_object("longcurve_switch")						

	def button_build(self):
		"""Building buttons"""
		self.bitmap_button = self.builder.get_object("bitmap_button")
		self.trace_button = self.builder.get_object("trace_button")
		self.bitmap_button.set_sensitive(False)						#Turning bitmap & trace buttons until file will be opened
		self.trace_button.set_sensitive(False)

	def on_open_activate(self, widget, data = None):
		"""Opening image"""
		self.fcd = Gtk.FileChooserDialog("Open an image", None, Gtk.FileChooserAction.OPEN,			#Building file chooser dialog
				(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
		
		self.add_filters(self.fcd)								#Adding filters				

		response = self.fcd.run()								#Running file chooser dialog
		
		if response == Gtk.ResponseType.OK:						#Checking OK clicked
			print("Open clicked")
			print("File selected: " + self.fcd.get_filename())	

			self.picture.path = self.fcd.get_filename()			#Setting image path to choosed
		
			self.picture.convert_to("bmp")						#Converting image to BMP	

			self.load_image(self, self.picture.path)			#Displaying image

			self.picture.bitmapped = False						#Setting image bitmapped state to false 

			self.save.set_sensitive(True)						#Turning buttons & menu items to ON state
			self.save_as.set_sensitive(True)
			self.bitmap_button.set_sensitive(True)
			self.trace_button.set_sensitive(True)

			self.open_context_id = self.statusbar.get_context_id("File opening")	
			self.statusbar.push(self.open_context_id, "Image loaded")			#Displaying current state

			self.fcd.destroy()													#Destroying file chooser dialog
		elif response == Gtk.ResponseType.CANCEL:								#Checking CANCEL clicked
			print("Cancel clicked")
			self.fcd.destroy()													#Destroying file chooser dialog

	def add_filters(self, dialog):		
		"""Filters for FCD"""
		image_filter = Gtk.FileFilter()											
		image_filter.set_name("Image files")
		
		image_filter.add_mime_type("image/png")									#Adding mime type to filter
		image_filter.add_mime_type("image/jpg")
		image_filter.add_mime_type("image/jpeg")
		image_filter.add_mime_type("image/bmp")
		image_filter.add_mime_type("image/gif")

		image_filter.add_pattern("*.png")										#Adding reg exp to filter 
		image_filter.add_pattern("*.jpg")
		image_filter.add_pattern("*.jpeg")
		image_filter.add_pattern("*.bmp")
		image_filter.add_pattern("*.gif")

		self.extension_list = ["png", "jpg", "jpeg", "bmp", "gif"]				#List of compatible image extensions 		
																				##You could add more, if you could make PIL and extension friends	
		dialog.add_filter(image_filter)											#Adding filter to the dialog 

	
	def on_save_activate(self, menuitem, data = None):
		"""Saving current image"""
		print("Save clicked")
		self.picture.convert_to(None)											#Saving image
		saved_name = self.picture.path.split('/')[-1]							#Parsing saved name
		self.save_context_id = self.statusbar.get_context_id("File saving")		
		self.statusbar.push(self.save_context_id, "Image saved: " + saved_name) #Displaying saved name

	def on_save_as_activate(self, widget, data = None):
		"""Saving image as"""
		self.fcd = Gtk.FileChooserDialog("Save image", None, Gtk.FileChooserAction.SAVE,
				(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_SAVE, Gtk.ResponseType.OK))	#Building file chooser dialog
		
		response = self.fcd.run()												#Running file chooser dialog

		if self.fcd.get_filename() != None and self.fcd.get_filename().split('.')[-1] not in self.extension_list:	#Checking new image format
			self.error_dialog(self, "Unsupportable format.")
			self.fcd.destroy()

		elif response == Gtk.ResponseType.OK:									#Checking OK clicked
			print("Save as clicked")
			print("File selected: " + self.fcd.get_filename())

			self.saved_image = self.fcd.get_filename()							#Setting new image path to entered

			saved_as = self.saved_image.split('/')[-1].split('.')				#Parsing new image path 

			self.picture.save_image(saved_as[0], saved_as[1])					#Saving new image with new extension

			self.save_as_context_id = self.statusbar.get_context_id("File saving as...")
			self.statusbar.push(self.open_context_id, "Image saved as: " + saved_as[0]  
								+ '.' + saved_as[1])							#Displaying new image name

			self.fcd.destroy()													#Destroying file chooser dialog

		elif response == Gtk.ResponseType.CANCEL:								#Checking CANCEL clicked 
			print("Cancel clicked")
			self.fcd.destroy()													#Destroying file chooser dialog

	def option_toggled(self, widget):
		"""Change current output format"""
		if widget.get_active() == True:	 													#Checking button state	
			self.save_context_id = self.statusbar.get_context_id("Output format choosing")
			if Gtk.Buildable.get_name(widget) == "pdf_menu":								#Switch to PDF
				self.picture.trace_opt['-b']= "pdf"
				self.statusbar.push(self.save_context_id, "Output format: PDF")				#Displaying current output format
			if Gtk.Buildable.get_name(widget) == "postscript_menu":							
				self.picture.trace_opt['-b'] = "postscript"									#Switch to PostScript
				self.statusbar.push(self.save_context_id, "Output format: PostScript")
			if Gtk.Buildable.get_name(widget) == "svg_menu":	
				self.picture.trace_opt['-b'] = "svg"										#Switch to SVG													
				self.statusbar.push(self.save_context_id, "Output format: SVG")

	def on_about_activate(self, menuitem, data = None):
		#"""Displaying about information"""    
	    print("About selected")
	    self.response = self.about_dialog.run() #Running about dialog
	    self.about_dialog.hide()				#Hiding about dialog

	def on_bitmap_button_clicked(self, button, data = None):
		"""Making and collecting options for bitmap"""
		self.picture.bitmap_opt['-f'] = self.filter_spin_button.get_value()			#Getting values from spin buttons
		self.picture.bitmap_opt['-s'] = self.scale_spin_button.get_value_as_int()
		self.picture.bitmap_opt['-t'] = self.threshold_spin_button.get_value()
		self.picture.make_bitmap()													#Making bitmap
		self.load_image(self, self.picture.bitmap_path)								#Displaying bitmapped image
		self.make_bitmap_context_id = self.statusbar.get_context_id("Making bitmap")
		self.statusbar.push(self.open_context_id, "Image bitmapped: " 
							+ self.picture.bitmap_path.split('/')[-1])				#Displaying bitmapped image name
		self.picture.bitmapped = True 												#Setting bitmapped state to true	

	def on_trace_button_clicked(self, button, data = None):
		"""Tracing and collecting options"""
		if self.picture.trace_opt.has_key('-b') and self.picture.bitmapped:											#Cheking options dictionary for having output format value and having image bitmapped
			self.picture.trace_opt['-a'] = self.alphamax_spin_button.get_value()									#Collecting trace options
			self.picture.trace_opt['-O'] = self.tolerance_spin_button.get_value()
			self.picture.trace_opt['-t'] = self.turdsize_spin_button.get_value_as_int()
			self.picture.trace_bitmap()																				#Tracing image
			self.picture.output_path = self.picture.bitmap_path.split('.')[0] + '.' + self.picture.trace_opt['-b']	#Parsing output file name
			self.trace_bitmap_context_id = self.statusbar.get_context_id("Making trace")
			self.statusbar.push(self.open_context_id, "Bitmap traced: " + self.picture.output_path.split('/')[-1])	#Displaying traced file name
		elif self.picture.bitmapped == False:																		#Checking for image bimapped
			self.error_dialog(self, "Bitmap image before tracing.")													#Display error dialog
		else:
			self.error_dialog(self, "Choose export format before tracing.")											#Display error dialog
	def on_longcurve_switch_activate(self, switch, gparam):
		"""Setting longcurve option"""
		if self.longcurve_switch.get_active():				#Cheking for toggled switch 
			self.picture.trace_opt['-n'] = ''				#Add longcurve option to dictionary 
		else:
			self.picture.trace_opt.pop('-n', None)			#Remove longcurve option to dictionary 
					
if __name__ == "__main__":											
	main = MainWindow()
	Gtk.main()												#Starting program session