#!/usr/bin/env python3

import os

import grass.script as gs


def run_aspect_class(scanned_elev, env, **kwargs):
    gs.run_command("r.slope.aspect", elevation=scanned_elev, aspect="aspect_val", 
                   min_slope=8.0, flags="n", env=env)
    # reclassify using rules passed as a string to standard input
    # 0:22.5:1 means reclassify interval 0 to 22.5 percent of aspect to category 1 
    rules = ['0:22.5:1', '22.5:67.5:1', '67.5:292.5:NULL', '292.5:337.5:1', '337.5:360:1', '*:-9999:NULL']
    gs.write_command('r.recode', input='aspect_val', output='aspect_class',
                          rules='-', stdin='\n'.join(rules), env=env)
    # set new color table: blue - white
    gs.run_command('r.colors', map='aspect_class', color='wave', env=env)


def main():
    env = os.environ.copy()
    env["GRASS_OVERWRITE"] = "1"
    elevation = "elev_lid792_1m"
    elev_resampled = "elev_resampled"
    gs.run_command("g.region", raster=elevation, res=4, flags="a", env=env)
    gs.run_command("r.resamp.stats", input=elevation, output=elev_resampled, env=env)

    run_aspect_class(scanned_elev=elev_resampled, env=env)


if __name__ == "__main__":
    main()
