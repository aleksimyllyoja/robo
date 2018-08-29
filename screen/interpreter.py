import pickle

from screen.scrapers import TemplateMatcher
from screen.utils import with_screenshot_source, SCREENSHOT_SCALE

import pyautogui

sbd = lambda xs: sorted(xs, key = lambda x: x.get('distance'))

@with_screenshot_source
def click(name, source_image=None, magic_range=8, dataset='contours'):
    data = pickle.load(open("tests/"+name+".pickle", "rb"))

    data_source_image = data.get('source_image')

    clicks = []

    #all_boxes = data.get('text-boxes')+data.get('contours')

    for ct in sbd(data.get(dataset))[:magic_range]:
        ct_area = ct.get('area')

        x = int(ct_area.get('x'))
        y = int(ct_area.get('y'))
        w = int(ct_area.get('w'))
        h = int(ct_area.get('h'))

        template_image = data_source_image[y:y+h, x:x+w]

        tm = TemplateMatcher()
        tm.initialize(source_image, template_image)
        tm_data = tm.get_data()

        #print(ct.get('distance'), tm_data.get('correlation'), w, h, w*h)

        area = tm_data.get('area')

        cx = area.get('center-x')+ct.get('offset')[0]
        cy = area.get('center-y')+ct.get('offset')[1]

        clicks.append((cx, cy))

    clicks_and_counts = sorted(
        list(set([(c, clicks.count(c)) for c in clicks])),
        key = lambda x: -x[1]
    )

    (cx, cy), c = clicks_and_counts[0]
    print("VOTES: ", c)

    pyautogui.click(cx*SCREENSHOT_SCALE, cy*SCREENSHOT_SCALE)
