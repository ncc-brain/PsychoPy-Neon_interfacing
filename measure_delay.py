"""
Minimal example to measure the delay between the presentation PC and Neon.
"""
NEON_ADDRESS = "192.168.144.57"
NEON_PORT = "8080"
N_segment = 10

from psychopy import core
import sys
import time
from pupil_labs.realtime_api.simple import Device
import numpy as np
from matplotlib import pyplot as plt

try:
    device = Device(address=NEON_ADDRESS, port=NEON_PORT)
except:
    print("Could not connect to Neon.")
    sys.exit()

print("Starting Neon streaming...")
device.streaming_start()

for i in range(N_segment):
    print(f"Segment {i+1}/{N_segment}")
    estimate = device.estimate_time_offset()
    print(f"Mean offset: {estimate.time_offset_ms.mean} ms, Median offset: {estimate.time_offset_ms.median} ms")
    print(f"Standard deviation: {estimate.time_offset_ms.std:.2f} ms")
    core.wait(1)

device.close()