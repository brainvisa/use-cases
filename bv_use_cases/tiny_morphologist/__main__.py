# -*- coding: utf-8 -*-
import json
import os
from pathlib import Path
import shutil
import tempfile

from bv_use_cases import tiny_morphologist

from capsul.api import Capsul, Process
from capsul.dataset import Completion


# import sys
# import yaql
# spms = [
#     {
#         'version': 8,
#         'directory': '/software/spm8',
#     },
#     {
#         'version': 12,
#         'directory': '/software/spm12',
#     }
# ]

# engine = yaql.factory.YaqlFactory().create()

# expression = engine(
#     '$.where($.version = 12)')
# selected_spm = expression.evaluate(data=spms)
# print(selected_spm)
# sys.exit()

subjects = (
    'aleksander',)
#     'casimiro',
#     'christophorus',
#     'christy',
#     'conchobhar',
#     'cornelia',
#     'dakila',
#     'demosthenes',
#     'devin',
#     'ferit',
#     'gautam',
#     'hikmat',
#     'isbel',
#     'ivona',
#     'jordana',
#     'justyn',
#     'katrina',
#     'lyda',
#     'melite',
#     'mina',
#     'odalric',
#     'rainbow',
#     'rashn',
#     'shufen',
#     'simona',
#     'svanhildur',
#     'thilini',
#     'til',
#     'vanessza',
#     'victoria'
# )

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
        },
        'remote': {
            'label': 'triscotte',
            'type': 'ssh',
            'host': 'triscotte.cea.fr',
            'modules': {}
        }
    }
    # Create fake SPM directories
    for version in ('8', '12'):
        fakespm = tmp / 'software' / f'fakespm-{version}'
        fakespm.mkdir(parents=True, exist_ok=True)
        # Write a file containing only the version string that will be used
        # by fakespm module to check installation.
        (fakespm / 'fakespm').write_text(version)
        fakespm_config = {
            'directory': str(fakespm),
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
    processing_pipeline = capsul.custom_pipeline(autoexport_nodes_parameters=False)

    completion = Completion()
    completion.add_dataset_items({
        output_dataset: {
            'TinyMorphologist': ['nobias', 'normalized',
                                 'right_hemisphere',
                                 'left_hemisphere']},
    })

    # Parse the dataset with BIDS-specific query (here "suffix" is part
    #  of BIDS specification). The object returned contains info for main
    # BIDS fields (sub, ses, acq, etc.)
    count = 0
    for t1_mri in input_dataset.find(suffix='T1w'):
        # Create a TinyMorphologist pipeline
        tiny_morphologist = capsul.executable('bv_use_cases.tiny_morphologist.TinyMorphologist',
                                              normalization='aims')
        # Set the input data
        tiny_morphologist.input = t1_mri['path']
        # Complete outputs following BraiVISA organization
        # Make the link between BIDS metadata and BrainVISA metadata 
        #output_dataset.set_output_paths(tiny_morphologist,
        completion.set_paths(tiny_morphologist,
            center='whaterver',
            subject=t1_mri['sub'],
            acquisition=t1_mri['ses'],
            extension = 'nii'
        )
        # Add the current TinyMorhpologist pipeline to the main
        # pipeline that will be executed
        processing_pipeline.add_process(f'pipeline_{count}', tiny_morphologist)
        print('Created', f'pipeline_{count}')
        for field in tiny_morphologist.fields():
            value = getattr(tiny_morphologist, field.name, None)
            print('   ', ('<-' if field.is_output() else '->'), field.name, '=', value)
        for node_name, node in tiny_morphologist.nodes.items():
            if not node_name:
                continue
            print('   ', node_name, ':', node)
            if isinstance(node,Process):
                for field in node.fields():
                    value = getattr(node, field.name, None)
                    print('       ', ('<-' if field.is_output() else '->'), field.name, '=', value)

        import sys
        sys.stdout.flush()
        from soma.qt_gui.qt_backend import QtGui
        from capsul.qt_gui.widgets import PipelineDeveloperView

        app = QtGui.QApplication.instance()
        if not app:
            app = QtGui.QApplication(sys.argv)
        view1 = PipelineDeveloperView(tiny_morphologist)
        view1.show()
        app.exec_()
        del view1
        sys.exit()

        count = count + 1
    with capsul.engine() as ce:
      # Finally execute all the TinyMorphologist instances
      ce.run(processing_pipeline)
finally:
    shutil.rmtree(tmp)
