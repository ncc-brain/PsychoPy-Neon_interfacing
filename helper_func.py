import sys
from pathlib import Path
from string import ascii_letters
from typing import Union, Optional
from pprint import pprint
from psychopy import core, visual, gui
from pupil_labs.realtime_api import Device


class MyExp:
    """A class to store experiment parameters and methods"""

    def __init__(
        self,
        sub: str,
        task: str,
        run: Union[int, str],
        use_neon: bool = False,
        neon_address: Optional[str] = None,
        neon_port: Optional[Union[int, str]] = None,
    ):
        run = str(run)

        # BIDS-like naming
        self.sub = sub
        self.task = task
        self.run = run
        self.prefix = f"sub-{sub}_task-{task}_run-{run}"

        # Data directories and files
        self.sub_dir = Path("data") / ("sub-" + sub)
        self.beh_dir = self.sub_dir / "beh"
        if not self.beh_dir.exists():
            self.beh_dir.mkdir(parents=True)
        self.beh_tsv = self.beh_dir / (self.prefix + "_beh.tsv")
        self._check_duplicate()

        # Neon settings
        self.use_neon = use_neon
        if use_neon:
            if neon_address is None or neon_port is None:
                # Get Neon address and port from user
                dlg = gui.Dlg()
                dlg.addField("Neon address", "192.168.144")
                dlg.addField("Neon port", "8080")
                dlg_data = dlg.show()
                sys.exit() if not dlg.OK else None
                neon_address = str(dlg_data[0])
                neon_port = str(dlg_data[1])
            self.neon_address = neon_address
            self.neon_port = neon_port
            self.neon = Device(address=neon_address, port=neon_port)
        else:
            self.neon = self.neon_address = self.neon_port = None

        self.quit_keys = "escape"
        self.clock = core.Clock()
        print("\nExperiment parameters:")
        pprint(vars(self))

    def _check_duplicate(self):
        if self.beh_tsv.exists():
            dlg = gui.Dlg(title="WARNING: Existing run data")
            dlg.addText(f"{self.beh_tsv} already exists")
            dlg.addField(
                "How would you like to proceed?", choices=["Overwrite", "New files"]
            )
            dlg_data = dlg.show()
            sys.exit() if not dlg.OK else None

            if dlg_data[0] == "Overwrite":
                print(f"Overwriting existing run-{self.run} data")
            else:
                print(f"Trying to find a substitute name for run-{self.run}")
                for a in ascii_letters:
                    run = self.run + a
                    prefix = f"sub-{self.sub}_task-{self.task}_run-{run}"
                    tsv = self.beh_dir / (prefix + "_beh.tsv")
                    if not tsv.exists():
                        break

                self.__init__(
                    self.sub,
                    self.task,
                    run,
                    self.use_neon,
                    self.neon_address,
                    self.neon_port,
                )

    def activate_win(self):
        """Define a full-screen window for presentation"""
        self.win = visual.Window(screen=-1, fullscr=True)
        self.win.mouseVisible = False
        self.win.winHandle.activate()

    def win_flip_with_neon_event(self, event_name: str):
        """Flip the window and send a Neon event if applicable"""
        if self.use_neon and self.neon is not None:
            self.win.callOnFlip(
                self.neon.send_event,
                event_name,
                event_timestamp_unix_ns=int(core.getTime() * 1e9),
            )
        self.win.flip()
