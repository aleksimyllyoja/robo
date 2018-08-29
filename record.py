from pynput import keyboard
from pynput import mouse

from queue import Queue

import os, time, sys
import itertools

import threading

from screen.dump import dump_screen_data, get_screenshot_image

from runner import *

lock = False
loading = False
click_queue = Queue()
save_queue = Queue()

saved = []

save_index = 0

def animate():
    global lock, loading, saved

    for c in itertools.cycle(['|', '/', '-', '\\']):
        if not lock:
            break

        ind = str(save_queue.qsize()) if save_queue.qsize() > 1 else ''
        sys.stdout.write('\r# ' + c + ' '+ind)
        sys.stdout.flush()
        time.sleep(0.1)

    loading = False
    sys.stdout.flush()
    sys.stdout.write('\r')

def save(save_index):
    global saved

    source_image = get_screenshot_image()

    while click_queue.empty():
        time.sleep(0.1)

    else:
        (x, y) = click_queue.get()
        time.sleep(2)
        #print('\n', save_index, (x, y))

        model_name = dump_screen_data(source_image, (x, y))
        saved.insert(save_index, "click('"+model_name+"')")

        save_queue.get()

def on_click(x, y, button, pressed):
    global lock

    if lock:
        click_queue.put((x, y))
        lock = False

def on_move(x, y):
    global lock, loading, save_index

    if not lock:
        lock = True

        if not loading:
            loading = True
            animation_thread = threading.Thread(target=animate)
            animation_thread.start()

        save_queue.put("save")
        save_index += 1

        thread = threading.Thread(target = save, args=(save_index, ))
        thread.start()

try:
    with mouse.Listener(on_click=on_click, on_move=on_move) as listener:
        print("# READY\n")
        listener.join()

except KeyboardInterrupt:
    print("")
    print("\n".join(saved))
    sys.exit(0)
