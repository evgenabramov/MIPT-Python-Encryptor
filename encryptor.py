#!/usr/bin/env python
# -*- coding: utf-8 -*-
import string
import json
import parser
from text_manager import get_stream


def get_next_symbol(symbol, step, is_encoding=True):
    if not is_encoding:
        step = -step
    if symbol not in string.ascii_letters:
        return symbol
    if symbol in string.ascii_uppercase:
        lower_bound = ord('A')
        upper_bound = ord('Z')
    else:
        lower_bound = ord('a')
        upper_bound = ord('z')
    return chr(lower_bound + (ord(symbol) - lower_bound + step) % (upper_bound - lower_bound + 1))


def caesar(data, key, is_encoding):
    for index in range(len(data)):
        data[index] = get_next_symbol(data[index], key, is_encoding)
    return data


def vigenere(data, key, is_encoding):
    for index in range(len(data)):
        data[index] = get_next_symbol(data[index], ord(key[index % len(key)]), is_encoding)
    return data


def process(cipher, key, input_filename, output_filename, is_encoding):
    with get_stream(input_filename, 'r') as input_file:
        data = list(input_file.read())
    if cipher == 'caesar':
        data = caesar(data, int(key), is_encoding)
    else:
        data = vigenere(data, key, is_encoding)
    data = ''.join(data)
    with get_stream(output_filename, 'w') as output_file:
        output_file.write(data)


def count_frequency(data):
    frequency = {}
    for letter in string.ascii_lowercase:
        frequency[letter] = 0.0
    num_letters = 0
    for symbol in data:
        if symbol in string.ascii_letters:
            frequency[symbol.lower()] += 1
            num_letters += 1
    for letter in string.ascii_lowercase:
        frequency[letter] = frequency[letter] / num_letters
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


def hack(input_filename, output_filename, model_filename):
    with open(model_filename, 'r') as model_file:
        model_frequency = json.load(model_file)
    with get_stream(input_filename, 'r') as input_file:
        data = list(input_file.read())
    frequency = count_frequency(data)
    min_step = min([step for step in range(alphabet_length)],
                   key=lambda step: get_difference(step, model_frequency, frequency))
    data = caesar(data, min_step, is_encoding=True)
    data = ''.join(data)
    with get_stream(output_filename, 'w') as output_file:
        output_file.write(data)


alphabet_length = len(string.ascii_lowercase)

args = parser.command_parser.parse_args()
if args.method == 'encode':
    process(args.cipher, args.key, args.input_file, args.output_file, is_encoding=True)
elif args.method == 'decode':
    process(args.cipher, args.key, args.input_file, args.output_file, is_encoding=False)
elif args.method == 'train':
    train(args.text_file, args.model_file)
elif args.method == 'hack':
    hack(args.input_file, args.output_file, args.model_file)
