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
The following command li

```
python DeepWDM.py sampleFiles/waveforms/goose_male.wav sampleFiles/word_durations/goose_male.TextGrid sampleFiles/goose_male.csv
python DeepWDM.py sampleFiles/waveforms sampleFiles/word_durations sampleFiles/word_durations.csv

python AutoVowelDuration.py sampleFiles/waveforms/goose_male.wav sampleFiles/vowel_durations/goose_male.TextGrid sampleFiles/goose_male.csv
python AutoVowelDuration.py sampleFiles/waveforms sampleFiles/vowel_durations sampleFiles/vowel_durations.csv

python DeepFormants.py sampleFiles/waveforms/goose_male.wav sampleFiles/vowel_durations/goose_male.TextGrid sampleFiles/goose_male.csv
python DeepFormants.py sampleFiles/waveforms sampleFiles/vowel_durations sampleFiles/formants.csv

python GenerateSearchWindows.py sampleFiles/word_durations/goose_male.TextGrid
python GenerateSearchWindows.py sampleFiles/word_durations

python AutoVOT.py sampleFiles/waveform/goose_male.wav sampleFiles/word_durations/goose_male.TextGrid
python AutoVOT.py sampleFiles/waveform sampleFiles/word_durations
```

```
python DeepWDM.py sampleFiles/waveforms/goose_male.wav sampleFiles/word_durations/goose_male.TextGrid sampleFiles/goose_male.csv
python DeepWDM.py sampleFiles/waveforms sampleFiles/word_durations sampleFiles/word_durations.csv

python AutoVowelDuration.py sampleFiles/waveforms/goose_male.wav sampleFiles/vowel_durations/goose_male.TextGrid sampleFiles/goose_male.csv
python AutoVowelDuration.py sampleFiles/waveforms sampleFiles/vowel_durations sampleFiles/vowel_durations.csv

python DeepFormants.py sampleFiles/waveforms/goose_male.wav sampleFiles/vowel_durations/goose_male.TextGrid sampleFiles/goose_male.csv
python DeepFormants.py sampleFiles/waveforms sampleFiles/vowel_durations sampleFiles/formants.csv

python GenerateSearchWindows.py sampleFiles/word_durations/goose_male.TextGrid
python GenerateSearchWindows.py sampleFiles/word_durations

python AutoVOT.py sampleFiles/waveform/goose_male.wav sampleFiles/word_durations/goose_male.TextGrid
python AutoVOT.py sampleFiles/waveform sampleFiles/word_durations
```
