#!/usr/bin/env python3

    def run_viewshed(scanned_elev, env, **kwargs):
    coordinates = [638830, 220150]
    gs.run_command('r.viewshed', input=scanned_elev, output='viewshed', coordinates=coordinates, observer_elevation=2, flags='b', env=env)
    gs.run_command('r.colors', map='viewshed', color='grey')
    
    if __name__ == '__main__':
    import os
    os.environ['GRASS_OVERWRITE'] = '1'
    elevation = 'elev_lid792_1m'
    run_viewshed(scanned_elev=elevation, env=None)
