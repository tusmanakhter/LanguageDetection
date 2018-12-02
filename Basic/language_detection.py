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


def read_bigram_model(model, bigram):
    with open(model, 'r') as file:
        for line in file:
            result = re.search('\((.*)\|(.*)\) = (.*)', line)
            key = result.group(2) + result.group(1)
            probability = float(result.group(3))
            bigram[key]['probability'] = probability


def read_text_unigram(filename):
    file = open(filename, 'r')
    text = file.read()
    file.close()
    chars = list(''.join(filter(str.isalpha, text)).lower())
    return chars


def read_text_bigram(filename):
    file = open(filename, 'r')
    text = file.read()
    file.close()
    chars = ''.join(filter(str.isalpha, text)).lower()
    chars = [chars[i:i+2] for i in range(len(chars)-1)]
    return chars


def read_sentences_unigram(filename):
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


def read_sentences_bigram(filename):
    sentences = {}
    with open(filename, 'r') as file:
        for i, line in enumerate(file):
            original = line.replace('\n', '')
            line = ''.join(filter(str.isalpha, line)).lower()
            line = [line[i:i + 2] for i in range(len(line) - 1)]
            sentences[i] = {
                'original': original,
                'chars': line
            }
    return sentences


def initialize_unigram():
    unigram = {}
    for letter in letters:
        unigram[letter] = {
            'probability': 0,
            'count': 0
        }
    return unigram


def initialize_bigram():
    bigram = {}
    for letter in letters:
        for letter2 in letters:
            bigram[letter + letter2] = {
                'probability': 0,
                'count': 0
            }
    return bigram


def calc_unigram_vals(chars, unigram):
    total_chars = len(chars)
    for char in chars:
        unigram[char]['count'] += 1
    for key, value in unigram.items():
        count = value['count']
        probability = (count+0.5)/(total_chars + len(letters)*0.5)
        value['probability'] = probability


def calc_bigram_vals(chars, bigram):
    total_chars = {}
    for letter in letters:
        total_chars[letter] = 0
    for char in chars:
        bigram[char]['count'] += 1
        total_chars[char[:-1]] += 1
    for key, value in bigram.items():
        count = value['count']
        probability = (count+0.5)/(total_chars[key[:-1]] + len(letters)*0.5)
        value['probability'] = probability


