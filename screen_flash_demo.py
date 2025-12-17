from psychopy import core, visual, event, gui
import sys
from time import time_ns
from pupil_labs.realtime_api.simple import Device

# Get Neon address and port from user
dlg = gui.Dlg()
dlg.addField("Neon address", "10.55.60.77")
dlg.addField("Neon port", "8080")
dlg_data = dlg.show()
sys.exit() if not dlg.OK else None
NEON_ADDRESS = dlg_data[0]
NEON_PORT = int(dlg_data[1])

# Initialize the Neon device
try:
    device = Device(address=NEON_ADDRESS, port=NEON_PORT)
except Exception as e:
    print(f"Error connecting to Neon: {e}")
    sys.exit()

# Experiment parameters and PsychoPy objects
N = 5  # Number of trials
win = visual.Window(screen=-1, fullscr=True, units="height", color=[-1, -1, -1])
win.mouseVisible = False
square = visual.Rect(
    win, width=2, height=2, fillColor="white", lineColor="white", units="norm"
)
text = visual.TextStim(win, text="Press space to start", height=0.05)

# Display initial message and wait for space key to continue
text.draw()
win.flip()
event.waitKeys(keyList=["space"])
win.flip()
device.recording_start()
core.wait(3)

# Estimate clock offset
estimate = device.estimate_time_offset().time_offset_ms.median
clock_offset_ns = round(estimate * 1e6)
print(f"Clock median offset: {clock_offset_ns / 1e6} ms")


def send_event(device, clock_offset_ns):
    device.send_event(
        "Flash onset (callOnFlip)",
        event_timestamp_unix_ns=int(time_ns() - clock_offset_ns),
    )


for i in range(N):
    square.draw()
    win.callOnFlip(send_event, device, clock_offset_ns)
    win.flip()
    core.wait(0.5)
    win.flip()
    core.wait(2)

device.recording_stop_and_save()
device.close()
core.quit()
