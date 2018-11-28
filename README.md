# LanguageDetection

Assignment for COMP 472.

Creates and uses n-gram models to classify sentences into English, French or Italian.

# Requirements
1. Python 3.5+

# Instructions

**Usage**: `python3 model.py [-h] [-t test_file] [-e english_file] [-f french_file] [-i italian_file]`

To run this program specify the python3 interpreter and the model.py script name with arguments. The program
expects multiple options that can be explained by running the -h or --help command.

The program expects all files with relative path from the program file or an absolute path.

Generate the model:

`python3 model.py -e '../Training/trainEN.txt' -f '../Training/trainFR.txt' -i '../Training/trainOT.txt'`

Test the model:

`python3 model.py -t '../Testing/30Sentences.txt'`

