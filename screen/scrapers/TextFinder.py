import cv2
import tesserocr as tr
from PIL import Image

import settings

from screen.scrapers import Scraper
from screen.utils import *

class TextFinder(Scraper):

    PREPROCESS_SCALE = 1.5

    def preprocess(self):
        self.source_image = cv2.resize(self.source_image, (0, 0), fx=self.PREPROCESS_SCALE, fy=self.PREPROCESS_SCALE)
        self.source_image = Image.fromarray(cv2.cvtColor(self.source_image, cv2.COLOR_BGR2RGB))

    def get_data(self, ril=tr.RIL.WORD):
        with tr.PyTessBaseAPI() as api:
            api.SetImage(self.source_image)

            line_boxes = api.GetComponentImages(ril, True)

            for i, (im, box, _, _) in enumerate(line_boxes):

                x, y = box['x'], box['y']
                w, h = box['w'], box['h']

                #api.SetRectangle(x-r, y-r, w+2*r, h+2*r)
                #conf = api.MeanTextConf()
                #text = api.GetUTF8Text()

                #if not text:
                #    continue

                area_x = x/self.PREPROCESS_SCALE
                area_y = y/self.PREPROCESS_SCALE
                area_w = w/self.PREPROCESS_SCALE
                area_h = h/self.PREPROCESS_SCALE

                if area_w*area_h <= 64: # 64 px^2
                    continue

                yield {
                    #'text': text,
                    #'image': im,
                    'area': {
                        'x': area_x,
                        'y': area_y,
                        'w': area_w,
                        'h': area_h,
                        'center-x': area_x+area_w/2,
                        'center-y': area_y+area_h/2,
                    }
                }
