#!/usr/bin/env python3

import os

import grass.script as gs


def run_viewshed(scanned_elev, scanned_calib_elev, env, points=None, **kwargs):
    viewshed = "viewshed"
    if not points:
        points = "points"
        import analyses

        analyses.change_detection(
            scanned_calib_elev,
            scanned_elev,
            points,
            height_threshold=[10, 100],
            cells_threshold=[5, 50],
            add=True,
            max_detected=5,
            debug=True,
            env=env,
        )

    # if points detected
    if gs.vector_info_topo("points")["points"]:
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
            output=viewshed,
            coordinates=[float(p) for p in data.split(",")][:2],
            observer_elevation=2,
            flags="b",
            env=env,
        )
    else:
        # create empty vector
        gs.mapcalc(f"{viewshed} = null()", env=env)


def main():
    env = os.environ.copy()
    env["GRASS_OVERWRITE"] = "1"
    elevation = "elev_lid792_1m"
    elev_resampled = "elev_resampled"
    # We use resampling to get a similar resolution as with Tangible Landscape.
    gs.run_command("g.region", raster=elevation, res=4, flags="a", env=env)
    gs.run_command("r.resamp.stats", input=elevation, output=elev_resampled, env=env)
    # The end of the block which needs no editing.

    # Code specific to testing of the analytical function.
    # Create points which is the additional input needed for the process.
    points = "points"
    gs.write_command(
        "v.in.ascii",
        flags="t",
        input="-",
        output=points,
        separator="comma",
        stdin="638432,220382",
        env=env,
    )
    run_viewshed(
        scanned_elev=elev_resampled,
        scanned_calib_elev=elev_resampled,
        points=points,
        env=env,
    )


if __name__ == "__main__":
    main()
