#!/usr/bin/env python3

import os

import grass.script as gs


def run_viewshed(scanned_elev, scanned_calib_elev, env, points=None, **kwargs):
    viewshed = "viewshed"
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
        point_list = []
        data = (
            gs.read_command(
                "v.out.ascii",
                input=points,
                type="point",
                format="point",
                separator="comma",
                env=env,
            )
            .strip()
            .splitlines()[0]
        )
        gs.run_command(
            "r.viewshed",
            input=scanned_calib_elev,
            output="viewshed",
            coordinates=[float(p) for p in data.split(",")][:2],
            observer_elevation=2,
            flags="b",
            env=env,
        )
    else:
        # create empty vector
        gs.mapcalc("viewshed = null()", env=env)


def main():
    env = os.environ.copy()
    env["GRASS_OVERWRITE"] = "1"
    elevation = "elev_lid792_1m"

    run_viewshed(scanned_elev=elevation, env=env)


if __name__ == "__main__":
    main()
