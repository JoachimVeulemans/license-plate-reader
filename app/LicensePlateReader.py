import numpy as np
import cv2
import imutils
import pytesseract
import time
import imageio
import re


class LicensePlateReader:
	def __init__(self):
		pass

	@staticmethod
	def get_license_plate_text(file):
		# Read image in color
		img = cv2.imread(file, cv2.IMREAD_COLOR)

		# Resize image so why can use different formats of images with the same code
		img = cv2.resize(img, (620, 480))

		# Convert image to grey scale
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

		# Blur image in order to reduce noise
		gray = cv2.bilateralFilter(gray, 11, 17, 17)

		# Execute Canny to do edge detection
		edged = cv2.Canny(gray, 30, 200)

		# Find contours
		cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)
		cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]
		screen_cnt = None

		# Loop over our contours
		for c in cnts:
			# Approximate the contour
			peri = cv2.arcLength(c, True)
			approx = cv2.approxPolyDP(c, 0.018 * peri, True)

			# Let's say when it has 4 corners, we have found the license
			if len(approx) == 4:
				screen_cnt = approx
				break

		if screen_cnt is None:
			# No license found
			return "No license found"
		else:
			# License found
			cv2.drawContours(img, [screen_cnt], -1, (0, 255, 0), 3)

			# Make everything around the license black
			mask = np.zeros(gray.shape, np.uint8)
			blacked_img = cv2.drawContours(mask, [screen_cnt], 0, 255, -1,)
			blacked_img = cv2.bitwise_and(img, img, mask=mask)

			# Crop image
			(x, y) = np.where(mask == 255)
			(topx, topy) = (np.min(x), np.min(y))
			(bottomx, bottomy) = (np.max(x), np.max(y))
			cropped = gray[topx:bottomx+1, topy:bottomy+1]

			# Convert image to text through tesseract
			# https://stackoverflow.com/questions/44619077/pytesseract-ocr-multiple-config-options
			text = pytesseract.image_to_string(cropped, config='--psm 11')

			# ######################################
			# #### Uncomment below for testing #####
			# ######################################
			"""
			cv2.imshow('Original', img)
			cv2.imshow('Blacked', blacked_img)
			cv2.imshow('Cropped', cropped)
			cv2.waitKey(0)
			cv2.destroyAllWindows()
			"""

			text = text.lower().replace("\n", "")
			text = re.sub('[^a-z0-9.]', '', text)

			if text == "":
				text = "No license found"

			return text


if __name__ == '__main__':
	filename = "/home/license/images/camera_screen.jpg"
	camera_ip = "192.168.1.20"

	# ######################################
	# #### Uncomment below for testing #####
	# ######################################
	"""
	filename = "/home/license/images/image.jpg"
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
