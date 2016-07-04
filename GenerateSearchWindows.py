# -*- coding: utf-8 -*-
"""
Generate search windows for the processing of AutoVOT and DeepVOT

Joseph Keshet joseph.keshet@biu.ac.il
Last updated: 6/29/2016
"""

import os
import sys
import argparse
from helpers.textgrid import *

# The starting directory, defined to cd to in case of error
current_dir = os.path.dirname(os.path.abspath(__file__))


# Directory listing for Mac, to avoid files like .DS_Store
# https://mail.python.org/pipiermail/tutor/2004-April/029019.html
def mylistdir(directory):
    """ A specialized version of os.listdir() that ignores files
    that start with a leading period (e.g. .DS_Store)."""
    filelist = os.listdir(directory)
    return [x for x in filelist if not (x.startswith('.'))]


def generate_search_windows(textgrid_filename, tier, before, after):
    # read the whole input text grid
    textgrid = TextGrid()
    textgrid.read(textgrid_filename)
    tier_names = textgrid.tierNames()

    window_xmin = list()
    window_xmax = list()
    window_mark = list()
    tier_index = tier_names.index(tier)
    # print all its interval, which has some value in their description (mark)
    for (i, interval) in enumerate(textgrid[tier_index]):
        if re.search(r'\S', interval.mark()):
            # define processing window
            window_xmin.append(max(textgrid.xmin(), textgrid[tier_index][i].xmin() - before))
            window_xmax.append(min((textgrid[tier_index][i].xmin() + after, textgrid.xmax())))
            window_mark.append(i)

    # prepare TextGrid
    window_tier = IntervalTier(name='window', xmin=textgrid.xmin(), xmax=textgrid.xmax())
    window_tier.append(Interval(textgrid.xmin(), window_xmin[0], ''))
    for i in xrange(0, len(window_xmin)-1):
        window_tier.append(Interval(window_xmin[i], window_xmax[i], window_mark[i]))
        window_tier.append(Interval(window_xmax[i], window_xmin[i+1], ''))
    window_tier.append(Interval(window_xmin[-1], window_xmax[-1], window_mark[-1]))
    window_tier.append(Interval(window_xmax[-1], textgrid.xmax(), ''))

    # write textgrid
    textgrid.append(window_tier)
    textgrid.write(textgrid_filename)


def main(textgrid_path, tier, before, after):
    # check if both inputs are directories
    if os.path.isdir(textgrid_path):
        # Select each wav file, create a textgrid name, run DeepWDM script
        for textgrid_filename in mylistdir(textgrid_path):
            textgrid_filename_abs = os.path.abspath("%s/%s" % (textgrid_path, textgrid_filename))
            generate_search_windows(textgrid_filename_abs, tier, before, after)
    elif os.path.isfile(textgrid_path):
        textgrid_path_abs = os.path.abspath(textgrid_path)
        generate_search_windows(textgrid_path_abs, tier, before, after)
    else:
        print >> sys.stderr, "Input path %s not found." % textgrid_path


if __name__ == "__main__":
    # command line arguments
    parser = argparse.ArgumentParser("Generate search windows for the processing of AutoVOT and DeepVOT.")
    parser.add_argument("textgrid_path", help="a TextGrid file or folder")
    parser.add_argument("--tier", default="word", help="name of the tier with the word boundaries")
    parser.add_argument("--before", default=0.18, help="seconds before the word start boundary", type=float)
    parser.add_argument("--after", default=0.1, help="seconds after the word start boundary", type=float)
    args = parser.parse_args()
    
    # main function
    main(args.textgrid_path, args.tier, args.before, args.after)
