#!/usr/bin/env python3

"""
Instructions

- Functions intended to run for each scan
  need to start with `run_`, e.g., `run_slope`.

- Do not modify the parameters of the `run_` function
  unless you know what you are doing.
  See optional parameters at:
  https://github.com/tangible-landscape/grass-tangible-landscape/wiki/Running-analyses-and-developing-workflows#python-workflows

- All gs.run_command/read_command/write_command/parse_command
  need to be passed *env* parameter like this: `(..., env=env)`.
"""

import os

import grass.script as gs


def run_drain(scanned_elev, scanned_calib_elev, env, points=None, **kwargs):
    drain = "drain"
    if not points:
        elev_no_points = scanned_calib_elev
        points = "points"
        import analyses
        from tangible_utils import get_environment

        env2 = get_environment(raster=elev_no_points)
        analyses.change_detection(
            "scan_saved",
            scanned_elev,
            points,
            height_threshold=[10, 100],
            cells_threshold=[5, 50],
            add=True,
            max_detected=5,
            debug=True,
            env=env,
        )
    else:
        elev_no_points = scanned_elev
        env2 = env
    # if points detected
    if gs.vector_info_topo("points")["points"]:
        gs.run_command(
            "r.drain",
            input=elev_no_points,
            output=drain,
            drain=drain,
            start_points=points,
            env=env2,
        )
    else:
        # create empty vector
        gs.run_command("v.edit", map=drain, tool="create", env=env)


# this part is for testing without TL
def main():

    # get the current environment variables as a copy
    env = os.environ.copy()
    # we want to run this repetetively without deleted the created files
    env["GRASS_OVERWRITE"] = "1"
    elevation = "elev_lid792_1m"
    elev_resampled = "elev_resampled"
    # resampling to have similar resolution as with TL
    gs.run_command("g.region", raster=elevation, res=4, flags="a", env=env)
    gs.run_command("r.resamp.stats", input=elevation, output=elev_resampled, env=env)
    gs.run_command("g.copy", raster=[elev_resampled, "scan_saved"], env=env)

    # create points
    points = "points"
    gs.write_command(
        "v.in.ascii",
        flags="t",
        input="-",
        output=points,
        separator="comma",
        stdin="638432,220382\n638621,220607",
        env=env,
    )
    run_drain(
        scanned_elev=elev_resampled,
        scanned_calib_elev="scan_saved",
        env=env,
        points=points,
    )


if __name__ == "__main__":
    main()
