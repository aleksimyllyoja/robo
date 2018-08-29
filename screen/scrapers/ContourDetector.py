import cv2
import numpy as np
from math import sqrt

from screen.scrapers import Scraper
from screen.utils import *

class ContourDetector(Scraper):
    """
    https://docs.opencv.org/3.1.0/d3/dc0/group__imgproc__shape.html#ga17ed9f5d79ae97bd4c7cf18403e1689a

    https://docs.opencv.org/3.4.0/d9/d8b/tutorial_py_contours_hierarchy.html
    """

    def preprocess(self):
        # TODO: no magic numbers

        self.source_image = cv2.cvtColor(self.source_image, cv2.COLOR_BGR2GRAY)
        self.source_image = cv2.bilateralFilter(self.source_image, 10, 20, 20)
        self.source_image = cv2.Canny(self.source_image, 10, 100)


    def get_data(self, limit=None):
        # TODO: no magic numbers
        image, contours, hierarchy = cv2.findContours(self.source_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Filter by min and max area
        #def area_filter(c):
        #    a = cv2.contourArea(c)
        #    return a >= 10 and a <= 100

        #def hierarchy_level(i):
        #    if hierarchy[0][i][3] == -1:
        #        return 0
        #    else:
        #        return hierarchy_level(hierarchy[0][i][3])+1

        #contours = list(filter(area_filter, contours))[:limit]
        #print(len(hierarchy[0]))
        for i, contour in enumerate(contours):

            #if cv2.contourArea(contour) < 100: # under 10 px^2
            #    continue

            #level_next, previous, child, parent = hierarchy[0][i]
            #if hierarchy_level(i) > 2:
            #    continue

            #print(hierarchy_level(i))

            #if parent != -1:
            #    continue

            peri = cv2.arcLength(contour, True)
            #approx = cv2.approxPolyDP(contour, 0.015 * peri, True)
            x, y, w, h = cv2.boundingRect(contour)
            yield {
                #'contour': contour,
                #'approximation': approx,
                'area': {
                    'x': x,
                    'y': y,
                    'w': w,
                    'h': h,
                    'center-x': x+w/2,
                    'center-y': y+h/2
                }
            }
