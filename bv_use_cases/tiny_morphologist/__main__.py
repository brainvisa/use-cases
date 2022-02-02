# -*- coding: utf-8 -*-
import json
import os
from pathlib import Path
import shutil
import tempfile

from bv_use_cases import tiny_morphologist

from capsul.api import Capsul

subjects = (
    'aleksander',
    'casimiro',
    'christophorus',
    'christy',
    'conchobhar',
    'cornelia',
    'dakila',
    'demosthenes',
    'devin',
    'ferit',
    'gautam',
    'hikmat',
    'isbel',
    'ivona',
    'jordana',
    'justyn',
    'katrina',
    'lyda',
    'melite',
    'mina',
    'odalric',
    'rainbow',
    'rashn',
    'shufen',
    'simona',
    'svanhildur',
    'thilini',
    'til',
    'vanessza',
    'victoria'
)

# Create temporary directory for the use case
tmp_name = tempfile.mkdtemp()
try:
    #-------------------#
    # Environment setup #
    #-------------------#

    tmp = Path(tmp_name) 
    # Create BIDS directory
    bids = tmp / 'bids'
    # Write Capsul specific information
    bids.mkdir()
    with (bids / 'capsul.json').open('w') as f:
        json.dump({
            'path_layout': 'bids-1.6'
        }, f)

    # Create BrainVISA directory
    brainvisa = tmp / 'brainvisa'
    brainvisa.mkdir()
    # Write Capsul specific information
    with (brainvisa / 'capsul.json').open('w') as f:
        json.dump({
            'path_layout': 'brainvisa-6.0'
        }, f)

    # Generate fake T1 and T2 data in bids directory
    for subject in subjects:
        for session in ('m0', 'm12', 'm24'):
            for data_type in ('T1w', 'T2w'):
                file = (bids/ f'rawdata' / f'sub-{subject}' / f'ses-{session}' / 'anat' /
                        f'sub-{subject}_ses-{session}_{data_type}.nii')
                file.parent.mkdir(parents=True, exist_ok=True)
                with file.open('w') as f:
                    print(f'{data_type} acquisition for subject {subject} acquired in session {session}', file=f)

    # Configuration base dictionary
    config = {
        'default': {
            'label': 'Local computer',
            'modules': {}
        }
    }
    # Create fake SPM directories
    for version in ('8', '12'):
        spm = tmp / 'software' / f'fakespm-{version}'
        spm.mkdir(parents=True, exist_ok=True)
        # Write a file containing only the version string that will be used
        # by fakespm module to check installation.
        (spm / 'spm').write_text(version)
        fakespm_config = {
            'directory': str(spm),
            'version': version,
        }
        config['default']['modules'].setdefault('fakespm', []).append(fakespm_config)
        

    # Create a configuration file
    config_json = tmp / 'capsul_config.json'
    with config_json.open('w') as f:
        json.dump(config, f)
    

    #---------------------#
    # Pipelines execution #
    #---------------------#

    capsul = Capsul(config_file=config_json)
    # Input dataset is declared as following BIDS organization in capsul.json
    # therefore a BIDS specific object is returned
    input_dataset = capsul.dataset(bids)
    # Output dataset is declared as following BrainVISA organization in capsul.json
    # therefore a BrainVISA specific object is returned
    output_dataset = capsul.dataset(brainvisa)
    # Create a main pipeline that will contain all the morphologist pipelines
    # we want to execute
    processing_pipeline = capsul.custom_pipeline()
    # Parse the dataset with BIDS-specific query (here "suffix" is part
    #  of BIDS specification). The object returned contains info for main
    # BIDS fields (sub, ses, acq, etc.)
    count = 0
    for t1_mri in input_dataset.find(suffix='T1w'):
        # Create a TinyMorphologist pipeline
        tiny_morphologist = capsul.executable('bv_use_cases.tiny_morphologist.TinyMorphologist')
        # Set the input data
        tiny_morphologist.input = t1_mri['path']
        # Complete outputs following BraiVISA organization
        # Make the link between BIDS metadata and BrainVISA metadata 
        output_dataset.set_output_paths(tiny_morphologist,
            subject=t1_mri['sub'],
            acquisition=t1_mri.get('acq', 'default'),
        )
        # Add the current TinyMorhpologist pipeline to the main
        # pipeline that will be executed
        processing_pipeline.add_process(f'pipeline_{count}', tiny_morphologist)
        count = count + 1
    # # Finally execute all the TinyMorphologist instances
    # capsul.run(processing_pipeline)
finally:
    shutil.rmtree(tmp)
