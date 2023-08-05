# ---------------------------------------------------------------------------------
# 	QVisaDeviceSelect -> QWidget
#	Copyright (C) 2019 Michael Winters
#	github: https://github.com/mesoic
#	email:  mesoic@protonmail.com
# ---------------------------------------------------------------------------------
#	
#	Permission is hereby granted, free of charge, to any person obtaining a copy
#	of this software and associated documentation files (the "Software"), to deal
#	in the Software without restriction, including without limitation the rights
#	to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#	copies of the Software, and to permit persons to whom the Software is
#	furnished to do so, subject to the following conditions:
#	
#	The above copyright notice and this permission notice shall be included in all
#	copies or substantial portions of the Software.
#	
#	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#	IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#	FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#	AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#	LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#	OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#	SOFTWARE.
#

#!/usr/bin/env python 
# -*- coding: utf-8 -*-

# Import QT backends
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QComboBox, QLabel

# Helper class to generate and interact with initialized QVisaDevice objects
class QVisaDeviceSelect(QWidget):

	def __init__(self, _app):

		# Extends QWidget
		QWidget.__init__(self)

		# Inst widget and layout
		self._layout = QVBoxLayout()

		# Cache reference to _app for callback
		self._app = _app 

		# List of registered names
		self._registered = []

		# Widget label and comboBox
		self._select = QComboBox()
		self._select.currentTextChanged.connect(self._run_callback)
		
		# Widget select add items
		if _app.get_device_names() is not None:
			self._select.addItems( _app.get_device_names() )

		# Add widgets to layout
		self._layout.addWidget(self._select)
		self._layout.setContentsMargins(0,0,0,0)

		# Set layout
		self.setLayout(self._layout)

		# Callback function on text changed
		self._callback = None

	# Method to sync instrument widget to app
	def refresh(self, _app):
	
		# Get current list of names registered to app
		for _name in _app.get_device_names():
			
			# If name is not registered
			if self.isRegistered(_name) == False:
	
				# Add it to the combobox	
				self._select.addItem(_name)	
				self._registered.append(_name)

	# Register insturment by name
	def registerInst(self, _name):
		self._select.addItem(_name)
		self._registered.append(_name)
	
	# CHeck if name has been registered		
	def isRegistered(self, _name):
		return True if _name in self._registered else False

	# Wrapper method for currentText	
	def currentText(self):
		return self._select.currentText()
	
	# Wrapper method for setEnabled 	
	def setEnabled(self, _bool):
		self._select.setEnabled(_bool)

	# Wrapper method for blockSignals	
	def blockSignals(self, _bool):
		self._select.blockSignals(_bool)

	# Wrapper method for setFixedWidth
	def setFixedWidth(self, _width):
		self._select.setFixedWidth(int(_width))

	# Expose textChanged slot
	def set_callback(self, __func__):	
		self._callback = str(__func__)	

	# Run the callback	
	def _run_callback(self):
		if self._callback is not None:					
			__func__ = getattr(self._app, self._callback)
			__func__()