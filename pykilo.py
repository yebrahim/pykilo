#!/usr/bin/env python

import sys, argparse, tty, os, termios

col = row = 1
text = []
window_rows = window_columns = 0
old_tty = None

def write_at(string, r, c):
  sys.stdout.write('\033[{};{}H{}'.format(r, c, str(string)))

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
  return ord(sys.stdin.read(1))

def debug(msg):
  write_at(msg, window_rows - 2, 0)

def move_to(r, c):
  sys.stdout.write(u'\u001b[{};{}H'.format(r, c))

def backspace():
  global col, row
  col -= 1
  if col == -1:
    row -= 1 if row > 0 else 0
  write_at('', row, col)

def next_pos():
  global row, col, window_columns
  col += 1
  if col > window_columns:
    col = 1
    row += 1
  move_to(row, col)

def up():
  global row
  if row: row -=1
  move_to(row, col)

def down():
  global row, window_rows
  if row < window_rows: row += 1
  move_to(row, col)

def right():
  global col, window_columns
  if col < window_columns: col += 1
  move_to(row, col)

def left():
  global col
  if col: col -= 1
  move_to(row, col)

def handle_key(k, standalone=False):
  if k == 58: # ':'
    cmd_col = 1
    move_to(window_rows, 1)
    sys.stdout.write(u'\u001b[2K')
    write_at(':', window_rows, 1)
    command = ''
    while True:
      k = getch()
      if k == 13: # '\n'
        write_at('Invalid command: {}'.format(command), window_rows, 1)
        if command == 'q':
          exit()
        break
      cmd_col += 1
      write_at(chr(k), window_rows, cmd_col)
      command += chr(k)
  elif k == 27 and not standalone: # arrow key code start
    if getch() == 91:
      next1 = getch()
      if next1 == 65: up()
      elif next1 == 66: down()
      elif next1 == 67: right()
      elif next1 == 68: left()
    else: handle_key(k, True)
  else:
    write_at(chr(k), row, col)
    next_pos()

def start():
  global col, row
  while True:
    ch = getch()
    handle_key(ch)

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

