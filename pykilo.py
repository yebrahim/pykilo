#!/usr/bin/env python

import sys, argparse, tty, os

col = row = 1
lines = []
window_rows = window_columns = 0

def load_file(filename):
  global lines, col, row
  lines = open(filename).readlines()
  for l in lines:
    write_at(l, row, 1)
    row += 1
  row -= 1
  col = len(lines[-1])
  move_to(row, col)

def cls():
  print('\033[H\033[J')

def getch():
  return sys.stdin.read(1)

def debug(msg):
  write_at(msg, window_rows - 2, 0)

def write_at(string, r, c):
  sys.stdout.write('\033[{};{}H'.format(r, c) + string)

def move_to(r, c):
  sys.stdout.write(u'\u001b[{};{}H'.format(r, c))

def backspace():
  global col, row
  col -= 1
  if col == -1:
    row -= 1 if row > 0 else 0
  write_at('', row, col)

def start():
  global col, row
  while True:
    ch = getch()
    write_at(ch, row, col)
    col += 1
    move_to(row, col)
    if ch == ':':
      if getch() == 'q':
        break
      else:
        sys.stdout.write(ch)
    #if ch == '\x7f':
      #print('YAY')

def init():
  global window_rows, window_columns
  tty.setraw(sys.stdin)
  ts = os.popen('stty size', 'r').read().split()
  window_rows, window_columns = ts[0], ts[1]
  cls()
  move_to(0, 0)

def exit():
  cls()

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('filename', help='file name', nargs='?')
  args = parser.parse_args()

  init()

  if args.filename:
    load_file(args.filename)

  start()

  exit()

