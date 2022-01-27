from pprint import pprint

from capsul.api import Capsul

# Capsul entry point
capsul = Capsul()
# User and site configuration had been read.
# Configuration customization goes here

# An executable (for instance a Process or a Pipeline) must be defined 
# in both the user environment and the execution environment. It is 
# supposed to be the same on both environments. Therefore,
# it is possible to get an executable instance either from a Capsul
# instance (user environment) or from a CapsulEngine instance (execution
# environment, possibly on a remote computer).
executable = capsul.executable('bv_use_cases.simplest.list_directory')
executable.path = '/'

# To be able to run an executable, it is necessary to get a CapsulEngine
# instance. If this instance is remote, it is also necessary to connect to
# the remote server before doing anything. In some cases it may be interesting
# to separate this two steps; for instance if one only wants to see the engine 
# configuration. Therefore, a "with" statement must be used to define portion
# of code requiring a valid connection to the CapsulEngine.

capsul_engine = capsul.engine()
with capsul_engine.connect():
    capsul_engine.run(executable)
    print(executable.result)
# Here the connection to the CapsulEngine is closed. The execution_id may not be
# valid for another connection to the same engine. This is engine implementation
# dependent.