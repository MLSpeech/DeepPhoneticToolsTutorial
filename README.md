# {Deep} Phonetic Tools Tutorial

The repository contains the scripts, data and links to the repositories that used in the tutorial presented at BigPhon, a LabPhon15 Satellite Workshop. 

## Installation
The code is compatible with Mac OS X and Linux and was tested on OS X El-Capitan and Ubuntu 14.04. In order to install you need to type in command line
```
git clone --recursive https://github.com/MLSpeech/DeepPhoneticToolsTutorial
```

### Dependencies
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

### Ubuntu
Ubuntu users should also install SoX:
```bash
apt-get install sox
```
 
### Model Installation
First, download the desired model: [RNN](https://drive.google.com/open?id=0Bxkc5_D0JjpiNHVzU19WTUdBS3M), [2 Stacked Layers RNN](https://drive.google.com/open?id=0Bxkc5_D0JjpiS3VOVjVUNlVZSlU), [Bi-Directional RNN](https://drive.google.com/open?id=0Bxkc5_D0JjpiNWlOOUFtMzYzY1U). Than, move the model file to: `back_end/results/` inside the project directory.

## Usage
For measurement just type: 
```bash
python predict.py "input wav file" "output text grid file" "model type"
```

## Example
You can try our tool using the example file in the data folder. 
Type:
```bash
python predict.py data/test.wav data/test.TextGrid rnn
```

## Training Your Own Model
In order to train DeepWDM model using your own data you need to preform two steps:
- A. Extract features 
- B. Train the model

### Extract features 
Extracting features for training new model can be done by using the run_front_end.py script from the fron/_end folder.
This script get as input three parameter:
- A. The path where to the folder which contains the .wav files.
- B. the path to the manual annotation files. Those files should be in a TextGrid format, the same as in the example folder.
- C. The path where to save the features and labels.

To test the feature extraction procedure, type the following command from the front\_end folder: 
```bash
python run_front_end.py data/test_file/ --in_path_y data/test_file/ data/test_features/
```
This script will generate two files(tmp.features and tmp.label), one for the features and one for the labels. These files will be used to train ht model.

### Train the model
In oder to train the model you should run the run.lua script from the back/_end folder with the right path to the labels and features from the previous step.
The parameter for the new files are: `-folder_path`, `-x_filename` and `y_filename`.

### Useful Tricks
- In order to load the data faster, it is recommended to convert the features and labels files to .t7 format. You can do it by simply using the convert2t7.lua script, it gets as input the path to the features and label files along with the desired output paths, and saves them as .t7 file. 
- Another option is to run the data.lua script and uncomment lines 38-39 with the torch.save() command.
- You can try out the impact of the other parameters such as: learning rate, different optimization technique, etc.
- If your dataset is unbalanced, i.e there are much more silence then activities in the speech signal, you can try to different weights on the loss functions. This can be done by changing the values of the `weights` parameter in loss.lua file.
