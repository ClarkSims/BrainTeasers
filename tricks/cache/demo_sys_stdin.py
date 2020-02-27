#!/usr/bin/env python3
import sys

for line in sys.stdin:
  tokens = line.split()
  print('tokens = {{{}}}'.format(tokens))
