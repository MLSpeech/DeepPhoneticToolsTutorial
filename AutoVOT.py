# -*- coding: utf-8 -*-
"""
Code to run AutoVOT tool
"""

import os
import sys
import argparse
from helpers.utilities import *

# The starting directory, defined to cd to in case of error
current_dir = os.path.dirname(os.path.abspath(__file__))

auto_vot_model = "models/vot_predictor.amanda.max_num_instances_1000.model"


# Directory listing for Mac, to avoid files like .DS_Store
# https://mail.python.org/pipiermail/tutor/2004-April/029019.html
def mylistdir(directory):
    """ A specialized version of os.listdir() that ignores files
    that start with a leading period (e.g. .DS_Store)."""
    filelist = os.listdir(directory)
    return [x for x in filelist if not (x.startswith('.'))]


def csv_append_row_and_correct_wav(tmp_preds, preds_filename, wav_path, tmp_wav_path, with_headers=True):

    if with_headers:
        skip_header = True

    all_lines = list()

    # check if the CSV file exists
    if os.path.isfile(preds_filename):
        # read it lines
        for line in open(preds_filename, 'r'):
            all_lines.append(line)
    else:
        # if the file does not exist it does not have headers and they should be copied
        skip_header = False

    # check if there is a header
    for line in open(tmp_preds, 'r'):
        if skip_header:
            skip_header = False
        else:
            all_lines.append(line.replace(tmp_wav_path, wav_path))
    # now dump everything back
    with open(preds_filename, 'w') as f:
        for line in all_lines:
            f.write(line)


def main(wav_path, textgrid_path, windows_tier, output_csv_filename):
    # check if both inputs are directories
    if os.path.isdir(wav_path) and os.path.isdir(textgrid_path):
        if os.path.isfile(output_csv_filename):
            os.remove(output_csv_filename)
        # Select each wav file, create a textgrid name, run DeepWDM script
        for wav_filename in mylistdir(wav_path):
            textgrid_filename = wav_filename.replace(".wav", ".TextGrid")
            wav_filename_abs = os.path.abspath("%s/%s" % (wav_path, wav_filename))
            textgrid_filename_abs = os.path.abspath("%s/%s" % (textgrid_path, textgrid_filename))
            output_csv_filename_abs = os.path.abspath(output_csv_filename)
            os.chdir("AutoVOT/autovot/bin")
            tmp_wav16_filename = generate_tmp_filename("wav")
            command1 = "sox %s -c 1 -r 16000 %s" % (wav_filename_abs, tmp_wav16_filename)
            easy_call(command1)
            tmp_predictions = generate_tmp_filename("preds")
            command2 = "python auto_vot_decode.py %s %s %s --window_tier %s --csv_file %s" % (tmp_wav16_filename,
                                                                                       textgrid_filename_abs,
                                                                                       auto_vot_model,
                                                                                       windows_tier,
                                                                                       tmp_predictions)
            easy_call(command2)
            csv_append_row_and_correct_wav(tmp_predictions, output_csv_filename_abs, wav_filename_abs, tmp_wav16_filename)
            os.remove(tmp_predictions)
            os.remove(tmp_wav16_filename)
            os.chdir(current_dir)
    elif os.path.isfile(wav_path):
        wav_path_abs = os.path.abspath(wav_path)
        textgrid_path_abs = os.path.abspath(textgrid_path)
        output_csv_filename_abs = os.path.abspath(output_csv_filename)
        os.chdir("AutoVOT/autovot/bin")
        tmp_wav16_filename = generate_tmp_filename("wav")
        command1 = "sox %s -c 1 -r 16000 %s" % (wav_path_abs, tmp_wav16_filename)
        easy_call(command1)
        tmp_predictions = generate_tmp_filename("preds")
        command2 = "python auto_vot_decode.py %s %s %s --window_tier %s --csv_file %s" % (tmp_wav16_filename,
                                                                                   textgrid_path_abs,
                                                                                   auto_vot_model,
                                                                                   windows_tier,
                                                                                   tmp_predictions)
        easy_call(command2)
        csv_append_row_and_correct_wav(tmp_predictions, output_csv_filename_abs, wav_path_abs, tmp_wav16_filename)
        os.remove(tmp_wav16_filename)
        os.remove(tmp_predictions)
        os.chdir(current_dir)
    else:
        print >> sys.stderr, "Input paths should be both files or both directories."
        print >> sys.stderr, "It might be that the input WAV or one of the folder do not exists."


if __name__ == "__main__":
    # command line arguments
    parser = argparse.ArgumentParser("Automatic tool of word duration measurement.")
    parser.add_argument("wav_path", help="a WAV file or folder with WAV files")
    parser.add_argument("textgrid_path", help="a TextGrid file or folder")
    parser.add_argument("csv_output_path", help="a CSV filename for output")
    parser.add_argument("--windows_tier", default="window", help="optional tier name for search window")
    args = parser.parse_args()
    
    # main function
    main(args.wav_path, args.textgrid_path, args.windows_tier, args.csv_output_path)