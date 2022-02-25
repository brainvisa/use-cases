# -*- coding: utf-8 -*-
from pathlib import Path

from soma.controller import field, File

from capsul.api import Process, Pipeline


class BiasCorrection(Process):
    input: field(type_=File)
    strength: float = 0.8
    output: field(type_=File, write=True)

    def execute(self, context):
        with open(self.input) as f:
            content = self.read()
        content = f'{content}\nBias correction with strength={self.strength}'
        with open(self.output, 'w') as f:
            f.write(content)

    path_layout = dict(
        bids={'output': {'part': 'nobias'}},
        brainvisa={'output': {'prefix': 'nobias'}}
    )

class FakeSPMNormalization(Process):
    input: field(type_=File)
    template: field(type_=File)
    output: field(type_=File, write=True)
    
    requirements = {
        'fakespm': {
            'version': '12'
        }
    }
    
    path_layout = dict(
        bids={'output': {'part': 'normalized'}},
        brainvisa={'output': {'prefix': 'normalized'}}
    )

    def execute(self, context):
        fakespmdir = Path(context.fakespm.directory)
        real_version = (fakespmdir / 'fakespm').read_text().strip()
        with open(self.input) as f:
            content = self.read()
        content = f'{content}\nNormalization with fakespm {real_version} installed in {fakespmdir} using template "{self.template}"'
        with open(self.output, 'w') as f:
            f.write(content)

class AimsNormalization(Process):
    input: field(type_=File)
    origin: field(type_=list[float], default_factory=lambda: [1.2, 3.4, 5.6])
    output: field(type_=File, write=True)

    path_layout = dict(
        bids={'output': {'part': 'normalized'}},
        brainvisa={'output': {'prefix': 'normalized'}}
    )

    def execute(self, context):
        with open(self.input) as f:
            content = self.read()
        content = f'{content}\nNormalization with Aims, origin={self.origin}'
        with open(self.output, 'w') as f:
            f.write(content)

class SplitBrain(Process):
    input: field(type_=File)
    right_output: field(type_=File, write=True)
    left_output: field(type_=File, write=True)

    path_layout = dict(
        bids={'output': {'part': 'split'}},
        brainvisa={'output': {'prefix': 'split'}}
    )

    def execute(self, context):
        with open(self.input) as f:
            content = self.read()
        content = f'{content}\nBias correction with strength={self.strength}'
        with open(self.output, 'w') as f:
            f.write(content)


class ProcessHemisphere(Process):
    input: field(type_=File)
    output: field(type_=File, write=True)

    def execute(self, context):
        with open(self.input) as f:
            content = self.read()
        content = f'{content}\nProcess hemisphere'
        with open(self.output, 'w') as f:
            f.write(content)

class TinyMorphologist(Pipeline):
    def pipeline_definition(self):
        self.add_process('nobias', BiasCorrection)

        self.add_switch('normalization', ['none', 'fakespm', 'aims'], ['output'])
        self.add_process('fakespm_normalization', FakeSPMNormalization)
        self.add_process('aims_normalization', AimsNormalization)
        self.add_process('split', SplitBrain)
        self.add_process('right_hemi', ProcessHemisphere)
        self.add_process('left_hemi', ProcessHemisphere)

        self.add_link('nobias.output->normalization.none_switch_output')
        
        self.add_link('nobias.output->fakespm_normalization.input')
        self.add_link('fakespm_normalization.output->normalization.fakespm_switch_output')

        self.add_link('nobias.output->aims_normalization.input')
        self.add_link('aims_normalization.output->normalization.aims_switch_output')

        self.export_parameter('nobias', 'output', 'nobias')

        self.add_link('normalization.output->split.input')
        self.export_parameter('normalization', 'output', 'normalized')
        self.add_link('split.right_output->right_hemi.input')
        self.export_parameter('right_hemi', 'output', 'right_hemisphere')
        self.add_link('split.left_output->left_hemi.input')
        self.export_parameter('left_hemi', 'output', 'left_hemisphere')

    path_layout = dict(
        bids={
            '*': {'pipeline': 'tinymorphologist'},
            'left_hemisphere': {'part': 'left_hemi'},
            'right_hemisphere': {'part': 'right_hemi'},
        },
        brainvisa={
            '*': {'process': 'tinymorphologist'},
            'left_hemisphere': {'prefix': 'left_hemi'},
            'right_hemisphere': {'prefix': 'right_hemi'},
        }
    )


