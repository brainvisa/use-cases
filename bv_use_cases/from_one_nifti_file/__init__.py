import os
from soma.controller import path, directory, List, field
from capsul.api import Process

class ListDirectory(Process):
    '''
    Return a list containing the names of the files in the directory.
    '''
    path : directory(doc='directory to list')
    result : field(List[path()], doc='the output', output=True)

    def execute(self, context):
        self.result = os.listdir(self.path)


def list_directory(
        path:   directory(doc='directory to list')
    ) -> List[path()]:
    '''
    Return a list containing the names of the files in the directory.
    '''
    return os.listdir(path)
