#!/usr/bin/python3

from pathlib import Path
from subprocess import PIPE, run

examples = [
  x for x in Path(__file__).parent.iterdir() if x.is_dir() and (x / 'CMakeLists.txt').exists()
]

assert(len(examples) > 0)

def runCommand(command):
  print('- %s' % command)
  result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
  if result.returncode != 0:
    print("error while running '%s':\n" % command, '  ' + str(result.stderr).replace('\n','\n  '))
    exit(result.returncode)
  return result.stdout

print('')
for example in examples:
  print("running example %s" % example.name)
  print("================" + ('=' * len(example.name)))
  project = Path(".") / 'build' / example.name
  configure = runCommand('cmake -H%s -B%s -DCMAKE_BUILD_TYPE=RelWithDebInfo' % (example, project))
  print('  ' + '\n  '.join([line for line in configure.split('\n') if 'CPM:' in line]))
  build = runCommand('cmake --build %s -j4' % (project))
  print('  ' + '\n  '.join([line for line in build.split('\n') if 'Built target' in line]))
  print('')
