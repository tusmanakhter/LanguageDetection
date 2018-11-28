#!/usr/bin/python3
import string
import re
import os
import math

letters = list(string.ascii_lowercase)


def read_unigram_model(model, unigram):
    with open(model, 'r') as file:
        for line in file:
            result = re.search('\((.*)\) = (.*)', line)
            key = result.group(1)
            probability = float(result.group(2))
            unigram[key]['probability'] = probability


def read_text(filename):
    file = open(filename, 'r')
    text = file.read()
    file.close()
    chars = list(''.join(filter(str.isalpha, text)).lower())
    return chars


def read_sentences(filename):
    sentences = {}
    with open(filename, 'r') as file:
        for i, line in enumerate(file):
            original = line.replace('\n', '')
            line = list(''.join(filter(str.isalpha, line)).lower())
            sentences[i] = {
                'original': original,
                'chars': line
            }
    return sentences


def intialize_unigram():
    unigram = {}
    for letter in letters:
        unigram[letter] = {
            'probability': 0,
            'count': 0.5
        }
    return unigram


def calc_unigram_vals(chars, unigram):
    total_chars = len(chars)
    for char in chars:
        unigram[char]['count'] += 1
    for key, value in unigram.items():
        count = value['count']
        probability = count/(total_chars + len(letters)*0.5)
        value['probability'] = probability


def print_unigram(unigram, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as file:
        for key, value in unigram.items():
            file.write('({}) = {}\n'.format(key, value['probability']))


def get_predictions_unigram(unigrams):
    max_prob = max(unigrams, key=lambda x: unigrams[x]['total'])
    return max_prob


def test_strings_unigram(string_list, english_unigram, french_unigram, italian_unigram):
    unigrams = {
        'English': {
            'name': 'ENGLISH',
            'model': english_unigram,
            'total': 0
        },
        'French': {
            'name': 'FRENCH',
            'model': french_unigram,
            'total': 0
        },
        'Italian': {
            'name': 'OTHER',
            'model': italian_unigram,
            'total': 0
        }
    }

    for key, value in string_list.items():
        output_file = "./Output/out{}.txt".format(key+1)
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w') as file:
            file.write('{}\n'.format(value['original']))
            file.write('UNIGRAM MODEL\n')
            for char in value['chars']:
                file.write('UNIGRAM: {}\n'.format(char))
                for unigram in unigrams.values():
                    char_prob = unigram['model'][char]['probability']
                    unigram['total'] += math.log(char_prob)
                    file.write('{}: P({}) = {} ==> log prob of sentence so far: {}\n'
                               .format(unigram['name'], char, char_prob, unigram['total']))
                file.write('\n')
            language = get_predictions_unigram(unigrams)
            file.write('According to the unigram model, the sentence is in {}\n'.format(language))
            print("Sentence {}: {} is in {}".format(key+1, value['original'], language))


def train(training_file_en, training_file_fr, training_file_it):
    english_chars = read_text(training_file_en)
    english_unigram = intialize_unigram()
    calc_unigram_vals(english_chars, english_unigram)
    print_unigram(english_unigram, './Models/unigramEN.txt')

    french_chars = read_text(training_file_fr)
    french_unigram = intialize_unigram()
    calc_unigram_vals(french_chars, french_unigram)
    print_unigram(french_unigram, './Models/unigramFR.txt')

    italian_chars = read_text(training_file_it)
    italian_unigram = intialize_unigram()
    calc_unigram_vals(italian_chars, italian_unigram)
    print_unigram(italian_unigram, './Models/unigramOT.txt')


def test(testing_file):
    string_list = read_sentences(testing_file)
    english_unigram = intialize_unigram()
    read_unigram_model('./Models/unigramEN.txt', english_unigram)
    french_unigram = intialize_unigram()
    read_unigram_model('./Models/unigramFR.txt', french_unigram)
    italian_unigram = intialize_unigram()
    read_unigram_model('./Models/unigramOT.txt', italian_unigram)

    test_strings_unigram(string_list, english_unigram, french_unigram, italian_unigram)


def train_and_test(training_file_en, training_file_fr, training_file_it, testing_file):
    string_list = read_sentences(testing_file)

    english_chars = read_text(training_file_en)
    english_unigram = intialize_unigram()
    calc_unigram_vals(english_chars, english_unigram)
    print_unigram(english_unigram, './Models/unigramEN.txt')

    french_chars = read_text(training_file_fr)
    french_unigram = intialize_unigram()
    calc_unigram_vals(french_chars, french_unigram)
    print_unigram(french_unigram, './Models/unigramFR.txt')

    italian_chars = read_text(training_file_it)
    italian_unigram = intialize_unigram()
    calc_unigram_vals(italian_chars, italian_unigram)
    print_unigram(italian_unigram, './Models/unigramOT.txt')

    test_strings_unigram(string_list, english_unigram, french_unigram, italian_unigram)
