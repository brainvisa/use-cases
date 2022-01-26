# use-cases
Use cases for future BrainVISA API

## Using the code

The future [soma-base](https://github.com/populse/soma-base) / [capsul](https://github.com/populse/capsul) libs will need python 3.9. We will thus use the branch "pydantic_controller"

The simplest is to use a [casa-distro](https://github.com/brainvisa/casa-distro) container for developers, and setup a minimalist dev environment, based on an Ubuntu 22.04 container with singularity:

* [install singularity](https://brainvisa.info/web/download.html#prerequisites-for-singularity-on-linux)

* Go to your "casa_distro" directory:

      mkdir ~/casa_distro  # if you don't have it already
      cd ~/casa_distro

* get the developer image:
    If you already have casa_distro installed:

        casa_distro pull_image image=casa-dev-5.3.sif

    or, otherwise:

        wget https://brainvisa.info/download/casa-dev-5.3.sif

* setup a developer environment:

      mkdir bv_use_cases
      singularity run -B bv_use_cases:/casa/setup casa-dev-5.3.sif distro=opensource

* change the `bv_maker.cfg` file for a ligher one, which switches to the expected branches:

      cat > bv_use_cases/conf/bv_maker.cfg << EOF
      [ source \$CASA_SRC ]
        brainvisa brainvisa-cmake \$CASA_BRANCH
        brainvisa casa-distro \$CASA_BRANCH
        git https://github.com/populse/soma-base.git pydantic_controller soma/soma-base
        git https://github.com/populse/populse_db.git master populse_db
        git https://github.com/populse/capsul.git pydantic_controller capsul
        git https://github.com/brainvisa/use-cases.git master brainvisa/use-cases

      [ build \$CASA_BUILD ]
        default_steps = configure build
        make_options = -j\$NCPU
        build_type = Release
        packaging_thirdparty = OFF
        clean_config = ON
        clean_build = ON
        test_ref_data_dir = \$CASA_TESTS/ref
        test_run_data_dir = \$CASA_TESTS/test
        brainvisa brainvisa-cmake \$CASA_BRANCH \$CASA_SRC
        brainvisa casa-distro \$CASA_BRANCH \$CASA_SRC
        + \$CASA_SRC/soma/soma-base
        + $CASA_SRC/populse_db
        + \$CASA_SRC/capsul
        + \$CASA_SRC/brainvisa/use-cases
      EOF

* get the code and build:

      bv_use_cases/bin/bv_maker

* Temporarily (until we ship it in a newer dev image), you need to install pydantic:

      bv_use_cases/bin/bv pip3 install pydantic

* It's ready. You can us it using either:

      bv_use_cases/bin/bv bash
      bv_use_cases/bin/bv ipython3
      bv_use_cases/bin/bv python <script>

  You can also set the bv_use_cases/bin directory into your `PATH` configuration.

The main module is `bv_use_cases`:

    from bv_use_cases import simplest
