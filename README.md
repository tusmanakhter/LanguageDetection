# LanguageDetection

Assignment for COMP 472.

Creates and uses n-gram models to classify sentences into English, French or Italian.

# Requirements
1. Python 3+

# Instructions

**Usage**: `python3 model.py [-h] [-t test_file] [-e english_file] [-f french_file] [-i italian_file]`

To run this program specify the python3 interpreter and the model.py script name with arguments. The program
expects multiple options that can be explained by running the -h or --help command.

In the **_Basic_** folder, code can be found implementing only unigram and bigram models, with quite a bit of duplication. 
However, in the **_Experimental_** folder, the code has been made generic to support any n-gram model with the change
of one variable. In the _language_detection.py_ file there is the following line:

`ngrams = ["Unigram", "Bigram", "Trigram"]`

Adding another n-gram to this list will allow the program to train and test using that value of n it, 
however when adding an n-gram to this list, the previous ones must also be in the list, in order. 

The program expects all files with relative paths from the program file or an absolute path.

Train/generate the model:

`python3 model.py -e '../Training/trainEN.txt' -f '../Training/trainFR.txt' -i '../Training/trainOT.txt'`

Test the model:

`python3 model.py -t '../Testing/30Sentences.txt'`

To both train and test:

`python3 model.py -e '../Training/trainEN.txt' -f '../Training/trainFR.txt' -i '../Training/trainOT.txt' -t '../Testing/30Sentences.txt'`