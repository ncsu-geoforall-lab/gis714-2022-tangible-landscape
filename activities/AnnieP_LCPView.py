#!/usr/bin/env python3

import os

import grass.script as gs


def run_LCP(scanned_elev, scanned_calib_elev, env, points=None, **kwargs):
    """Doesn't do anything, except loading points from a vector map to Python

    If *points* is provided, the function assumes it is name of an existing vector map.
    This is used during testing.
    If *points* is not provided, the function assumes it runs in Tangible Landscape.
    """
    if not points:
        # If there are no points, ask Tangible Landscape to generate points from
        # a change in the surface.
        points = "points"
        import analyses

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
    # Output point coordinates from GRASS GIS and read coordinates into a Python list.
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
        .splitlines()
    )
    if len(data) < 2:
        # For the cases when the analysis expects at least 2 points, we check the
        # number of points and return from the function if there is less than 2
        # points. (No points is a perfectly valid state in Tangible Landscape,
        # so we need to deal with it here.)
        return
    for point in data:
        point_list.append([float(p) for p in point.split(",")][:2])
    LCP(scanned_calib_elev, point_list[0], point_list[1], env)
    gs.run_command(
        "r.viewshed",
        input=scanned_calib_elev,
        output="viewshed",
        coordinates=point_list[1],
        observer_elevation=2,
        flags="b",
        env=env,
    )


def LCP(elevation, start_coordinate, end_coordinate, env):
    gs.run_command("r.slope.aspect", elevation=elevation, slope="slope", env=env)
    gs.run_command(
        "r.cost",
        input="slope",
        output="cost",
        start_coordinates=start_coordinate,
        outdir="outdir",
        flags="k",
        env=env,
    )
    gs.run_command("r.colors", map="cost", color="gyr", env=env)
    gs.run_command(
        "r.drain",
        input="cost",
        output="drain",
        direction="outdir",
        drain="drain",
        flags="d",
        start_coordinates=end_coordinate,
        env=env,
    )


def main():
    env = os.environ.copy()
    env["GRASS_OVERWRITE"] = "1"
    elevation = "elev_lid792_1m"
    elev_resampled = "elev_resampled"
    gs.run_command("g.region", raster=elevation, res=4, flags="a", env=env)
    gs.run_command("r.resamp.stats", input=elevation, output=elev_resampled, env=env)
    # Code specific to testing of the analytical function.
    # Create points which is the additional input needed for the process.
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
    run_LCP(
        scanned_elev=elev_resampled,
        scanned_calib_elev=elev_resampled,
        points=points,
        env=env,
    )  # run the viewshed from the end


if __name__ == "__main__":
    main()
