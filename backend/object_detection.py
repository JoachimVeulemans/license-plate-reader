from vehicle import Vehicle
from lp import LP
import cv2
import numpy as np
from src.label import Label, lwrite
from src.keras_utils import load_model, detect_lp
from src.utils import im2single, nms
from src.label import dknet_label_conversion, Shape


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
        R, boxes, confidences, class_ids = self.vehicle.detect_objects(img, str(filename).split('.')[0] + '.txt')

        if len(R):
            WH = np.array(img.shape[1::-1], dtype=float)
            Lcars = []
            
            for i, r in enumerate(R):
                cx, cy, w, h = (np.array(boxes[i])/np.concatenate((WH, WH))).tolist()
                tl = np.array([cx - w/2., cy - h/2.])
                br = np.array([cx + w/2., cy + h/2.])
                label = Label(0, tl, br)
                Lcars.append(label)
                cv2.imwrite('%s/%s-car.png' % (self.output_dir, filename), img)
            lwrite('%s/%s-car.txt' % (self.output_dir, filename), Lcars)

    def detect_debug(self, img, filename):
        self.detect_vehicle(img, filename)
        return self.detect_lp(img, filename)

    def detect_lp(self, img, filename):
        ratio = float(max(img.shape[:2])) / min(img.shape[:2])
        side = int(ratio*288.)
        bound_dim = min(side + (side % (2**4)), 608)

        Llp, LlpImgs, _ = detect_lp(self.wpod_net, im2single(img), bound_dim, 2**4, (240, 80), self.lp_threshold)

        if len(LlpImgs):
            Ilp = LlpImgs[0]
            Ilp = cv2.cvtColor(Ilp, cv2.COLOR_BGR2GRAY)
            Ilp = cv2.cvtColor(Ilp, cv2.COLOR_GRAY2BGR)

            s = Shape(Llp[0].pts)

            cv2.imwrite('%s/%s-lp.png' % (self.output_dir, filename), Ilp*255.)

        # LP OCR
        R, idxs, boxes, confidences, class_ids = self.lp.detect_objects(Ilp*255., filename)

        print('\t\t%d lps found' % len(R))
        
        if len(R):
            L = dknet_label_conversion(R, 240, 80)
            L = nms(L, .45)
            L.sort(key=lambda x: x.tl()[0])
            lp_str = ''.join([chr(l.cl()) for l in L])
            return lp_str
        
        return "No license found"
