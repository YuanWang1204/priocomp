#!/bin/sh
zig4 -l../../ILP/ilp_all_weights_expanded.tif 24_load_ilp_all/24_load_ilp_all.dat 24_load_ilp_all/24_load_ilp_all.spp 24_load_ilp_all/24_load_ilp_all_out/24_load_ilp_all.txt 0 0 1 0 --grid-output-formats=compressed-tif --image-output-formats=png
