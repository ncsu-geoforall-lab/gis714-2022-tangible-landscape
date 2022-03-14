#!/usr/bin/env python3

import os

import grass.script as gs


def run_viewshed(scanned_elev, env, **kwargs):
    coordinates = [638830, 220150]
    gs.run_command('r.viewshed', input=scanned_elev, output='viewshed', coordinates=coordinates, observer_elevation=2, flags='b', env=env)


def main():
    env = os.environ.copy()
    env["GRASS_OVERWRITE"] = "1"
    elevation = "elev_lid792_1m"
    
    run_viewshed(scanned_elev=elevation, env=env)


if __name__ == "__main__":
    main()
