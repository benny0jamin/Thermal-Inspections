#!/usr/bin/python3
# EAR Controlled (EAR99)
# WARNING: This document contains technology subject to the Export Administration Regulations (EAR)
# (15 C.F.R. Sections 730-774).  Export or diversion contrary to law is prohibited.

import fnv
import fnv.reduce
import fnv.file
import sys
import os
import shlex


file_path = r'E:\2023\ScanPro\Jemalong\Jemalong 21st\A615'
try:
	im = fnv.file.ImagerFile(file_path)
except:
	print("A filename can be supplied as an argument.")

print("Type commands at the prompt, type 'help' for options.")

while True:
	args = shlex.split(input("> "))

	if len(args) == 0:
		continue

	if args[0].lower() == "quit" or args[0].lower() == "exit":
		break
	elif args[0].lower() == "help":
		print("quit/exit: exit the application");
		print("open <filename>: open a file.");
		print("close: close the file.");
		print("first: read the first frame.");
		print("firstsuperframe: read the first superframe.");
		print("next: read the next frame.");
		print("nextsuperframe: read the next superframe.");
		print("savecsv <out filename>: write currently read frame to a csv file.");
		print("unit: set the desired output units.");
		print("temptype: set the desired output temperature unit.");
		print("objpar: print the current object parameters.");
		print("emissivity: set the emissivity object parameter.");
		print("distance: set the distance object parameter.");
		print("resetobjpar: reset the object parameters to the values from the camera.");
		print("update: update the frame with any unit/object parameter changes.");
	elif args[0].lower() == "open":
		if len(args) == 2:
			im = fnv.file.ImagerFile(args[1])
		else:
			print("Usage is:")
			print("  open <filename>")
	elif args[0].lower() == "close":
		im.close()
		im = None
	elif args[0].lower() == "first":
		(frame, eof) = im.first_frame_number(fnv.Preset.ANY)
		if frame is not None:
			im.get_frame(frame)
			frameInfo = im.frame_info
			imageRoi = im.rois[0]
			print("Image min:", imageRoi.min_value)
			print("Image max:", imageRoi.max_value)
			print("Image mean:", imageRoi.mean)
			print("Preset:", frameInfo.preset)
			print("Frame Number:", frameInfo.frame)
			print("Time:", frameInfo.time)
	elif args[0].lower() == "firstsuperframe":
		(frame, eof) = im.first_frame_number(fnv.Preset.SUPERFRAME)
		if frame is not None:
			im.get_superframe(frame)
			frameInfo = im.frame_info
			imageRoi = im.rois[0]
			print("Image min:", imageRoi.min_value)
			print("Image max:", imageRoi.max_value)
			print("Image mean:", imageRoi.mean)
			print("Preset:", frameInfo.preset)
			print("Frame Number:", frameInfo.frame)
			print("Time:", frameInfo.time)
	elif args[0].lower() == "next":
		(frame, eof) = im.next_frame_number(im.frame_number, fnv.Preset.ANY)
		if frame is not None:
			im.get_frame(frame)
			frameInfo = im.frame_info
			imageRoi = im.rois[0]
			print("Image min:", imageRoi.min_value)
			print("Image max:", imageRoi.max_value)
			print("Image mean:", imageRoi.mean)
			print("Preset:", frameInfo.preset)
			print("Frame Number:", frameInfo.frame)
			print("Time:", frameInfo.time)
	elif args[0].lower() == "nextsuperframe":
		(frame, eof) = im.next_frame_number(im.frame_number, fnv.Preset.SUPERFRAME)
		if frame is not None:
			im.get_superframe(frame)
			frameInfo = im.frame_info
			imageRoi = im.rois[0]
			print("Image min:", imageRoi.min_value)
			print("Image max:", imageRoi.max_value)
			print("Image mean:", imageRoi.mean)
			print("Preset:", frameInfo.preset)
			print("Frame Number:", frameInfo.frame)
			print("Time:", frameInfo.time)
	elif args[0].lower() == "savecsv":
		if len(args) == 2:
			if im.has_frame:
				width = im.width
				height = im.height
				final = im.final
				with open(args[1], 'w') as f:
					for y in range(height):
						for x in range(width):
							if x != 0:
								f.write(",")
							f.write(str(final[y * width + x]))
						f.write("\n")
		else:
			print("Usage is:")
			print("savecsv <filename>")
	elif args[0].lower() == "unit":
		units = im.supported_units
		unit = im.unit
		print("Select a unit:")
		for i in range(len(units)):
			print(str(i) + ")", units[i], "(active)" if unit == units[i] else "")
		print(str(len(units)) + ") Cancel")
		sel = int(input("> "))
		if sel != len(units):
			im.unit = units[sel]
	elif args[0].lower() == "temptype":
		tempTypes = [fnv.TempType.CELSIUS, fnv.TempType.KELVIN, fnv.TempType.FAHRENHEIT, fnv.TempType.RANKINE]
		tempType = im.temp_type
		print("Select a temperature type:")
		for i in range(len(tempTypes)):
			print(str(i) + ")", tempTypes[i], "(active)" if tempType == tempTypes[i] else "")
		print(str(len(tempTypes)) + ") Cancel")
		sel = int(input("> "))
		if sel != len(tempTypes):
			im.temp_type = tempTypes[sel]
	elif args[0].lower() == "objpar":
		objPar = im.object_parameters

		print("emissivity: {0:0.3f}".format(objPar.emissivity))
		print("reflected temp: {0:0.2f}".format(objPar.reflected_temp))
		print("distance: {0:0.2f}".format(objPar.distance))
		print("atmosphere temp: {0:0.2f}".format(objPar.atmosphere_temp))
		print("relative humidity: {0:0.2f}".format(objPar.relative_humidity * 100))
		print("transmission: {0:0.3f}".format(objPar.atmospheric_transmission))
	elif args[0].lower() == "emissivity":
		if len(args) == 2:
			objPar = im.object_parameters
			objPar.emissivity = float(args[1])
			im.object_parameters = objPar
		else:
			print("Usage is:")
			print("emissivity <value 0 to 1>")
	elif args[0].lower() == "distance":
		if len(args) == 2:
			objPar = im.object_parameters
			objPar.distance = float(args[1])
			im.object_parameters = objPar
		else:
			print("Usage is:")
			print("emissivity <value in meters>")
	elif args[0].lower() == "resetobjpar":
		im.reset_object_parameters()
	elif args[0].lower() == "update":
		if im.update_frame():
			imageRoi = im.rois[0]
			print("Image min:", imageRoi.min_value)
			print("Image max:", imageRoi.max_value)
			print("Image mean:", imageRoi.mean)
