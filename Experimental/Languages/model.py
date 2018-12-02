#!/usr/bin/python3
import argparse
import language_detection

parser = argparse.ArgumentParser(description='Trains or tests n-gram models')

parser.add_argument("-t", "--test", help="test file")
parser.add_argument("-e", "--english", help="english file")
parser.add_argument("-f", "--french", help="french file")
parser.add_argument("-i", "--italian", help="italian file")
parser.add_argument("-y", "--frisian", help="frisian file")
parser.add_argument("-n", "--dutch", help="dutch file")

args = parser.parse_args()
testing_file = args.test
english_file = args.english
french_file = args.french
italian_file = args.italian
frisian_file = args.frisian
dutch_file = args.dutch

if testing_file and (english_file or french_file or italian_file or frisian_file or dutch_file):
    if not (english_file and french_file and italian_file and frisian_file and dutch_file):
        parser.error("Need all training files (3) and testing file to train and test.")
    else:
        language_detection.train_and_test(english_file, french_file, italian_file,
                                          frisian_file, dutch_file, testing_file)
elif testing_file:
    language_detection.test(testing_file)
elif english_file and french_file and italian_file and frisian_file and dutch_file:
    language_detection.train(english_file, french_file, italian_file, frisian_file, dutch_file)
else:
    parser.error("Need all training files (5) and/or testing file.")



