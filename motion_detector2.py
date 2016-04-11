# import the necessary packages
from __future__ import print_function
from imutils.object_detection import non_max_suppression
import argparse
import datetime
import imutils
import numpy as np
import time
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())

# if the video argument is None, then we are reading from webcam
if args.get("video", None) is None:
	camera = cv2.VideoCapture(0)
	time.sleep(0.25)

# otherwise, we are reading from a video file
else:
	camera = cv2.VideoCapture(args["video"])

#camera.set(3, 1920)
#camera.set(4, 1080)

# Get the width and height of frame
width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'X264') 
# used for recording identified threats
out = cv2.VideoWriter('events.avi', fourcc, 10, (width, height))
# the full recording
full_log_out = cv2.VideoWriter('full_log.avi', fourcc, 10, (width, height))

# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# initialize the first frame in the video stream
firstFrame = None

# loop over the frames of the video
while True:
	# grab the current frame and initialize the occupied/unoccupied
	# text
	(grabbed, frame) = camera.read()
	text = "Unoccupied"

	# if the frame could not be grabbed, then we have reached the end
	# of the video
	if not grabbed:
		break

	# resize the frame, convert it to grayscale, and blur it
	frame = imutils.resize(frame, width=min(width, frame.shape[1]))	

	# write date and time to frame
	cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
		(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)		

	# detect people in the image
	(rects, weights) = hog.detectMultiScale(frame, winStride=(8, 8),
		padding=(32, 32), scale=1.05)	

	# apply non-maxima suppression to the bounding boxes using a
	# fairly large overlap threshold to try to maintain overlapping
	# boxes that are still people
	rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
	pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

	# draw the final bounding boxes
	for (xA, yA, xB, yB) in pick:
		cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)	

	# write to video file if a human has been found
	if len(pick) != 0: 
		# write frame to file
		out.write(frame)

	full_log_out.write(frame)			

	# show the frame and record if the user presses a key
	cv2.imshow("Security Feed", frame)

	key = cv2.waitKey(1) & 0xFF

	# if the `q` key is pressed, exit loop
	if key == ord("q"):
		break

# cleanup the camera and close any open windows
camera.release()
out.release()
cv2.destroyAllWindows()