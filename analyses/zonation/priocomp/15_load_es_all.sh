#!/bin/sh
zig4 -l08_abf_es/08_abf_es_out/08_abf_es.rank_expanded.compressed.tif 15_load_es_all/15_load_es_all.dat 15_load_es_all/15_load_es_all.spp 15_load_es_all/15_load_es_all_out/15_load_es_all.txt 0 0 1 0 --grid-output-formats=compressed-tif --image-output-formats=png
