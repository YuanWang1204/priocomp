#!/bin/sh
zig4 -l12_abf_bd/12_abf_bd_out/12_abf_bd.rank_expanded.compressed.tif 16_load_bd_all/16_load_bd_all.dat 16_load_bd_all/16_load_bd_all.spp 16_load_bd_all/16_load_bd_all_out/16_load_bd_all.txt 0 0 1 0 --grid-output-formats=compressed-tif --image-output-formats=png
