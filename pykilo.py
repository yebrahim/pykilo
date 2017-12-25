#!/usr/bin/env python

import sys, argparse, tty, os, termios

col = row = 1
text = []
window_rows = window_columns = 0
old_tty = None

def load_file(filename):
  global text, col, row
  for l in open(filename).readlines():
    write_at(l, row, 1)
    text.append([c for c in l])
    row += 1
  row = col = 1
  move_to(1, 1)

def cls():
  print('\033[H\033[J')

def getch():
  return sys.stdin.read(1)

def debug(msg):
  write_at(msg, window_rows - 2, 0)

def write_at(string, r, c):
  sys.stdout.write('\033[{};{}H{}'.format(r, c, string))

def move_to(r, c):
  sys.stdout.write(u'\u001b[{};{}H'.format(r, c))

def backspace():
  global col, row
  col -= 1
  if col == -1:
    row -= 1 if row > 0 else 0
  write_at('', row, col)

def next_pos():
  global row, col
  col += 1
  if col > window_columns:
    col = 1
    row += 1

def start():
  global col, row
  while True:
    ch = getch()
    if ch == ':':
      cmd_col = 1
      move_to(window_rows, 1)
      sys.stdout.write(u'\u001b[2K')
      write_at(':', window_rows, 1)
      command = ''
      while True:
        ch = getch()
        if ord(ch) == 13:
          write_at('command: {}'.format(command), window_rows, 1)
          if command == 'q':
            exit()
          break
        cmd_col += 1
        write_at(ch, window_rows, cmd_col)
        command += ch
    else:
      write_at(ch, row, col)
      next_pos()
      move_to(row, col)

def init():
  global window_rows, window_columns, old_tty
  old_tty = termios.tcgetattr(sys.stdin)
  tty.setraw(sys.stdin)
  ts = os.popen('stty size', 'r').read().split()
  window_rows, window_columns = int(ts[0]), int(ts[1])
  cls()
  move_to(0, 0)

def exit():
  cls()
  termios.tcsetattr(sys.stdin, termios.TCSANOW, old_tty)
  sys.exit()

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('filename', help='file name', nargs='?')
  args = parser.parse_args()

  init()

  if args.filename:
    load_file(args.filename)

  start()

  exit()

