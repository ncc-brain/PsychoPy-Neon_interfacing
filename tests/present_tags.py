import os
from psychopy import visual, core, event

DIR_TAG = os.path.join('AprilTags', 'tag36h11')
TAG_SIZE = 0.1

win = visual.Window(fullscr=True, units='height')
height_in_pixels = win.size[1]/2
width_in_height = win.size[0]/win.size[1]
print(f'height_in_pixels: {height_in_pixels}')
print(f'width_in_pixels: {width_in_height*height_in_pixels}')

pos_list = [
    # Top row
    (-0.5*width_in_height, 0.5), (0, 0.5), (0.5*width_in_height, 0.5),
    # Middle row
    (-0.5*width_in_height, 0), (0.5*width_in_height, 0),
    # Bottom row
    (-0.5*width_in_height, -0.5), (0, -0.5), (0.5*width_in_height, -0.5)
]
anchor_list = [
    # Top row
    'top-left', 'top-center', 'top-right',
    # Middle row
    'center-left', 'center-right',
    # Bottom row
    'bottom-left', 'bottom-center', 'bottom-right'
]

tags = [
    visual.ImageStim(
        win,
        image=os.path.join(DIR_TAG, f'tag36_11_{i:05d}.png'),
        size=TAG_SIZE,
        pos=pos_list[i],
        anchor=anchor_list[i]
        )
        for i in range(0, 8)
    ]

text = visual.TextStim(
    win,
    text='Press space to show the tags',
    height=0.05
    )

text.draw()
win.flip()
while True:
    if 'space' in event.getKeys():
        break

for tag in tags:
    tag.draw()
text.setText('Press space to close the window')
text.draw()
win.flip()
while True:
    if 'space' in event.getKeys():
        break

win.close()
exit() 