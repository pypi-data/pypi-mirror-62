"""
Functions that actually plot x against y.
"""

import matplotlib.pyplot as plt
import numpy as np
import unyt

from matplotlib.colors import Normalize, LogNorm
from velociraptor import VelociraptorCatalogue
from velociraptor.autoplotter.objects import VelociraptorLine
from typing import Tuple

import velociraptor.tools as tools


def scatter_x_against_y(
    x: unyt.unyt_array, y: unyt.unyt_quantity
) -> Tuple[plt.Figure, plt.Axes]:
    """
    Creates a scatter of x against y (unyt arrays).
    """

    fig, ax = plt.subplots()

    ax.scatter(x.value, y.value, s=1, edgecolor="none", alpha=0.5, zorder=-100)

    set_labels(ax=ax, x=x, y=y)

    return fig, ax


def histogram_x_against_y(
    x: unyt.unyt_array,
    y: unyt.unyt_array,
    x_bins: unyt.unyt_array,
    y_bins: unyt.unyt_array,
) -> Tuple[plt.Figure, plt.Axes]:
    """
    Creates a plot of x against y with a 2d histogram in the background.
    
    Actually uses pcolormesh and the numpy histogram method.
    """

    fig, ax = plt.subplots()

    H, x_bins, y_bins = np.histogram2d(x=x, y=y, bins=[x_bins, y_bins])

    im = ax.pcolormesh(x_bins, y_bins, H.T, norm=LogNorm(), zorder=-100)

    fig.colorbar(im, ax=ax, label="Number of haloes", pad=0.0)

    set_labels(ax=ax, x=x, y=y)

    return fig, ax


def mass_function(
    x: unyt.unyt_array, x_bins: unyt.unyt_array, mass_function: VelociraptorLine
) -> Tuple[plt.Figure, plt.Axes]:
    """
    Creates a plot of x as a mass function, binned with x_bins.
    """

    fig, ax = plt.subplots()

    centers, mass_function, error = mass_function.output

    ax.errorbar(centers, mass_function, error)

    ax.set_xlabel(tools.get_full_label(x))
    ax.set_ylabel(
        tools.get_mass_function_label(
            mass_function_sub_label="{}", mass_function_units=mass_function.units
        )
    )

    return fig, ax


def decorate_axes(
    ax: plt.Axes, catalogue: VelociraptorCatalogue, loc: str = "top left"
) -> None:
    """
    Decorates the axes with information about the redshift and
    scale-factor.
    """

    legend = ax.legend()

    # First need to parse the 'loc' string
    va, ha = loc.split(" ")

    if va == "bottom":
        y = 0.05
    elif va == "top":
        y = 0.95
    else:
        raise AttributeError(f"Unknown location string {loc}. Choose e.g. bottom right")

    if ha == "left":
        x = 0.05
    elif ha == "right":
        x = 0.95

    ax.text(
        x,
        y,
        f"$z={catalogue.z:2.3f}$\n$a={catalogue.a:2.3f}$",
        ha=ha,
        va=va,
        transform=ax.transAxes,
        multialignment=ha,
    )

    return


def set_labels(ax: plt.Axes, x: unyt.unyt_array, y: unyt.unyt_array) -> None:
    """
    Set the x and y labels for the axes.
    """

    ax.set_xlabel(tools.get_full_label(x))
    ax.set_ylabel(tools.get_full_label(y))

    return
