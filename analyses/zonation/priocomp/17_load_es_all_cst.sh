#!/bin/sh
zig4 -l10_abf_es_cst/10_abf_es_cst_out/10_abf_es_cst.rank_expanded.compressed.tif 17_load_es_all_cst/17_load_es_all_cst.dat 17_load_es_all_cst/17_load_es_all_cst.spp 17_load_es_all_cst/17_load_es_all_cst_out/17_load_es_all_cst.txt 0 0 1 0 --grid-output-formats=compressed-tif --image-output-formats=png
