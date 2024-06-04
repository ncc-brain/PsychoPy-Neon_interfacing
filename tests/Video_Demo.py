from psychopy import visual, event, core
from PIL import Image
import numpy as np
import cv2
import time

def desaturate_area(coloration, scale_factor, image_np, center, radius, blur_std, win_size_factor):
    radius = int(radius*scale_factor)
    blur_std = int(blur_std*scale_factor)

    # Convert the normalized image (0-1) to 0-255 and to BGR
    image = (image_np[:, :, ::-1] * 255).astype(np.uint8)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Convert grayscale image back to BGR for compatibility
    gray = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    win_size=radius + blur_std*win_size_factor

    # Calculate the boundaries of the window
    x_min = max(0, int(center[0]) - win_size)
    y_min = max(0, int(center[1]) - win_size)
    x_max = max(0, min(image.shape[1], int(center[0]) + win_size))
    y_max = max(0, min(image.shape[0], int(center[1]) + win_size))

    center_mask = (int(center[0] - x_min), int(center[1] - y_min))

    # Check if the window is valid
    if x_min < x_max and y_min < y_max:
        # Create a mask with a radial gradient centered on the center position
        mask = np.zeros((y_max-y_min, x_max-x_min), dtype=np.float32)
        if mask.shape[1] != 0 and mask.shape[0] !=0:
            y,x = np.ogrid[-center_mask[1]:y_max-y_min-center_mask[1], -center_mask[0]:x_max-x_min-center_mask[0]]
            dist_from_center = np.sqrt(x*x + y*y)
        
            # Define the radius of the plateau
            plateau_radius = radius / 2.0  # Adjust as needed

            # Create a mask with a plateau of full desaturation and a smooth gradient
            mask = np.piecewise(dist_from_center, [dist_from_center <= plateau_radius, dist_from_center > plateau_radius], 
                            [1, lambda x: np.exp(-((x-plateau_radius)**2) / (2.0*blur_std*blur_std))])

            # Convert the mask back to uint8
            mask = mask / np.max(mask)

            # Create a copy of the original image
            image_copy = image.copy()

            if coloration:
                # Apply the mask to the grayscale image for coloration
                image_copy = gray.copy()
                image_copy[y_min:y_max, x_min:x_max] = mask[:,:,None] * image[y_min:y_max, x_min:x_max] + (1 - mask[:,:,None]) * gray[y_min:y_max, x_min:x_max]
            else:
                # Apply the mask to the original image for discoloration
                image_copy[y_min:y_max, x_min:x_max] = mask[:,:,None] * gray[y_min:y_max, x_min:x_max] + (1 - mask[:,:,None]) * image[y_min:y_max, x_min:x_max]

            return image_copy/255.0
    else:
        if coloration:
            return gray/255.0
        else:
            return image/255.0

# Setup PsychoPy window
win = visual.Window(fullscr=True, color=[1, 1, 1], units='pix')
win_size = win.size

height, width = win.size
win_size = win.size

image_size_factor=1
image_compress_factor=0.6

# Load the video using OpenCV
video_path = 'materials/newborn_cats.mp4'
cap = cv2.VideoCapture(video_path)

# Get the frame rate of the video
frame_rate = cap.get(cv2.CAP_PROP_FPS)

# Time per frame (in seconds)
time_per_frame = 1.0 / frame_rate

print(f"The original video is being played at {frame_rate} frames per second.")


# Create a mouse object
mouse = event.Mouse(visible=True, win=win)

# Create ImageStim for displaying frames
frame_texture = visual.ImageStim(win, image=None, size=(int(image_size_factor*height), int(image_size_factor*width)))

# Create a switch for coloration or discoloration
coloration = False  # Set to True for coloration, False for discoloration

start_time = time.time()
frame_count = 0
# Main loop for displaying frames
while cap.isOpened() and not event.getKeys(keyList=['escape']):
    loop_start_time=time.time()

    ret, frame = cap.read()
    if not ret or frame is None:
        break

    frame = cv2.resize(frame, (int(image_compress_factor*height), int(image_compress_factor*width))) # Resize to fit the window
    frame_np = np.flip(np.array(frame),0) / 255.0  # Convert to numpy array and normalize
    

    # Process the frame (e.g., modify, desaturate, etc.)
    # Here, we convert the frame to RGB format for PsychoPy

    # Desaturate area around mouse position
    mouse_pos = mouse.getPos()
    mouse_pos = (mouse_pos[0] + height/2*image_size_factor, mouse_pos[1]+width/2*image_size_factor)  # Convert to image coordinates
    mouse_pos_compress = ((mouse_pos[0])*image_compress_factor, (mouse_pos[1])*image_compress_factor)  # Convert to image coordinates

    desaturated_frame = desaturate_area(True, image_compress_factor/image_size_factor, frame_np, mouse_pos_compress, 100, 100, 3)

    # Update the ImageStim with the modified frame
    frame_texture.setImage(desaturated_frame)
    frame_texture.draw()
    win.flip()

    frame_count += 1

    # Wait for the appropriate amount of time before displaying the next frame
    core.wait(time_per_frame-(time.time() - loop_start_time))

end_time = time.time()
elapsed_time = end_time - start_time
displayed_frame_rate = frame_count / elapsed_time

print(f"The frames were displayed at {displayed_frame_rate} frames per second.")

# Release the video capture and close the window
cap.release()
win.close()
core.quit()