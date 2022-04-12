#!/usr/bin/env python3

import os

import grass.script as gs


def run_curvatures(scanned_elev, env, **kwargs):
    gs.run_command(
        "r.param.scale",
        input=scanned_elev,
        output="profile_curv",
        method="profc",
        size=11,
        env=env,
    )
    gs.run_command(
        "r.param.scale",
        input=scanned_elev,
        output="tangential_curv",
        method="crosc",
        size=11,
        env=env,
    )
    gs.run_command(
        "r.colors", map=["profile_curv", "tangential_curv"], color="curvature", env=env
    )

    gs.run_command(
        "r.mapcalc",
        expression="curvature_mix = if(row() > col(), tangential_curv, profile_curv)",
    )


def main():
    env = os.environ.copy()
    env["GRASS_OVERWRITE"] = "1"
    elevation = "elev_lid792_1m"
    elev_resampled = "elev_resampled"
    gs.run_command("g.region", raster=elevation, res=4, flags="a", env=env)
    gs.run_command("r.resamp.stats", input=elevation, output=elev_resampled, env=env)

    run_curvatures(scanned_elev=elev_resampled, env=env)


if __name__ == "__main__":
    main()
