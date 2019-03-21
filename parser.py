# -*- coding: utf-8 -*-
import argparse
import sys


def build_encode_parser():
    encode_parser = subs.add_parser('encode', description='Encode text from file to another')
    encode_parser.set_defaults(method='encode')
    encode_parser.add_argument('--cipher', required=True, help='Cipher name: caesar or vigenere')
    encode_parser.add_argument('--key', required=True, help='Cipher key')
    encode_parser.add_argument('--input-file', required=False,
                               help='Name of input file', dest='input_file', default=sys.stdin)
    encode_parser.add_argument('--output-file', required=False,
                               help='Name of output file', dest='output_file', default=sys.stdout)
    return encode_parser


def build_decode_parser():
    decode_parser = subs.add_parser('decode', description='Decode text from file to another')
    decode_parser.set_defaults(method='decode')
    decode_parser.add_argument('--cipher', required=True, help='Cipher name: caesar or vigenere')
    decode_parser.add_argument('--key', required=True, help='Cipher key')
    decode_parser.add_argument('--input-file', required=False,
                               help='Name of input file', dest='input_file', default=sys.stdin)
    decode_parser.add_argument('--output-file', required=False,
                               help='Name of output file', dest='output_file', default=sys.stdout)
    return decode_parser


def build_train_parser():
    train_parser = subs.add_parser('train', description='Train encryptor using language model')
    train_parser.set_defaults(method='train')
    train_parser.add_argument('--text-file', required=False,
                              help='Name of text file', dest='text_file', default=sys.stdin)
    train_parser.add_argument('--model-file', required=True,
                              help='Name of model file', dest='model_file')
    return train_parser


def build_hack_parser():
    hack_parser = subs.add_parser('hack', description='Try to decode text using language model')
    hack_parser.set_defaults(method='hack')
    hack_parser.add_argument('--input-file', required=False,
                             help='Name of text file', dest='input_file', default=sys.stdin)
    hack_parser.add_argument('--output-file', required=False,
                             help='Name of model file', dest='output_file', default=sys.stdout)
    hack_parser.add_argument('--model-file', required=True,
                             help='Name of model file', dest='model_file')
    return hack_parser


command_parser = argparse.ArgumentParser()
subs = command_parser.add_subparsers()
encode_parser = build_encode_parser()
decode_parser = build_decode_parser()
train_parser = build_train_parser()
hack_parser = build_hack_parser()
