#!/usr/bin/python3
import string
import re
import os
import math
import itertools
import glob

letters = list(string.ascii_lowercase)
ngrams = ["Unigram", "Bigram", "Trigram"]
languages = {
    "english": {
        "output": "EN",
    },
    "french": {
        "output": "FR"
    },
    "italian": {
        "output": "OT"
    }
}


def add_training(training_file_en, training_file_fr, training_file_it):
    languages["english"]["training"] = training_file_en
    languages["french"]["training"] = training_file_fr
    languages["italian"]["training"] = training_file_it


def read_model(model, gram, n):
    with open(model, 'r') as file:
        for line in file:
            if n == 1:
                result = re.search('\((.*)\) = (.*)', line)
                key = result.group(1)
                probability = float(result.group(2))
            else:
                result = re.search('\((.*)\|(.*)\) = (.*)', line)
                key = result.group(2) + result.group(1)
                probability = float(result.group(3))
            gram[key]['probability'] = probability


def read_text(filename, n):
    file = open(filename, 'r')
    text = file.read()
    file.close()
    chars = ''.join(filter(str.isalpha, text)).lower()
    chars = [chars[i:i+n] for i in range(len(chars)-(n-1))]
    return chars


def read_sentences(filename, n):
    sentences = {}
    with open(filename, 'r') as file:
        for i, line in enumerate(file):
            original = line.replace('\n', '')
            line = ''.join(filter(str.isalpha, line)).lower()
            line = [line[i:i+n] for i in range(len(line)-(n-1))]
            sentences[i] = {
                'original': original,
                'chars': line
            }
    return sentences


def initialize_gram(n):
    gram = {}
    data = []
    if n > 1:
        for i in itertools.repeat(None, n):
            data.append(letters)
        chars_list = list(itertools.product(*data))
        chars_list = [''.join(chars) for chars in chars_list]
    else:
        chars_list = letters
    for chars in chars_list:
        gram[chars] = {
            'probability': 0,
            'count': 0.5
        }
    return gram


def calc_vals(chars, gram, n):
    total_chars = len(chars)
    for char in chars:
        gram[char]['count'] += 1
    for key, value in gram.items():
        count = value['count']
        probability = count/(total_chars + 0.5*(len(letters)**n))
        value['probability'] = probability


def print_gram(gram, filename, n):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as file:
        for key, value in gram.items():
            if n == 1:
                file.write('({}) = {}\n'.format(key, value['probability']))
            else:
                file.write('({}|{}) = {}\n'.format(key[-1], key[:-1], value['probability']))


def get_prediction(gram):
    max_prob = max(gram, key=lambda x: gram[x]['total'])
    return max_prob


def test_strings(string_list, english_gram, french_gram, italian_gram, name):
    grams = {
        'English': {
            'name': 'ENGLISH',
            'model': english_gram,
            'total': 0
        },
        'French': {
            'name': 'FRENCH',
            'model': french_gram,
            'total': 0
        },
        'Italian': {
            'name': 'OTHER',
            'model': italian_gram,
            'total': 0
        }
    }
    print("\n{} Predictions:\n".format(name))
    for key, value in string_list.items():
        output_file = "./Output/out{}.txt".format(key+1)
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        grams['English']['total'] = 0
        grams['French']['total'] = 0
        grams['Italian']['total'] = 0
        with open(output_file, 'a') as file:
            if name == "Unigram":
                file.write('{}\n\n'.format(value['original']))
            else:
                file.write('----------------\n')
            file.write('{} MODEL\n\n'.format(name.upper()))
            for char in value['chars']:
                file.write('{}: {}\n'.format(name.upper(), char))
                for gram in grams.values():
                    char_prob = gram['model'][char]['probability']
                    gram['total'] += math.log(char_prob)
                    if name == "Unigram":
                        file.write('{}: P({}) = {} ==> log prob of sentence so far: {}\n'
                                   .format(gram['name'], char, char_prob, gram['total']))
                    else:
                        file.write('{}: P({}|{}) = {} ==> log prob of sentence so far: {}\n'
                                   .format(gram['name'], char[-1], char[:-1], char_prob, gram['total']))
                file.write('\n')
            language = get_prediction(grams)
            file.write('According to the {} model, the sentence is in {}\n'.format(name.lower(), language))
            print("Sentence {}: {} is in {}".format(key+1, value['original'], language))


def train(training_file_en, training_file_fr, training_file_it):
    add_training(training_file_en, training_file_fr, training_file_it)
    for index, value in enumerate(ngrams):
        for language in languages.values():
            output_file = './Models/{}{}.txt'.format(value.lower(), language['output'])
            chars = read_text(language['training'], index+1)
            gram = initialize_gram(index+1)
            calc_vals(chars, gram, index+1)
            print_gram(gram, output_file, index+1)


def test(testing_file):
    try:
        files = glob.glob('./Output/*')
        for f in files:
            os.remove(f)
    except OSError:
        pass
    for index, value in enumerate(ngrams):
        string_list = read_sentences(testing_file, index+1)
        for language in languages.values():
            input_model = './Models/{}{}.txt'.format(value.lower(), language['output'])
            gram = initialize_gram(index+1)
            language['gram'] = gram
            read_model(input_model, gram, index+1)
        test_strings(string_list, languages["english"]["gram"], languages["french"]["gram"],
                     languages["italian"]["gram"], value)


def train_and_test(training_file_en, training_file_fr, training_file_it, testing_file):
    train(training_file_en, training_file_fr, training_file_it)
    test(testing_file)
