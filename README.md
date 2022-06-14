# use-cases
Use cases for future BrainVISA API

## Using the code

The future [soma-base](https://github.com/populse/soma-base) / [capsul](https://github.com/populse/capsul) libs will need python 3.9. We will thus use the branch "pydantic_controller"

The simplest is to use a [casa-distro](https://github.com/brainvisa/casa-distro) container for developers, and setup a minimalist dev environment, based on an Ubuntu 22.04 container with singularity.

* Please read and follow the instructions there:

[Capsul v3 installation](https://github.com/populse/capsul/tree/pydantic_controller)


* The main module is `bv_use_cases`:

    from bv_use_cases import simplest
