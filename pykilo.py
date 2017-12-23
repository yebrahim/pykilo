#!/usr/bin/env python3

import sys, argparse, tty, termios, fcntl, os

cursorX = cursorY = 0

def load_file(filename):
  lines = open(filename).readlines()
  cursorY = len(lines) + 1
  cursorX = len(lines[-1])
  write_at(''.join(lines), 0, 0)
  write_at('hi', cursorX, cursorY - 1)

def cls():
  print('\033[H\033[J')

def getch():
  old_settings = termios.tcgetattr(0)
  new_settings = old_settings[:]
  new_settings[3] &= ~termios.ICANON & ~termios.ECHO
  try:
    termios.tcsetattr(0, termios.TCSANOW, new_settings)
    ch = sys.stdin.read(1)
  finally:
    termios.tcsetattr(0, termios.TCSANOW, old_settings)
  return ch

def write_at(string, x, y):
  print('\033[{};{}H'.format(y, x) + string)

def start():
  while 1:
    ch = getch()
    sys.stdout.write(ch)
    sys.stdout.flush()
    if ch == ':':
      if getch() == 'q':
        break
      else:
        print(ch, end='')
    if ch == '\x7f':
      print('YAY')

def init():
  cls()

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

