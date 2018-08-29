from screen.utils import *
from screen.scrapers import TextFinder, ContourDetector, TemplateMatcher

# TODO: refactor these two. Looks same
def contours_with_distances(source_image, point):
    cd = ContourDetector()
    cd.initialize(source_image)

    for i, data in enumerate(cd.get_data()):
        area = data.get('area')
        data["distance"] = distance(
            area.get('center-x'), area.get('center-y'),
            point[0], point[1]
        )
        data['source'] = 'CD'
        data['offset'] = (point[0]-area.get('center-x'), point[1]-area.get('center-y'))
        yield data


def text_boxes_with_distances(source_image, point):
    tf = TextFinder()
    tf.initialize(source_image)

    for i, data in enumerate(tf.get_data()):
        area = data.get('area')
        data['distance'] = distance(
            area.get('center-x'), area.get('center-y'),
            point[0], point[1]
        )
        data['source'] = 'OCR'
        data['offset'] = (point[0]-area.get('center-x'), point[1]-area.get('center-y'))
        yield data

@with_screenshot_source
def get_screenshot_image(source_image):
    return source_image

def dump_screen_data(source_image, click_point):
    point = (click_point[0]/SCREENSHOT_SCALE, click_point[1]/SCREENSHOT_SCALE)

    boxes_by_dist = list(text_boxes_with_distances(source_image, point))
    contours_by_dist = list(contours_with_distances(source_image, point))

    all_data = {
        'source_image': source_image,
        'contours': contours_by_dist,
        'text-boxes': boxes_by_dist,
        'click-point': point
    }

    stamp = str(time.time())
    import pickle
    pickle.dump(all_data, open('tests/'+stamp+'.pickle', 'wb'))

    return stamp