def print_unigram(unigram, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as file:
        for key, value in unigram.items():
            file.write('({}) = {}\n'.format(key, value['probability']))


def print_bigram(bigram, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as file:
        for key, value in bigram.items():
            file.write('({}|{}) = {}\n'.format(key[1], key[0], value['probability']))


def get_prediction(gram):
    max_prob = max(gram, key=lambda x: gram[x]['total'])
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
    print("Unigram Predictions:\n")
    for key, value in string_list.items():
        output_file = "./Output/out{}.txt".format(key+1)
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        unigrams['English']['total'] = 0
        unigrams['French']['total'] = 0
        unigrams['Italian']['total'] = 0
        with open(output_file, 'w') as file:
            file.write('{}\n\n'.format(value['original']))
            file.write('UNIGRAM MODEL\n\n')
            for char in value['chars']:
                file.write('UNIGRAM: {}\n'.format(char))
                for unigram in unigrams.values():
                    char_prob = unigram['model'][char]['probability']
                    unigram['total'] += math.log(char_prob)
                    file.write('{}: P({}) = {} ==> log prob of sentence so far: {}\n'
                               .format(unigram['name'], char, char_prob, unigram['total']))
                file.write('\n')
            language = get_prediction(unigrams)
            file.write('According to the unigram model, the sentence is in {}\n'.format(language))
            print("Sentence {}: {} is in {}".format(key+1, value['original'], language))


def test_strings_bigram(string_list, english_bigram, french_bigram, italian_bigram):
    bigrams = {
        'English': {
            'name': 'ENGLISH',
            'model': english_bigram,
            'total': 0
        },
        'French': {
            'name': 'FRENCH',
            'model': french_bigram,
            'total': 0
        },
        'Italian': {
            'name': 'OTHER',
            'model': italian_bigram,
            'total': 0
        }
    }
    print("\nBigram Predictions:\n")
    for key, value in string_list.items():
        output_file = "./Output/out{}.txt".format(key+1)
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        bigrams['English']['total'] = 0
        bigrams['French']['total'] = 0
        bigrams['Italian']['total'] = 0
        with open(output_file, 'a') as file:
            file.write('----------------\n')
            file.write('BIGRAM MODEL\n\n')
            for char in value['chars']:
                file.write('BIGRAM: {}\n'.format(char))
                for bigram in bigrams.values():
                    char_prob = bigram['model'][char]['probability']
                    bigram['total'] += math.log(char_prob)
                    file.write('{}: P({}|{}) = {} ==> log prob of sentence so far: {}\n'
                               .format(bigram['name'], char[1], char[0], char_prob, bigram['total']))
                file.write('\n')
            language = get_prediction(bigrams)
            file.write('According to the bigram model, the sentence is in {}\n'.format(language))
            print("Sentence {}: {} is in {}".format(key+1, value['original'], language))


def train(training_file_en, training_file_fr, training_file_it):
    # Unigram
    english_chars = read_text_unigram(training_file_en)
    english_unigram = initialize_unigram()
    calc_unigram_vals(english_chars, english_unigram)
    print_unigram(english_unigram, './Models/unigramEN.txt')

    french_chars = read_text_unigram(training_file_fr)
    french_unigram = initialize_unigram()
    calc_unigram_vals(french_chars, french_unigram)
    print_unigram(french_unigram, './Models/unigramFR.txt')

    italian_chars = read_text_unigram(training_file_it)
    italian_unigram = initialize_unigram()
    calc_unigram_vals(italian_chars, italian_unigram)
    print_unigram(italian_unigram, './Models/unigramOT.txt')

    #Bigram
    english_chars = read_text_bigram(training_file_en)
    english_bigram = initialize_bigram()
    calc_bigram_vals(english_chars, english_bigram)
    print_bigram(english_bigram, './Models/bigramEN.txt')

    french_chars = read_text_bigram(training_file_fr)
    french_bigram = initialize_bigram()
    calc_bigram_vals(french_chars, french_bigram)
    print_bigram(french_bigram, './Models/bigramFR.txt')

    italian_chars = read_text_bigram(training_file_it)
    italian_bigram = initialize_bigram()
    calc_bigram_vals(italian_chars, italian_bigram)
    print_bigram(italian_bigram, './Models/bigramOT.txt')


def test(testing_file):
    # Unigram
    string_list_unigram = read_sentences_unigram(testing_file)
    english_unigram = initialize_unigram()
    read_unigram_model('./Models/unigramEN.txt', english_unigram)
    french_unigram = initialize_unigram()
    read_unigram_model('./Models/unigramFR.txt', french_unigram)
    italian_unigram = initialize_unigram()
    read_unigram_model('./Models/unigramOT.txt', italian_unigram)

    test_strings_unigram(string_list_unigram, english_unigram, french_unigram, italian_unigram)

    # Bigram
    string_list_bigram = read_sentences_bigram(testing_file)
    english_bigram = initialize_bigram()
    read_bigram_model('./Models/bigramEN.txt', english_bigram)
    french_bigram = initialize_bigram()
    read_bigram_model('./Models/bigramFR.txt', french_bigram)
    italian_bigram = initialize_bigram()
    read_bigram_model('./Models/bigramOT.txt', italian_bigram)

    test_strings_bigram(string_list_bigram, english_bigram, french_bigram, italian_bigram)


def train_and_test(training_file_en, training_file_fr, training_file_it, testing_file):
    # Unigram
    string_list_unigram = read_sentences_unigram(testing_file)

    english_chars = read_text_unigram(training_file_en)
    english_unigram = initialize_unigram()
    calc_unigram_vals(english_chars, english_unigram)
    print_unigram(english_unigram, './Models/unigramEN.txt')

    french_chars = read_text_unigram(training_file_fr)
    french_unigram = initialize_unigram()
    calc_unigram_vals(french_chars, french_unigram)
    print_unigram(french_unigram, './Models/unigramFR.txt')

    italian_chars = read_text_unigram(training_file_it)
    italian_unigram = initialize_unigram()
    calc_unigram_vals(italian_chars, italian_unigram)
    print_unigram(italian_unigram, './Models/unigramOT.txt')

    test_strings_unigram(string_list_unigram, english_unigram, french_unigram, italian_unigram)

    # Bigram
    string_list_bigram = read_sentences_bigram(testing_file)

    english_chars = read_text_bigram(training_file_en)
    english_bigram = initialize_bigram()
    calc_bigram_vals(english_chars, english_bigram)
    print_bigram(english_bigram, './Models/bigramEN.txt')

    french_chars = read_text_bigram(training_file_fr)
    french_bigram = initialize_bigram()
    calc_bigram_vals(french_chars, french_bigram)
    print_bigram(french_bigram, './Models/bigramFR.txt')

    italian_chars = read_text_bigram(training_file_it)
    italian_bigram = initialize_bigram()
    calc_bigram_vals(italian_chars, italian_bigram)
    print_bigram(italian_bigram, './Models/bigramOT.txt')

    test_strings_bigram(string_list_bigram, english_bigram, french_bigram, italian_bigram)