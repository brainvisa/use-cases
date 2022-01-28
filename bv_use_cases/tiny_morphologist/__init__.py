from soma.controller import field, file
from capsul.api import Process, Pipeline


class BiasCorrection(Process):
    input: field(type_=file())
    strength: float = 0.8
    output: field(type_=file(), output=True)

    def execute(self):
        with open(self.input) as f:
            content = self.read()
        content = f'{content}\nBias correction with strength={self.strength}'
        with open(self.output, 'w') as f:
            f.write(content)

class SPMNormalization(Process):
    input: field(type_=file())
    template: field(type_=file())
    output: field(type_=file(), output=True)

    def execute(self):
        with open(self.input) as f:
            content = self.read()
        content = f'{content}\nSPM normalization with template "{self.template}"'
        with open(self.output, 'w') as f:
            f.write(content)

class AimsNormalization(Process):
    input: field(type_=file())
    origin: field(type_=list[float], default_factory=lambda: [1.2, 3.4, 5.6])
    output: field(type_=file(), output=True)

    def execute(self):
        with open(self.input) as f:
            content = self.read()
        content = f'{content}\nSPM normalization with origin={self.origin}'
        with open(self.output, 'w') as f:
            f.write(content)

class SplitBrain(Process):
    input: field(type_=file())
    right_output: field(type_=file(), output=True)
    left_output: field(type_=file(), output=True)

    def execute(self):
        with open(self.input) as f:
            content = self.read()
        content = f'{content}\nBias correction with strength={self.strength}'
        with open(self.output, 'w') as f:
            f.write(content)


class ProcessHemisphere(Process):
    input: field(type_=file())
    output: field(type_=file(), output=True)

    def execute(self):
        with open(self.input) as f:
            content = self.read()
        content = f'{content}\nProcess hemisphere'
        with open(self.output, 'w') as f:
            f.write(content)

class TinyMorphologist(Pipeline):
    def pipeline_definition(self):
        self.add_process('nobias', BiasCorrection)
        self.add_switch('normalization', ['none', 'spm', 'aims'], ['output'])
        self.add_process('spm_normalization', SPMNormalization)
        self.add_process('aims_normalization', AimsNormalization)
        self.add_process('split', SplitBrain)
        self.add_process('right_hemi', ProcessHemisphere)
        self.add_process('left_hemi', ProcessHemisphere)

        self.add_link('nobias.output->normalization.none_switch_output')
        
        self.add_link('nobias.output->spm_normalization.input')
        self.add_link('spm_normalization.output->normalization.spm_switch_output')

        self.add_link('nobias.output->aims_normalization.input')
        self.add_link('aims_normalization.output->normalization.aims_switch_output')
        
        self.add_link('normalization.output->split.input')
        self.add_link('split.right_output->right_hemi.input')
        self.export_parameter('right_hemi', 'output', 'right_hemisphere')
        self.add_link('split.left_output->left_hemi.input')
        self.export_parameter('left_hemi', 'output', 'left_hemisphere')


