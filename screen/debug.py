import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, PathPatch, Circle
from matplotlib.path import Path

from screen.utils import *
from screen.scrapers import TemplateMatcher

import pickle

from pprint import pprint

sbd = lambda xs: sorted(xs, key = lambda x: x.get('distance'))

@with_screenshot_source
def debug(name, source_image=None, magic_range=8, dataset='contours'):
    data = pickle.load(open("tests/"+name+".pickle", "rb"))

    data_source_image = data.get('source_image')

    original_x, original_y = data.get('click-point')

    print(original_x, original_y)

    clicks = []

    screen_background = source_image.copy()

    #all_boxes = data.get('text-boxes')+data.get('contours')

    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))

    ax[0].imshow(data_source_image)

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

        area = tm_data.get('area')

        cx = area.get('center-x')+ct.get('offset')[0]
        cy = area.get('center-y')+ct.get('offset')[1]

        tx = int(area.get('x'))
        ty = int(area.get('y'))
        tw = int(area.get('w'))
        th = int(area.get('h'))

        screen_background[ty:+ty+th, tx:tx+tw] = template_image

        ax[0].add_patch(
            Rectangle(
                (x, y), w, h,
                edgecolor='red', fill=False
            )
        )

        ax[1].add_patch(
            Rectangle(
                (tx, ty), tw, th,
                edgecolor='blue', fill=False
            )
        )
        clicks.append((cx, cy))

    clicks_and_counts = sorted(
        list(set([(c, clicks.count(c)) for c in clicks])),
        key = lambda x: x[1]
    )

    for ((cx, cy), count) in clicks_and_counts:
        ax[1].text(cx, cy, str(count), color='red')
        ax[1].add_patch(
            Circle(
                (cx, cy), 4,
                color='green'
            )
        )

    ax[1].imshow(screen_background)

    ax[0].add_patch(
        Circle(
            (int(original_x), int(original_y)), 5,
            color='green'
        )
    )

    plt.tight_layout()
    plt.show()
