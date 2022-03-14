#!/usr/bin/env python3

import os

import grass.script as gs


def LCP(elevation, start_coordinate, end_coordinate, env):
    gs.run_command('r.slope.aspect', elevation=scanned_elev, slope='slope', env=env) #get slope
    gs.run_command('r.cost', input='slope', output='cost', start_coordinates=start_coordinate, outdir='outdir',
                   flags='k', env=env) #input slope, output cost 
    gs.run_command('r.colors', map='cost', color='gyr', env=env) #map of colors  
    gs.run_command('r.drain', input='cost', output='drain', direction='outdir',drain='drain', 
                   flags='d', start_coordinates=end_coordinate, env=env)  #input cost, output drain
    
    
def run_viewshed(scanned_elev, env, **kwargs):
    end = [638928, 220472]
    gs.run_command('r.viewshed', input=scanned_elev, output='viewshed', coordinates=end, observer_elevation=2, flags='b', env=env)

    

def main():
    env = os.environ.copy()
    env["GRASS_OVERWRITE"] = "1"
    elevation = "elev_lid792_1m"
    start = [638469, 220070]
    end = [638928, 220472]
    
    LCP(elevation, start, end, env) #run the LCP command 
    run_viewshed(scanned_elev=elevation, env=env) #run the viewshed from the end


if __name__ == "__main__":
    main()
