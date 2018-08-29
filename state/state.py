import settings
import inspect
import logging
import pickle

from pathlib import Path

def save_state(state):
    path = Path(settings.STATEFILE)
    # TODO
    try:
        pickle.dump(state, open(path, 'wb'))
    except FileNotFoundError:
        pass

save_ok_state = lambda : save_state({})

def read_state():
    try:
        return pickle.load(open(settings.STATEFILE, 'rb'))
    except IOError:
        logging.info("Creating a new state")
        return {}

def autokey(predicate, *args, **kwargs):
    caller_frame = inspect.stack()[2][0]
    frameinfo = inspect.getframeinfo(caller_frame)
    caller_name = frameinfo.code_context[0].split("(")[0].strip()

    return "-".join(filter(None, [
        caller_name.strip(),
        str(args[0]) if args else ""
    ]))
