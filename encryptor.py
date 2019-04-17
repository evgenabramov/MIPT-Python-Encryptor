#!/usr/bin/env python
# -*- coding: utf-8 -*-
import string
import json
import parser
from collections import Counter
from text_manager import get_stream
from itertools import cycle


def get_next_symbol(symbol, step):
    if symbol not in string.ascii_letters:
        return symbol
    if symbol.isupper():
        lower_bound = ord('A')
        upper_bound = ord('Z')
    else:
        lower_bound = ord('a')
        upper_bound = ord('z')
    return chr(lower_bound + (ord(symbol) - lower_bound + step) % (upper_bound - lower_bound + 1))


def caesar(data, key):
    for index, symbol in enumerate(data):
        data[index] = get_next_symbol(symbol, key)
    return data


def vigenere(data, key, is_encoding):
    for (index, symbol), key_symbol in zip(enumerate(data), cycle(key)):
        letter_position = ord(key_symbol)
        data[index] = get_next_symbol(symbol, letter_position if is_encoding else -letter_position)
    return data


def process(cipher, key, input_filename, output_filename, is_encoding):
    with get_stream(input_filename, 'r') as input_file:
        data = list(input_file.read())
    if cipher == 'caesar':
        data = caesar(data, int(key) if is_encoding else -int(key))
    else:
        data = vigenere(data, key, is_encoding)
    data = ''.join(data)
    with get_stream(output_filename, 'w') as output_file:
        output_file.write(data)


def count_frequency(data):
    frequency = Counter(symbol.lower() for symbol in data if symbol in string.ascii_letters)
    num_letters = sum(frequency.values())
    frequency = dict(frequency)
    for letter in frequency.keys():
        frequency[letter] /= num_letters
    return frequency


def train(text_filename, model_filename):
    with get_stream(text_filename, 'r') as text_file:
        data = list(text_file.read())
    frequency = count_frequency(data)
    with open(model_filename, 'w') as model_file:
        json.dump(frequency, model_file)


def get_difference(step, model_frequency, frequency):
    result = 0
    for fake_letter in frequency.keys():
        result += abs(model_frequency[get_next_symbol(fake_letter, step)] - frequency[fake_letter])
    return result


alphabet_length = len(string.ascii_lowercase)


def hack(input_filename, output_filename, model_filename):
    with open(model_filename, 'r') as model_file:
        model_frequency = json.load(model_file)
    with get_stream(input_filename, 'r') as input_file:
        data = list(input_file.read())
    frequency = count_frequency(data)
    min_step = min(range(alphabet_length),
                   key=lambda step: get_difference(step, model_frequency, frequency))
    data = caesar(data, min_step)
    data = ''.join(data)
    with get_stream(output_filename, 'w') as output_file:
        output_file.write(data)


args = parser.command_parser.parse_args()
if args.method == 'encode':
    process(args.cipher, args.key, args.input_file, args.output_file, is_encoding=True)
elif args.method == 'decode':
    process(args.cipher, args.key, args.input_file, args.output_file, is_encoding=False)
elif args.method == 'train':
    train(args.text_file, args.model_file)
elif args.method == 'hack':
    hack(args.input_file, args.output_file, args.model_file)
