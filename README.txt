LanguageDetection

Instructions

Usage: python3 model.py [-h] [-t test_file] [-e english_file] [-f french_file] [-i italian_file]

To run this program specify the python3 interpreter and the model.py script name with arguments. The program
expects multiple options that can be explained by running the -h or --help command.

In the Basic folder, code can be found implementing only unigram and bigram models, with quite a bit of duplication.
However, in the Experimental folder, the code has been made generic to support any n-gram model with the change
of one variable. In the language_detection.py file there is the following line:

ngrams = ["Unigram", "Bigram", "Trigram"]

Adding another n-gram to this list will allow the program to train and test using that value of n,
however when adding an n-gram to this list, the previous ones must also be in the list, in order. 

In addition to test with the 3 original languages use the program in folder Ngrams and to experiment with the
addition languages of Dutch and West Frisian, use the program in folder Languages

The file 30SentencesUnigram.txt contains the 10 original sentence, 10 that unigram gets wrong and 10 that it gets right.
The file 30SentencesBigram.txt contains the 10 original sentence, 10 that bigram gets wrong and 10 that it gets right.
The file 50SentencesExperimental.txt contains the 50 sentences to be used with the language experiment.
The file 30Sentences.txt contains the 30 sentence we use to originally test the system.

The program expects all files with relative paths from the program file or an absolute path.

Basic

Train/generate the model:

python3 model.py -e '../Training/trainEN.txt' -f '../Training/trainFR.txt' -i '../Training/trainOT.txt'

Test the models:

python3 model.py -t '../Testing/30Sentences.txt'

To both train and test:

python3 model.py -e '../Training/trainEN.txt' -f '../Training/trainFR.txt' -i '../Training/trainOT.txt' -t '../Testing/30Sentences.txt'

Experimental

Language

Train/generate the model:

python3 model.py -e '../../Training/trainEN.txt' -f '../../Training/trainFR.txt' -i '../../Training/trainOT.txt' -y '../../Training/trainFY.txt' -n '../../Training/trainNL.txt'

Test the models:

python3 model.py -t '../../Testing/50SentencesExperimental.txt'

To both train and test:

python3 model.py -e '../../Training/trainEN.txt' -f '../../Training/trainFR.txt' -i '../../Training/trainOT.txt' -y '../../Training/trainFY.txt' -n '../../Training/trainNL.txt' -t '../../Testing/50SentencesExperimental.txt'

Ngram

Train/generate the model:

python3 model.py -e '../../Training/trainEN.txt' -f '../../Training/trainFR.txt' -i '../../Training/trainOT.txt'

Test the models:

python3 model.py -t '../../Testing/30Sentences.txt'

To both train and test:

python3 model.py -e '../../Training/trainEN.txt' -f '../../Training/trainFR.txt' -i '../../Training/trainOT.txt' -t '../../Testing/30Sentences.txt'
