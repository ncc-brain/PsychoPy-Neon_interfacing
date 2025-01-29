"""
Minimal example of presentation PC control of Neon.
Only setup required is to have Neon connected to the companion device and
the correct address and port specified below.
Start and stop of recording as well as sending events are fully automated.
"""
address = "192.168.144.57"
port = "8080"

from psychopy import core, visual, event
import sys
import time
from pupil_labs.realtime_api.simple import Device

try:
    device = Device(address=address, port=port)
except:
    print("Could not connect to Neon.")
    sys.exit()

N = 20
win = visual.Window(screen=-1, fullscr=True, units="height")
win.mouseVisible = False
circle = visual.Circle(win, radius=.2, fillColor="red", lineColor="white")
text = visual.TextStim(win, text="Press space to start", height=.05)

text.draw()
win.flip()
event.waitKeys(keyList=["space"]) 
win.flip()
device.recording_start()
core.wait(5)

# KEY CODE TO ESTIMATE NEON CLOCK OFFSET
# RECOMMEND TO PERFORRM THIS DURING INTER-TRIAL INTERVALS
estimate = device.estimate_time_offset()
clock_offset_ns = round(estimate.time_offset_ms.mean * 1_000_000)
print(f"Clock offset: {clock_offset_ns/1e6} ms")

for i in range(N):
    circle.draw()
    win.flip()
    
    # KEY CODE TO SEND EVENT TO NEON
    device.send_event(
        "Circle onset",
        event_timestamp_unix_ns=int(time.time_ns() - clock_offset_ns)
        )
    core.wait(1)
    win.flip()
    core.wait(1)

device.recording_stop_and_save()
core.wait(1)
win.close()
core.quit()