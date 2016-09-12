#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Functions and utilities comparing raster similarities.

Module can be used alone or as part of Snakemake workflow.
"""
import logging
import rasterio
import os
import pandas as pd
import numpy as np

from importlib.machinery import SourceFileLoader
from scipy.spatial.distance import jaccard
from timeit import default_timer as timer

utils = SourceFileLoader("lib.utils", "src/00_lib/utils.py").load_module()


def compute_jaccard(x, y, x_min=0.0, x_max=1.0, y_min=0.0, y_max=1.0,
                    warn_uneven=True, limit_tolerance=4, disable_checks=False):
    """Calculate the Jaccard index (Jaccard similarity coefficient).

    The Jaccard coefficient measures similarity between sample sets, and is
    defined as the size of the intersection divided by the size of the union of
    the sample sets. The Jaccard coefficient can be calculated for a subset of
    rasters provided by using the threshold argument.

    Min and max values must be provided for both RasterLayer objects x
    and y. Method can be used with RasterLayers of any value range, but
    the defaults [0.0, 1.0] are geared towards comparing Zonation rank priority
    rasters. Limits provided are inclusive.

    :param x ndarray object.
    :param y ndarray object.
    :param x_min Numeric minimum threshold value for x to be used
                 (default 0.0).
    :param x_max Numeric maximum threshold value for x to be used
                 (default 1.0).
    :param y_min Numeric minimum threshold value for y to be used
                 (default 0.0).
    :param y_max Numeric maximum threshold value for y to be used
                 (default 1.0).
    :param warn_uneven Boolean indicating whether a warning is raised if the
                       compared raster coverages are very (>20x) uneven.
    :param limit_tolerance integer values that defines to which precision x and
                           y limits are rounded to. This helps e.g. with values
                           that close to 0 but not quite 0 (default: 4, i.e.
                           round(x, 4)).
    :param disable_checks boolean indicating if the input limit values are
                          checked against the actual raster values in x and y.

    :return numeric value in [0, 1].
    """
    if not disable_checks:
        assert x_min >= np.round(np.min(x), limit_tolerance), "Min threshold smaller than computed min of x"
        assert x_max >= np.round(np.max(x), limit_tolerance), "Max threshold smaller than computed max of x"
        assert x_min < x_max, "Min threshold for x larger to max threshold"
        assert y_min >= np.round(np.min(y), limit_tolerance), "Min threshold smaller than computed min of y"
        assert y_max <= np.round(np.max(y), limit_tolerance), "Max threshold smaller than computed max of y"
        assert y_min < y_max, "Min threshold for y larger to max threshold"

    # Get the values according to the limits provided
    x_bin = (x >= x_min) & (x <= x_max)
    y_bin = (y >= y_min) & (y <= y_max)

    if warn_uneven:
        x_size = np.sum(x_bin)
        y_size = np.sum(y_bin)
        # Sort from smaller to larger
        sizes = np.sort([x_size, y_size])
        if sizes[1] / sizes[0] > 20:
            print("WARNING: The extents of raster values above the "
                  "threshhold differ more than 20-fold: Jaccard coefficient " +
                  "may not be informative.")

    # Compute the Jaccard-Needham dissimilarity between two boolean 1-D arrays
    # and subtract from 1 to get the Jaccard index
    return 1 - jaccard(x_bin.flatten(), y_bin.flatten())


def cross_jaccard(input_rasters, thresholds, verbose=False, logger=None):
    """ Calculate Jaccard coefficients bewteen all the inpur rasters.

    This is a utility function that is intented to be used to compare
    top-fractions of the landscape. Thus, x_max and y_max for
    jaccard are fixed to 1.0.

    :param input_rasters list of input raster paths.
    :param thresholds Numeric vector values of thresholds.
    :param verbose: Boolean indicating how much information is printed out.
    :param logger: logger object to be used.
    :param ... additional arguments passed on to jaccard().

    :return Pandas Dataframe with Jaccard coefficients between all rasters.
    """
    # 1. Setup  --------------------------------------------------------------

    all_start = timer()

    if not logger:
        logging.basicConfig()
        llogger = logging.getLogger('cross_jaccard')
        llogger.setLevel(logging.DEBUG if verbose else logging.INFO)
    else:
        llogger = logger

    # Check the inputs
    assert len(input_rasters) > 1, "More than one input rasters are needed"
    assert len(thresholds) >= 1, "At least one threshold is needed"

    # 2. Calculations --------------------------------------------------------

    llogger.info(" [** COMPUTING JACCARD INDICES **]")

    all_jaccards = pd.DataFrame({"feature1": [], "feature2": [],
                                 "threshold": [], "coef": []})
    n_rasters = len(input_rasters)
    # Generate counter information for all the computations. The results
    # matrix is always diagonally symmetrical.
    n_computations = int((n_rasters * n_rasters - n_rasters) / 2 * len(thresholds))
    no_computation = 1

    for threshold in thresholds:
        # Initialize a matrix to hold the jaccard coefficients and populate it
        # with -1s.
        jaccards = np.empty([n_rasters, n_rasters])
        jaccards[:] = -1.0

        for i in range(0, n_rasters):
            raster1 = rasterio.open(input_rasters[i])
            # To calculate the Jaccard index we are dealing with binary data
            # only. Avoid using masked arrays and replace NoData values with
            # zeros.
            raster1_nodata = raster1.nodata
            raster1_src = raster1.read(1)
            np.place(raster1_src, np.isclose(raster1_src, raster1_nodata), 0.0)
            for j in range(i+1, n_rasters):
                raster2 = rasterio.open(input_rasters[j])
                raster2_nodata = raster2.nodata
                raster2_src = raster2.read(1)
                np.place(raster2_src, np.isclose(raster2_src, raster2_nodata), 0.0)
                prefix = utils.get_iteration_prefix(no_computation,
                                                    n_computations)
                llogger.info(("{} Calculating Jaccard ".format(prefix) +
                              "index for [{}".format(threshold) +
                              ", 1.0] between {} ".format(input_rasters[i]) +
                              "and {}".format(input_rasters[j])))

                coef = compute_jaccard(raster1_src, raster2_src,
                                       x_min=threshold, x_max=1.0,
                                       y_min=threshold, y_max=1.0)
                jaccards = pd.DataFrame({"feature1": [input_rasters[i]],
                                         "feature2": [input_rasters[j]],
                                         "threshold": [threshold],
                                         "coef": [coef]})
                all_jaccards = pd.concat([all_jaccards, jaccards])
                no_computation += 1

    all_jaccards.index = np.arange(0, len(all_jaccards.index), 1)

    all_end = timer()
    all_elapsed = round(all_end - all_start, 2)
    llogger.info(" [TIME] All processing took {} sec".format(all_elapsed))

    return all_jaccards
