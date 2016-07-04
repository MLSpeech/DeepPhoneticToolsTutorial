# {Deep} Phonetic Tools Tutorial

The repository contains the scripts, data and links to the repositories that used in the tutorial presented at BigPhon, a LabPhon15 Satellite Workshop. 

## Installation
The code is compatible with Mac OS X and Linux and was tested on OS X El-Capitan and Ubuntu 14.04. In order to install you need to type in command line
```
git clone --recursive https://github.com/MLSpeech/DeepPhoneticToolsTutorial.git
```

#### Dependencies
The code uses the following dependencies:
 - Torch7 with RNN package
```bash
git clone https://github.com/torch/distro.git ~/torch --recursive
cd ~/torch; bash install-deps;
./install.sh 

# On Linux with bash
source ~/.bashrc
# On Linux with zsh
source ~/.zshrc
# On OSX or in Linux with none of the above.
source ~/.profile

# For rnn package installation
luarocks install rnn
```
 - [Python (2.7) + Numpy](https://penandpants.com/2012/02/24/install-python/)
 - For the visualization tools: [Matplotlib](https://penandpants.com/2012/02/24/install-python/)

#### Ubuntu
Ubuntu users should also install SoX:
```bash
apt-get install sox
```
 
#### Model Installation
A model for DeepWDM should be downloaded from here: [RNN model](https://drive.google.com/open?id=0Bxkc5_D0JjpiNHVzU19WTUdBS3M). Then, should be moved to here: `DeepWDM/back_end/results/`.


## Usage and Examples
In the first part of the usage example we process a waveform in which the word goose /g uw s/ is pronnounced in isolation by a male. 

In order to find the duration of the whole word type
```
python DeepWDM.py sampleFiles/waveforms/goose_male.wav sampleFiles/word_durations/goose_male.TextGrid sampleFiles/goose_male.csv
```
The resulted TextGrid will contain a tier called *WORD*.
To extract the vowel from a waveform type
```
python AutoVowelDuration.py sampleFiles/waveforms/goose_male.wav sampleFiles/vowel_durations/goose_male.TextGrid sampleFiles/goose_male.csv
```
The resulted TextGrid will contain a tier called *VOWEL*.
In order to estimate the formants of the vowel defined by the previous step type
```
python DeepFormants.py sampleFiles/waveforms/goose_male.wav sampleFiles/vowel_durations/goose_male.TextGrid sampleFiles/goose_male.csv --tier_name VOWEL
```
In order to estimate the voice onset time (VOT) in the begining of the word, we first need to define a search window. To define a search window of 180 msec *before* the beginning of the word and the 100 msec *after* the beginning of the word, just type
```
python GenerateSearchWindows.py sampleFiles/word_durations/goose_male.TextGrid --before 0.18 --after 0.1
```
The resulted TextGrid will include a new tier called *WINDOW*.
The actual extraction of the VOT can be done as follows:
```
python AutoVOT.py sampleFiles/waveform/goose_male.wav sampleFiles/word_durations/goose_male.TextGrid
```

We now show how to process a whole directory of files. The first senatio to extract formants of the vowles you can type:
```
python AutoVowelDuration.py sampleFiles/waveforms sampleFiles/vowel_durations sampleFiles/vowel_durations.csv

python DeepFormants.py sampleFiles/waveforms sampleFiles/vowel_durations sampleFiles/formants.csv
```
In order to extract VOT in the begining of the words you can type
```
python DeepWDM.py sampleFiles/waveforms sampleFiles/word_durations sampleFiles/word_durations.csv

python GenerateSearchWindows.py sampleFiles/word_durations

python AutoVOT.py sampleFiles/waveform sampleFiles/word_durations
```
