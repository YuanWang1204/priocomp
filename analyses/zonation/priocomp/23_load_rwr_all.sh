#!/bin/sh
zig4 -l../../RWR/rwr_all_weights_expanded.tif 23_load_rwr_all/23_load_rwr_all.dat 23_load_rwr_all/23_load_rwr_all.spp 23_load_rwr_all/23_load_rwr_all_out/23_load_rwr_all.txt 0 0 1 0 --grid-output-formats=compressed-tif --image-output-formats=png
