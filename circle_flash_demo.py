"""
Minimal example of presentation PC control of Neon.
Only setup required is to have Neon connected to the companion device and
the correct address and port specified below.
Start and stop of recording as well as sending events are fully automated.
"""
NEON_ADDRESS = "192.168.144.11"
NEON_PORT = "8080"

from psychopy import core, visual, event
import sys
import time
from pupil_labs.realtime_api.simple import Device

try:
    device = Device(address=NEON_ADDRESS, port=NEON_PORT)
except:
    print("Could not connect to Neon.")
    sys.exit()

N = 10
win = visual.Window(screen=-1, fullscr=True, units="height", color=[0, 0, 0])
win.mouseVisible = False
# circle = visual.Circle(win, radius=.2, fillColor="red", lineColor="white")
square = visual.Rect(win, width=2, height=2, fillColor="white", lineColor="white", units="norm")
text = visual.TextStim(win, text="Press space to start", height=.05)

text.draw()
win.flip()
event.waitKeys(keyList=["space"]) 
text.setText("Starting...")
win.flip()
device.recording_start()
core.wait(3)

# KEY CODE TO ESTIMATE NEON CLOCK OFFSET
# RECOMMEND TO PERFORRM THIS DURING INTER-TRIAL INTERVALS
estimate = device.estimate_time_offset()
clock_offset_ns = round(estimate.time_offset_ms.median * 1_000_000)
print(f"Clock median offset: {clock_offset_ns/1e6} ms")

for i in range(N):
    square.draw()
    win.flip()
    
    # KEY CODE TO SEND EVENT TO NEON
    device.send_event(
        "Circle onset",
        event_timestamp_unix_ns=int(time.time_ns() - clock_offset_ns)
        )
    core.wait(2)
    win.flip()
    core.wait(2)

device.recording_stop_and_save()
core.wait(1)
win.close()
core.quit()