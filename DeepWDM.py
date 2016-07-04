# -*- coding: utf-8 -*-
"""
Code to run DeepWDM tool on a directory of .wav files.
Takes as input the directory containing wav files and the 
directory for textgrids to be saved.

DeepWDM: https://github.com/adiyossi/DeepWDM
Measures word duration (word onset and offset) and creates textgrid.

Emily Cibelli, emily.cibelli@northwestern.edu
Last updated: 6/14/2016
"""

import os
import sys
import argparse
import DeepWDM.predict 	# DeepWDM
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


def main(wav_path, textgrid_path, model, output_predictions):
    if os.path.isfile(output_predictions):
        os.remove(output_predictions)

    # check if both inputs are directories
    if os.path.isdir(wav_path) and os.path.isdir(textgrid_path):
        # Select each wav file, create a textgrid name, run DeepWDM script
        for wav_filename in mylistdir(wav_path):
            textgrid_filename = wav_filename.replace(".wav", ".TextGrid")
            wav_filename_abs = os.path.abspath("%s/%s" % (wav_path, wav_filename))
            textgrid_filename_abs = os.path.abspath("%s/%s" % (textgrid_path, textgrid_filename))
            output_predictions_abs = os.path.abspath(output_predictions)
            os.chdir("DeepWDM")
            tmp_predictions = generate_tmp_filename("preds")
            DeepWDM.predict.predict(wav_filename_abs, textgrid_filename_abs, model, tmp_predictions)
            csv_append_row(tmp_predictions, output_predictions_abs)
            os.chdir(current_dir)
    elif os.path.isfile(wav_path):
        wav_path_abs = os.path.abspath(wav_path)
        textgrid_path_abs = os.path.abspath(textgrid_path)
        output_preds_abs = os.path.abspath(output_predictions)
        os.chdir("DeepWDM")
        DeepWDM.predict.predict(wav_path_abs, textgrid_path_abs, model, output_preds_abs)
        os.chdir(current_dir)
    else:
        print >> sys.stderr, "Input paths should be both files or both directories."
        print >> sys.stderr, "It might be that the input WAV or one of the folder do not exists."


if __name__ == "__main__":
    # command line arguments
    parser = argparse.ArgumentParser("Automatic tool of word duration measurement.")
    parser.add_argument("input_wav_path", help="a WAV file or folder with WAV files")
    parser.add_argument("output_textgrid_path", help="an output TextGrid or output folder")
    parser.add_argument("output_predictions", help="CSV file with predictions")
    args = parser.parse_args()
    
    # main function
    main(args.input_wav_path, args.output_textgrid_path, "rnn", args.output_predictions)