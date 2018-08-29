import cv2
import settings

from screen.scrapers import Scraper
from screen.utils import *

class TemplateMatcher(Scraper):

    def initialize(self, source_image, template_image, *args, **kwargs):
        self.template_image = template_image

        super(TemplateMatcher, self).initialize(source_image, *args, **kwargs)

    def preprocess(self):
        self.image = cv2.cvtColor(
            self.source_image,
            cv2.COLOR_BGR2GRAY
        )

        self.template_image = cv2.cvtColor(self.template_image, cv2.COLOR_BGR2GRAY)

    def best_correlation_and_location(self, scale=1):
        #template = cv2.resize(self.template_image, (0, 0), fx=scale, fy=scale)
        result = cv2.matchTemplate(self.image, self.template_image, cv2.TM_CCOEFF_NORMED)

        width, height = self.template_image.shape[::-1]
        (_, correlation, _, location) = cv2.minMaxLoc(result)

        return (correlation, scale, location, width, height)

    def get_data(self, *args, **kwargs):
        correlation, scale, location, width, height = self.best_correlation_and_location()

        area_x = location[0]
        area_y = location[1]
        area_w = width
        area_h = height

        return {
            'correlation': correlation,
            'area': {
                'x': area_x,
                'y': area_y,
                'w': area_w,
                'h': area_h,
                'center-x': area_x+area_w/2,
                'center-y': area_y+area_h/2,
            }
        }
