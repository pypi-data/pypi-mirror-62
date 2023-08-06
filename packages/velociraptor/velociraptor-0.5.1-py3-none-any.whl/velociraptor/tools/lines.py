"""
Tools to generate various lines from datasets.
"""

import unyt
import numpy as np

from typing import List


def binned_mean_line(
    x: unyt.unyt_array,
    y: unyt.unyt_array,
    x_bins: unyt.unyt_array,
    minimum_in_bin: int = 1,
):
    """
    Get a mean line.
    
    Takes:

    x, an array of values to bin
    y, an array of values to find the mean in each bin of (and error)
    x_bins, the bins to use
    minimum_in_bin, the minimal number of values in each bin for it to be valid

    Returns:

    bin centers, mean, standard deviation
    """

    assert (
        x.units == x_bins.units
    ), "Please ensure that the x values and bins have the same units."

    hist = np.digitize(x, x_bins)

    means = []
    standard_deviations = []
    centers = []

    for bin in range(1, len(x_bins)):
        indicies_in_this_bin = hist == bin

        if indicies_in_this_bin.sum() >= minimum_in_bin:
            y_values_in_this_bin = y[indicies_in_this_bin].value

            means.append(np.mean(y_values_in_this_bin))
            standard_deviations.append(np.std(y_values_in_this_bin))

            centers.append(0.5 * (x_bins[bin - 1].value + x_bins[bin].value))

    means *= y.units
    standard_deviations *= y.units
    centers *= x.units

    return centers, means, standard_deviations


def binned_median_line(
    x: unyt.unyt_array,
    y: unyt.unyt_array,
    x_bins: unyt.unyt_array,
    percentiles: List[int] = [16, 86],
    minimum_in_bin: int = 1,
):
    """
    Get a median line with percentiles.
    
    Takes:

    x, an array of values to bin
    y, an array of values to find the mean in each bin of (and error)
    x_bins, the bins to use
    percentiles, the percentiles to use to calculate the deviation between
    minimum_in_bin, the minimal number of values in each bin for it to be valid

    Returns:

    bin centers, median, deviation, 
    """

    assert (
        x.units == x_bins.units
    ), "Please ensure that the x values and bins have the same units."

    hist = np.digitize(x, x_bins)

    medians = []
    deviations = []
    centers = []

    for bin in range(1, len(x_bins)):
        indicies_in_this_bin = hist == bin

        if indicies_in_this_bin.sum() >= minimum_in_bin:
            y_values_in_this_bin = y[indicies_in_this_bin].value

            medians.append(np.median(y_values_in_this_bin))
            deviations.append(np.percentile(y_values_in_this_bin, percentiles))

            centers.append(0.5 * (x_bins[bin - 1].value + x_bins[bin].value))

    medians *= y.units
    deviations *= y.units
    # Percentiles actually gives us the values - we want to be able to use
    # matplotlib's errorbar function
    deviations = abs(deviations.T - medians)
    centers *= x.units

    return centers, medians, deviations

