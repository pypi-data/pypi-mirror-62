from subprocess import Popen, PIPE
import shlex

def run_command(command):
  process = Popen(shlex.split(command), stdout=PIPE, stderr=PIPE, universal_newlines=True)
  while True:
      print(process.stderr.readline())
      output = process.stdout.readline()
      if output == '' and process.poll() is not None:
          break
      if output:
          print(output.strip())
  rc = process.poll()
  return rc

def run_with_pipe(command):
  commands = list(map(shlex.split,command.split("|")))
  ps = Popen(commands[0], stdout=PIPE, stderr=PIPE)
  for command in commands[1:]:
    ps = Popen(command, stdin=ps.stdout,stdout=PIPE, stderr=PIPE)
  return ps.stdout.readlines()
