#!/bin/sh
zig4 -l../../ILP/ilp_all_weights_costs_expanded.tif 26_load_ilp_all_cst/26_load_ilp_all_cst.dat 26_load_ilp_all_cst/26_load_ilp_all_cst.spp 26_load_ilp_all_cst/26_load_ilp_all_cst_out/26_load_ilp_all_cst.txt 0 0 1 0 --grid-output-formats=compressed-tif --image-output-formats=png
