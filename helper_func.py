import sys, os
import pandas as pd
import numpy as np
from string import ascii_letters, digits
from typing import Union
from pprint import pprint
from psychopy import core, visual, event, gui
import pupil_labs.realtime_api as plapi


class MyExp:
    '''A class to store experiment parameters and methods'''

    def __init__(self,
                 sub: str,
                 task: str,
                 run: Union[int, str],
                 eye: bool=False,
                 neon_ip: str="192.168.1.169",
                 neon_port: Union[int, str]=8080
                 ):
        
        run = str(run)
        neon_port = str(neon_port)
        
        self.sub    = sub
        self.task   = task
        self.run    = run
        self.prefix = 'sub-'+ sub + '_task-' + task + '_run-' + run

        self.sub_dir  = os.path.join('data', 'sub-' + sub)
        self.beh_dir  = os.path.join(self.sub_dir, 'beh')
        if not os.path.exists(self.beh_dir):
            os.makedirs(self.beh_dir)
        self.tsv = os.path.join(self.beh_dir, self.prefix + '_beh.tsv')

        self.eye = eye

        self.quit_keys = "escape"
        self.clock = core.Clock()
        
        if eye:
            self.eye_dir  = os.path.join(self.sub_dir, 'eyetrack')
            if not os.path.exists(self.eye_dir):
                os.makedirs(self.eye_dir)
            
            self.neon_ip = neon_ip
            self.neon_port = neon_port
            self.tracker = plapi.Device(address=neon_ip, port=neon_port)
        else:
            self.tracker = self.neon_ip = self.neon_port = None
        
        print("\nExperiment parameters:")
        pprint(vars(self))
    
    def check_duplicate(self):

        if os.path.exists(self.tsv):
            dlg = gui.Dlg(title='WARNING: Existing run data')
            dlg.addText(f'{self.tsv} already exists')
            dlg.addField('How would you like to proceed?',
                         choices=['Overwrite', 'New files'])
            dlg_data = dlg.show()
            if not dlg.OK: sys.exit()
            
            if dlg_data[0] == 'Overwrite':
                print(f'Overwriting existing run-{self.run} data')
            else:
                print(f'Trying to find a substitute name for run-{self.run}')
                for a in ascii_letters:
                    run = self.run + a
                    prefix = 'sub-'+ self.sub + '_task-' + self.task + '_run-' + run
                    tsv = os.path.join(self.beh_dir, prefix + '_beh.tsv')
                    if not os.path.exists(tsv):
                        break
                
                self.__init__(self.sub,
                              self.task,
                              run,
                              self.eye,
                              self.neon_ip,
                              self.neon_port)
    
    def activate_win(self):
        '''Define a full-screen window for presentation'''
        self.win = visual.Window(screen=-1,
                                 fullscr=True)
        self.win.mouseVisible = False
        self.win.winHandle.activate()
