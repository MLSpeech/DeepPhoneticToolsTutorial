# -*- coding: utf-8 -*-
"""
Code to run DeepFormants tool


Emily Cibelli, emily.cibelli@northwestern.edu
Last updated: 6/14/2016
"""

import os
import sys
import argparse
import DeepFormants.formants
from helpers.utilities import *

# The starting directory, defined to cd to in case of error
current_dir = os.path.dirname(os.path.abspath(__file__))


# Directory listing for Mac, to avoid files like .DS_Store
# https://mail.python.org/pipiermail/tutor/2004-April/029019.html
def mylistdir(directory):
    """ A specialized version of os.listdir() that ignores files
    that start with a leading period (e.g. .DS_Store)."""
    filelist = os.listdir(directory)
    return [x for x in filelist if not (x.startswith('.'))]


def main(wav_path, textgrid_path, prediction_filename, tier_name):
    # check if both inputs are directories
    if os.path.isdir(wav_path) and os.path.isdir(textgrid_path):
        if os.path.isfile(prediction_filename):
            os.remove(prediction_filename)
        # Select each wav file, create a textgrid name, run DeepWDM script
        for wav_filename in mylistdir(wav_path):
            textgrid_filename = wav_filename.replace(".wav", ".TextGrid")
            wav_filename_abs = os.path.abspath("%s/%s" % (wav_path, wav_filename))
            textgrid_filename_abs = os.path.abspath("%s/%s" % (textgrid_path, textgrid_filename))
            prediction_filename_abs = os.path.abspath(prediction_filename)
            os.chdir("DeepFormants")
            tmp_preds = generate_tmp_filename("preds")
            DeepFormants.formants.predict_from_textgrid(wav_filename_abs, tmp_preds, textgrid_filename_abs, tier_name)
            csv_append_row(tmp_preds, prediction_filename_abs)
            os.chdir(current_dir)
    elif os.path.isfile(wav_path):
        wav_path_abs = os.path.abspath(wav_path)
        textgrid_path_abs = os.path.abspath(textgrid_path)
        prediction_filename_abs = os.path.abspath(prediction_filename)
        os.chdir("DeepFormants")
        DeepFormants.formants.predict_from_textgrid(wav_path_abs, prediction_filename_abs, textgrid_path_abs, tier_name)
        os.chdir(current_dir)
    else:
        print >> sys.stderr, "Input paths should be both files or both directories."
        print >> sys.stderr, "It might be that the input WAV or one of the folder do not exists."


if __name__ == "__main__":
    # command line arguments
    parser = argparse.ArgumentParser("Automatic tool of word duration measurement.")
    parser.add_argument("input_wav_path", help="a WAV file or folder with WAV files")
    parser.add_argument("input_textgrid_path", help="an input TextGrid or folder, each labeled with the vowels")
    parser.add_argument("predictions_filename", help="output CSV file")
    parser.add_argument("--tier_name", default="VOWEL")
    args = parser.parse_args()
    
    # main function
    main(args.input_wav_path, args.input_textgrid_path, args.predictions_filename, args.tier_name)

