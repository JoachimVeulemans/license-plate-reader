from vehicle import Vehicle
from lp import LP
import cv2
import numpy as np
from src.label import Label, lwrite
from src.keras_utils import load_model, detect_lp
from src.utils import im2single, nms
from src.label import dknet_label_conversion, Shape
import time
import datetime

class Detector:
    def __init__(self):
        self.path_images = "."
        path_yolo = './'
        self.output_dir = './tmp/'
        self.vehicle = Vehicle(path_yolo)
        self.lp = LP(path_yolo)

        wpod_net_path = "models/wpod-net_update1.h5"
        self.wpod_net = load_model(wpod_net_path)
        self.lp_threshold = .5

    
    def detect_vehicle(self, img, filename):
        data = []
        copy = img
        R, boxes, confidences, class_ids = self.vehicle.detect_objects(copy, str(filename).split('.')[0] + '.txt')

        if len(R):
            WH = np.array(copy.shape[1::-1], dtype=float)
            Lcars = []
            
            for i, r in enumerate(R):
                cx, cy, w, h = (np.array(boxes[i])/np.concatenate((WH, WH))).tolist()
                tl = np.array([cx - w/2., cy - h/2.])
                br = np.array([cx + w/2., cy + h/2.])
                label = Label(0, tl, br)
                Lcars.append(label)
                data.append((cx, cy, w, h))
                cv2.imwrite('%s/%s-car.png' % (self.output_dir, filename), copy)
            lwrite('%s/%s-car.txt' % (self.output_dir, filename), Lcars)

        return data
    

    def detect_debug(self, img, filename):
        start = time.time()
        labels = self.detect_vehicle(img, filename)
        end = time.time()
        print("Vehicle detection took {:.6f} seconds".format(end - start) + " " + str(datetime.datetime.now()))
        licenses = []

        for i, car in enumerate(labels):
            cx = int(car[0] * img.shape[1])
            cy = int(car[1] * img.shape[0])
            w = int(car[2] * img.shape[1])
            h = int(car[3] * img.shape[0])
            cropped = img[cy:cy + h, cx:cx + w]
            cv2.imwrite('%s/%s-car-%s.png' % (self.output_dir, filename, str(i)), cropped)
            start = time.time()
            licenses.append(self.detect_lp(cropped, filename, i))
            end = time.time()
            print("LP detection took {:.6f} seconds".format(end - start) + " " + str(datetime.datetime.now()))

        return licenses

    def detect_lp(self, img, filename, i):
        ratio = float(max(img.shape[:2])) / min(img.shape[:2])
        side = int(ratio*288.)
        bound_dim = min(side + (side % (2**4)), 608)

        Llp, LlpImgs, _ = detect_lp(self.wpod_net, im2single(img), bound_dim, 2**4, (240, 80), self.lp_threshold)
        if len(LlpImgs):
            Ilp = LlpImgs[0]
            Ilp = cv2.cvtColor(Ilp, cv2.COLOR_BGR2GRAY)
            Ilp = cv2.cvtColor(Ilp, cv2.COLOR_GRAY2BGR)

            s = Shape(Llp[0].pts)

            cv2.imwrite('%s/%s-lp-%s.png' % (self.output_dir, filename, i), Ilp*255.)

            # LP OCR
            R, idxs, boxes, confidences, class_ids = self.lp.detect_objects(Ilp*255., filename)

            print('\t\t%d lps found' % len(R))
            
            if len(R):
                L = dknet_label_conversion(R, 240, 80)
                L = nms(L, .45)
                L.sort(key=lambda x: x.tl()[0])
                lp_str = ''.join([chr(l.cl()) for l in L])
                if (len(lp_str) <= 3):
                    return "No license found"
                return lp_str
        
        return "No license found"
