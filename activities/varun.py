#!/usr/bin/env python3

import os

import grass.script as gs


def run_lake(scanned_elev, env, **kwargs):
    coordinates = [638830, 220150]
    res = gs.raster_what(map=scanned_elev, coord=[coordinates])
    elev_value = float(res[0][scanned_elev]['value'])
    gs.run_command('r.lake', elevation=scanned_elev, lake='output_lake',
                   coordinates=coordinates, water_level=elev_value + 5, env=env)


def main():
    env = os.environ.copy()
    env["GRASS_OVERWRITE"] = "1"
    elevation = "elev_lid792_1m"
    elev_resampled = "elev_resampled"
    gs.run_command("g.region", raster=elevation, res=4, flags="a", env=env)
    gs.run_command("r.resamp.stats", input=elevation, output=elev_resampled, env=env)

    run_lake(scanned_elev=elev_resampled, env=env)


if __name__ == "__main__":
    main()
