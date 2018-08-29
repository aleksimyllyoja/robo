import logging
import sys
import pickle
from pathlib import Path

import settings

from screen.interpreter import *
from screen.debug import *
from operations import *

class RobotNotFoundException(Exception):
    pass

def run_robot(name):
    from state import save_ok_state
    logging.info("Starting %s" % name)

    try:
        # TODO: think this
        exec(open(settings.ROBOTS_DIRECTORY+"/"+name+"/main.py").read())
    except KeyboardInterrupt:
        logging.info("User interrupted")
        sys.exit(0)
    else:
        if not settings.STATELESS:
            logging.info("Saving all-clear state")

        save_ok_state()

    logging.info("Done.")

def load_and_run_robot(name):
    try:
        load_robot(name)
    except RobotNotFoundException as enfe:
        logging.error(enfe)
        settings.debug.print_known_robots()
    except Exception as e:
        logging.error(e)
        raise
    else:
        run_robot(name)

def load_template_mapping(robot_name):
    try:
        mapping = pickle.load(
            open(settings.ROBOT_DIRECTORY+"/"+settings.TEMPLATE_DIR+"/mapping.pickle", "rb")
        )
    except:
        return {}
    else:
        return dict(
            map(lambda x: (
                x.get("state_key"),
                x.get("filename")
            ),
            mapping
        ))

def load_environment_settings(robot_settings_module):
    [
        setattr(settings, setting, value)
        for setting, value in robot_settings_module.__dict__.items()
            if not callable(getattr(robot_settings_module, setting))
            and not setting.startswith("__")
    ]

def try_load_robot_settings_module(robot_name):
    try:
        return __import__(
            "%s.settings" % robot_name,
            globals(),
            locals(),
            ['*']
        )

    except ImportError:
        logging.info("No robot specific settings")
        #raise RobotNotFoundException(
        #    "Couldn't load a robot named %s" % robot_name
        #)

def load_robot(robot_name):
    sys.path.append(settings.ROBOTS_DIRECTORY)

    settings.ROBOT_DIRECTORY = settings.ROBOTS_DIRECTORY + robot_name + "/"
    settings.STATEFILE = settings.ROBOT_DIRECTORY+settings.STATE_DIR+"/"+settings.STATEFILENAME
    #settings.TEMPLATE_MAPPING = load_template_mapping(robot_name)

    sys.path.append(settings.ROBOT_DIRECTORY)

    logging.basicConfig(
        #filename = settings.ROBOT_DIRECTORY+"logs/log.txt",
        format = settings.LOGGING_FORMAT,
        level = logging.DEBUG if settings.VERBOSE else logging.INFO,
        handlers = [
            logging.StreamHandler(sys.stdout)
        ]
    )

    logging.info("Loaded robot named %s", robot_name)

    robot_settings_module = try_load_robot_settings_module(robot_name)
    if robot_settings_module:
        load_environment_settings(robot_settings_module)
