import cv2
import imageio
import sys
import requests
import time

if __name__ == '__main__':
	camera_ip = "192.168.1.200"
	backend_url = "127.0.0.1:4000/upload"
	pi_url = "192.168.1.7:8080/garage"

	if (len(sys.argv) != 1 and len(sys.argv) != 2):
		print("Wrong number of arguments given. First argument is ip address of camera.")
		sys.exit(1)

	if len(sys.argv) == 2:
		camera_ip = sys.argv[1]

	filename = "camera_screen.jpg"
	cap = cv2.VideoCapture("rtsp://" + camera_ip + ":554/ucast/11")

	while cap.isOpened():
		try:
			ret, frame = cap.read()
			imageio.imsave(filename, frame)
			r = requests.post(url = backend_url, params = {'file': frame})
			data = r.json() 
			print(data)
			if data == "LICENSE":
				r = requests.get(url = pi_url)
				data = r.json() 
				print(data)
				time.sleep(10)
		except ValueError as e:
			print(e)
		time.sleep(1)
