from sys import argv
from functools import reduce

file = argv[1]
startline = argv[2]
endline = argv[3]

with open(argv[1], 'r') as f:
  lines=f.readlines()
  important_lines = []
  state = "stop"
  for line in lines:
    if state == "stop":
      if line[0:3 + len(str(startline))] == "gc " + str(startline):
        state = "running"
        important_lines.append(line)
    else:
      important_lines.append(line)
      if line[0:3 + len(str(endline))] == "gc " + str(endline):
        break
  lines = important_lines

  def get_time(line):
    start = line.index(', ') + 2
    end = line.index(' ms cpu')

    start, middle, end = line[start:end].split("+")
    assist, bg, idle = middle.split("/")

    return float(start), float(assist), float(bg), float(idle), float(end)

  m = list(map(lambda line:sum(get_time(line)), lines))
  val = reduce((lambda x, y: x + y), m)
  print(val)
