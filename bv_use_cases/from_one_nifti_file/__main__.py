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
executable.t1w_mri = 'path/to/nifti/file'
executable.output_directory = 'path/to/output/dir' # no explicit database creation
executable.output_prefix = 'prefix'

# To be able to run an executable, it is necessary to get a CapsulEngine
# instance. If this instance is remote, it is also necessary to connect to
# the remote server before doing anything. In some cases it may be interesting
# to separate this two steps; for instance if one only wants to see the engine 
# configuration. Therefore, a "with" statement must be used to define portion
# of code requiring a valid connection to the CapsulEngine.
with capsul.engine() as capsul_engine:
    # Here we are connected to the Capsul engine and can send command to it
    execution_id = capsul_engine.start(executable)
    capsul_engine.wait(execution_id)
    final_status = capsul_engine.status(execution_id)
    pprint(final_status)
    capsul_engine.raise_for_status(final_status)

# Here the connection to the CapsulEngine is closed. The execution_id may not be
# valid for another connection to the same engine. This is engine implementation
# dependent.
