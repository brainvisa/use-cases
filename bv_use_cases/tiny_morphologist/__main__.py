import os
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
tmp = tempfile.mkdtemp()
try:
    # Create BIDS directory
    bids = f'{tmp}/bids'
    # Write Capsul specific information
    os.mkdir(bids)
    with open(f'{bids}/capsul.json', 'w') as f:
        json.dump({
            'paths_layout': 'bids-1.6'
        }, f)

    # Create BrainVISA directory
    brainvisa = f'{tmp}/brainvisa'
    os.mkdir(brainvisa)
    # Write Capsul specific information
    with open(f'{brainvisa}/capsul.json', 'w') as f:
        json.dump({
            'paths_layout': 'brainvisa-6.0'
        }, f)

    # Generate fake T1 and T2 data in bids directory
    for subject in subjects:
        for session in ('m0', 'm12', 'm24'):
            for data_type in ('T1w', 'T2w'):
                file = f'{bids}/rawdata/sub-{subject}/ses-{session}/anat/sub-{subject}_ses-{session}_{data_type}.nii'
                d = os.path.dirname(file)
                if not os.path.exists(d):
                    os.makedirs(d)
                with open(file, 'w') as f:
                    print(f'{data_type} acquisition for subject {subject} acquired in session {session}', file=f)

    capsul = Capsul()
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
    for t1_mri in dataset.find(suffix='T1w'):
        # Create a TinyMorphologist pipeline
        tiny_morphologist = capsul.executable('bv_use_cases.tiny_morphologist.TinyMorphologist')
        # Set the input data
        tiny_morphologist.input = t1_mri.path
        # Complete outputs following BraiVISA organization
        # Make the link between BIDS metadata and BrainVISA metadata 
        output_dataset.set_output_paths(tiny_morphologist,
            subject=t1_mri.sub,
            acquisition=t1_mri.acq,
        )
        # Add the current TinyMorhpologist pipeline to the main
        # pipeline that will be executed
        custom_pipeline.add_executable(tiny_morphologist)
    # Finally execute all the TinyMorphologist instances
    capsul.run(processing_pipeline)
finally:
    shutil.rmtree(tmp)
