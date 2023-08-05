#!/usr/bin/python3
"""Compute the Irreproducible Discovery Rate (IDR) from NarrowPeaks files

This section of the code provide facilities to handle logs in the mIDR project
"""
import logging
import sys
from os import path

import numpy as np
import matplotlib.pyplot as plt


def add_log(log, theta, logl, pseudo):
    """
    function to append thata and ll value to the logs
    """
    log['logl'].append(logl)
    if pseudo:
        log['pseudo_data'].append('#FF4949')
    else:
        log['pseudo_data'].append('#4970FF')
    for parameters in theta:
        log[parameters].append(theta[parameters])
    return log


def setup_logging(options):
    """Configure logging."""
    root = logging.getLogger(__name__)
    root.setLevel(logging.INFO)
    file_handler = logging.FileHandler(options.output + "/log.txt")
    file_handler.setLevel(logging.INFO)
    root.addHandler(file_handler)
    handler_list = [file_handler]
    if options.verbose:
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        root.addHandler(console)
        handler_list.append(console)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s: %(message)s", datefmt='%H:%M:%S',
        handlers=handler_list
    )


def plot_log(log, file_name):
    """
    plot logs into a file
    """
    x_axis = np.linspace(start=0,
                         stop=len(log['logl']),
                         num=len(log['logl']))
    i = 1
    for parameters in log:
        if parameters != "pseudo_data":
            plt.subplot(len(log.keys()), 1, i)
            plt.scatter(x_axis,
                        log[parameters],
                        c=log['pseudo_data'],
                        s=2)
            plt.ylabel(parameters)
            plt.xlabel('steps')
            i += 1
    plt.savefig(file_name)


def plot_classif(x_score, u_values, z_values, lidr, file_name):
    """
    plot logs into a file
    """
    plt.subplot(4, 1, 1)
    plt.hist(x_score[:, 0], bins=1000, label=str(0))
    plt.ylabel('counts')
    plt.xlabel('x scores')
    plt.subplot(4, 1, 2)
    plt.hist(z_values[:, 0], bins=1000, label=str(0))
    plt.ylabel('counts')
    plt.xlabel('z scores')
    plt.subplot(4, 1, 3)
    dotplot1 = plt.scatter(x_score[:, 1], z_values[:, 0], c=lidr)
    plt.ylabel('z score')
    plt.xlabel('x scores')
    cbar = plt.colorbar(dotplot1)
    cbar.ax.set_ylabel('lidr')
    plt.subplot(4, 1, 4)
    dotplot2 = plt.scatter(u_values[:, 1], z_values[:, 0], c=lidr)
    plt.ylabel('z score')
    plt.xlabel('u scores')
    cbar = plt.colorbar(dotplot2)
    cbar.ax.set_ylabel('lidr')
    plt.savefig(file_name)


def plot_samic(params_list, copula_list, file_name, iter, loglik):
    """
    plot logs into a file
    """
    for copula in copula_list:
        i = 1
        for params in ['pi', 'theta']:
            plt.subplot(len(copula_list) * 3 + 1, 1, i)
            plt.scatter(iter,
                        params_list[copula][params],
                        s=2)
            plt.ylabel(copula + params)
            plt.xlabel('steps')
            i += 1
        plt.subplot(len(copula_list) * 3 + 1, 1, i)
        plt.scatter(iter,
                    params_list['alpha'][params_list['order'][copula]],
                    s=2)
        plt.ylabel(copula + "alpha")
        plt.xlabel('steps')
        i += 1
    plt.subplot(len(copula_list) * 3 + 1, 1, i)
    plt.scatter(iter,
                loglik,
                s=2)
    plt.ylabel("loglik")
    plt.xlabel('steps')
    plt.savefig(file_name)
