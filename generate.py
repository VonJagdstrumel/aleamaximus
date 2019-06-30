#!/usr/bin/env python3

import sys

import markovify

text = sys.stdin.read()
text_model = markovify.NewlineText(text)

for i in range(int(sys.argv[1])):
    print(text_model.make_sentence())
