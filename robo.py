# -*- coding: utf-8 -*-

import argparse
import settings
import os

from runner import *

logo = """

                       88
                       88
                       88
8b,dPPYba,  ,adPPYba,  88,dPPYba,   ,adPPYba,
88P'   "Y8 a8"     "8a 88P'    "8a a8"     "8a
88         8b       d8 88       d8 8b       d8
88         "8a,   ,a8" 88b,   ,a8" "8a,   ,a8"
88          `"YbbdP"'  8Y"Ybbd8"'   `"YbbdP"'


"""

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        usage="\n\t run robot: robo [robot name] \n\t get help: robo -h "
    )

    parser.add_argument(
        'robot',
        type=str,
        help="robot's name"
    )
    parser.add_argument(
        '-s', '--save-state',
        help="save state",
        action='store_true'
    )
    parser.add_argument(
        '-f', '--fake',
        help="fake all operations",
        action='store_true'
    )
    parser.add_argument(
        '-v', '--verbose',
        help="DEBUG log",
        action='store_true'
    )

    parser.add_argument(
        '-c', '--create',
        help="create a new robot",
        action='store_true'
    )

    parser.add_argument(
        '-e', '--edit',
        help="create a new robot",
        action='store_true'
    )

    print(logo)
    ### TODO Refactor this into main() tms
    try:
        args = parser.parse_args()

    except:
        settings.debug.print_known_robots()

    else:
        settings.VERBOSE = args.verbose
        settings.STATELESS = not args.save_state
        settings.FAKE = args.fake

        # TODO: refactor this
        ## Experim.
        if args.create:
            if args.robot in settings.debug.known_robots():
                print("nope")
                die

            else: # TODO refactor somewhere
                print("Creating a new robot")
                robodir = settings.ROBOTS_DIRECTORY+"/"+args.robot
                os.mkdir(robodir)
                f = open(robodir+"/main.py", 'w+')
                f.close()

                import subprocess
                subprocess.call(['nano', robodir+"/main.py"])

                # TODO: factor.create_new_robot(name)

        if args.edit:
            import subprocess
            robodir = settings.ROBOTS_DIRECTORY+"/"+args.robot
            subprocess.call(['nano', robodir+"/main.py"])
        else:
            load_and_run_robot(args.robot)
