import numpy as np
import cv2
import imutils
import pytesseract
import time
import imageio
import re
import sys


if __name__ == '__main__':
	base_dir = ""
	camera_ip = "192.168.1.20"

	if (len(sys.argv) != 1 and len(sys.argv) != 3):
		print("Wrong number of arguments given. First argument is base directory, second argument is ip address of camera.")
		sys.exit(1)

	if len(sys.argv) == 3:
		base_dir = sys.argv[1]
		camera_ip = sys.argv[2]

	filename = base_dir + "images/camera_screen.jpg"

	# ######################################
	# #### Uncomment below for testing #####
	# ######################################
	"""
	filename = base_dir + "images/image.jpg"
	print(LicensePlateReader.get_license_plate_text(filename))
	"""

	cap = cv2.VideoCapture("rtsp://" + camera_ip + ":554/ucast/11")

	while cap.isOpened():
		try:
			ret, frame = cap.read()
			imageio.imsave(filename, frame)
			print(LicensePlateReader.get_license_plate_text(filename))
		except ValueError:
			print("No license found")
		time.sleep(1)
