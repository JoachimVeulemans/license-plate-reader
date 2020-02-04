import cv2
import imageio
import sys
import requests
import time

if __name__ == '__main__':
	base_dir = ""
	camera_ip = "192.168.1.20"
	backend_url = "127.0.0.1:4000/upload"

	if (len(sys.argv) != 1 and len(sys.argv) != 3):
		print("Wrong number of arguments given. First argument is base directory, second argument is ip address of camera.")
		sys.exit(1)

	if len(sys.argv) == 3:
		base_dir = sys.argv[1]
		camera_ip = sys.argv[2]

	filename = base_dir + "images/camera_screen.jpg"

	cap = cv2.VideoCapture("rtsp://" + camera_ip + ":554/ucast/11")

	while cap.isOpened():
		try:
			ret, frame = cap.read()
			imageio.imsave(filename, frame)
			r = requests.post(url = backend_url, params = {'file': frame})
			data = r.json() 
			print(data)
		except ValueError:
			print("Camera feed error")
		time.sleep(1)
