#!/bin/sh
zig4 -l12_abf_bd/12_abf_bd_out/08_abf_es.rank_bd_matched.compressed.tif 19_load_es_bd/19_load_es_bd.dat 19_load_es_bd/19_load_es_bd.spp 19_load_es_bd/19_load_es_bd_out/19_load_es_bd.txt 0 0 1 0 --grid-output-formats=compressed-tif --image-output-formats=png
