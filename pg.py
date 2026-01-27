from psychopy import core, visual, event
from ezeye import Experiment
from pathlib import Path
from random import shuffle

FIX_SIZE = 100
IMG_SIZE = (1200, 800)
IMG_DURATION = 4

exp = Experiment(
    dataset="EzEyeTestDataset",
    subject="MPUTC01",
    task="aruco",
    session="01",
    data_type="ieeg",
    use_pupil_labs=True,
)
exp.win.mouseVisible = False
exp.win.winHandle.activate()

text_stim = visual.TextStim(
    exp.win,
    text="Press SPACE to begin the experiment",
    color="white",
)

fix_cross = visual.ShapeStim(
    exp.win, vertices="cross", fillColor="white", lineColor=None, size=FIX_SIZE, units="pix"
)
img = visual.ImageStim(exp.win, size=IMG_SIZE, units="pix")
stimuli_dir = Path("stimuli")
img_paths = list(stimuli_dir.glob("*.jpg"))
shuffle(img_paths)

text_stim.draw()
exp.win.flip()
event.waitKeys(keyList=["space"])
exp.win.flip()

exp.start_recording()
core.wait(4)

exp.draw_markers("5x5_250", 8)
exp.log_event(win_flip=True, trial_type="draw ArUco markers")
core.wait(3)

# First 5 stimuli
for img_path in img_paths[:5]:
    img.image = str(img_path)
    fix_cross.draw()
    exp.log_event(
        win_flip=True,
        trial_type="fixation",
    )
    core.wait(.5)

    img.draw()
    exp.log_event(
        win_flip=True,
        trial_type="image",
    )
    core.wait(IMG_DURATION)
    
    exp.win.flip()
    core.wait(1)
    
    keys = event.getKeys(['escape'])
    if 'escape' in keys:
        exp.end()

exp.end()
