import time
import os
import pyautogui
import logging
import cv2
import tempfile
from math import sqrt

import settings

from mss import mss

class TargetNotFound(Exception):
    pass

def screenshot():
    return mss().shot(
        output=tempfile.gettempdir()+"/"+str(time.time())+".png"
    )

def screenshot_dimensions():
    shot = screenshot()
    img = cv2.imread(shot)
    return img.shape[1::-1]

RESOLUTION = pyautogui.size()
logging.debug("Detected screen resolution %sx%s" % RESOLUTION)

SCREENSHOT_RESOLUTION = screenshot_dimensions()
logging.debug("Detected screenshot resolution %sx%s" % SCREENSHOT_RESOLUTION)

TEMPLATE_RESOLUTION = (3840, 2400) ## TODO: move to template mapping!!!

SCREENSHOT_SCALE = float(RESOLUTION[0])/float(SCREENSHOT_RESOLUTION[0])

def distance(x1, y1, x2, y2):
    return sqrt((x2-x1)**2+(y2-y1)**2)

def with_screenshot_source(predicate):
    def __w(*args, **kwargs):
        screen = screenshot()
        screen_image = cv2.imread(screen)
        try:
            return predicate(source_image=screen_image, *args, **kwargs)
        except:
            raise
        finally:
            os.remove(screen)

    return __w

# TODO: logging here
def attempt(predicate, _time_limit=20, _wait=0.5, *args, **kwargs):
    success = False
    t0 = t1 = time.time()

    while not success and (t1-t0) <= _time_limit:
        try:
            return_value = predicate(*args, **kwargs)
        except TargetNotFound:
            time.sleep(_wait)
        else:
            success = True
            break
        finally:
            t1 = time.time()

    if success:
        return return_value
    else:
        raise TargetNotFound
