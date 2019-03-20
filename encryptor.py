#!/usr/bin/env python
# -*- coding: utf-8 -*-
import string
import json
import parser
from text_manager import get_stream


def get_next_symbol(symbol, step, is_encoding=True):
    if not is_encoding:
        step = -step
    if symbol in string.ascii_uppercase:
        lower_bound = ord('A')
        upper_bound = ord('Z')
        return chr(lower_bound + (ord(symbol) - lower_bound + step) % (upper_bound - lower_bound + 1))
    elif symbol in string.ascii_lowercase:
        lower_bound = ord('a')
        upper_bound = ord('z')
        return chr(lower_bound + (ord(symbol) - lower_bound + step) % (upper_bound - lower_bound + 1))
    return symbol


def caesar(data, key, is_encoding):
    for index in range(len(data)):
        data[index] = get_next_symbol(data[index], key, is_encoding)
    return data


def vigenere(data, key, is_encoding):
    for index in range(len(data)):
        data[index] = get_next_symbol(data[index], ord(key[index % len(key)]), is_encoding)
    return data


def encode(cipher, key, input_filename, output_filename):
    with get_stream(input_filename, 'r') as input_file:
        data = list(input_file.read())
    if cipher == 'caesar':
        data = caesar(data, int(key), is_encoding=True)
    else:
        data = vigenere(data, key, is_encoding=True)
    data = ''.join(data)
    with get_stream(output_filename, 'w') as output_file:
        output_file.write(data)


def decode(cipher, key, input_filename, output_filename):
    with get_stream(input_filename, 'r') as input_file:
        data = list(input_file.read())
    if cipher == 'caesar':
        data = caesar(data, int(key), is_encoding=False)
    else:
        data = vigenere(data, key, is_encoding=False)
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


def hack(input_filename, output_filename, model_filename):
    with open(model_filename, 'r') as model_file:
        model_frequency = json.load(model_file)
    with get_stream(input_filename, 'r') as input_file:
        data = list(input_file.read())
    frequency = count_frequency(data)
    min_diff = len(string.ascii_lowercase)
    min_step = 0
    for step in range(len(string.ascii_lowercase)):
        diff = 0
        for fake_letter in frequency.keys():
            diff += abs(model_frequency[get_next_symbol(fake_letter, step)]
                        - frequency[fake_letter])
        if diff < min_diff:
            min_step = step
            min_diff = diff
    data = caesar(data, min_step, is_encoding=True)
    data = ''.join(data)
    with get_stream(output_filename, 'w') as output_file:
        output_file.write(data)


args = parser.command_parser.parse_args()
if args.method == 'encode':
    encode(args.cipher, args.key, args.input_file, args.output_file)
elif args.method == 'decode':
    decode(args.cipher, args.key, args.input_file, args.output_file)
elif args.method == 'train':
    train(args.text_file, args.model_file)
elif args.method == 'hack':
    hack(args.input_file, args.output_file, args.model_file)
