import os, random, logging, sys
import cv2

def init_logging(logging_level):
	logging_levels = {
		"debug" 	: logging.DEBUG,
		"info" 		: logging.INFO,
		"warning"	: logging.WARNING,
		"error" 	: logging.ERROR,
		"critical" 	: logging.CRITICAL,
	}

	logger = logging.getLogger()
	formatter = logging.Formatter("%(asctime)s\t%(levelname)s\t%(message)s")

	logger.setLevel(logging_levels[logging_level])

	stdout_handler = logging.StreamHandler(sys.stdout)
	stdout_handler.setLevel(logging.DEBUG)
	stdout_handler.setFormatter(formatter)
	logger.addHandler(stdout_handler)

	logging.debug("loaded logging")

def play_video_clip(filename, length):
	if ".mp4" in filename:
		cap = cv2.VideoCapture(filename)

		if cap.isOpened():
			width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
			height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
			fps = cap.get(cv2.CAP_PROP_FPS)
			frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
			video_length = frame_count/fps
			start_frame_index = 0
			end_frame_index = frame_count

			logging.debug(
				"filename={},width={},height={},fps={},frame_count={},video_length={}s".format(
					filename,
					width,
					height,
					fps,
					frame_count,
					video_length,
				)
			)

			if video_length > length: #only skip to a random section if vid is longer than the defined clip length
				max_frame_index = int(frame_count - (fps*length)) #max frame index we can start video from, so it doesn't go over the actual video length
				start_frame_index = random.randint(0, max_frame_index) #get a random frame to start from
				end_frame_index = start_frame_index + (length * fps)
				cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame_index) #set current position of video to the random start frame

				logging.debug(
					"start_frame_index={},end_frame_index={},max_frame_index={}".format(
						start_frame_index,
						end_frame_index,
						max_frame_index,
					)
				)

			while(cap.isOpened()):
				ret, frame = cap.read()

				#logging.debug(cap.get(cv2.CAP_PROP_POS_FRAMES))

				if ret == True and cap.get(cv2.CAP_PROP_POS_FRAMES) <= end_frame_index:
					capsize = cv2.resize(frame, (800,600))
					cv2.imshow('Frame', capsize)

					if cv2.waitKey(25) & 0xFF == ord('q'):
						break

				else:
					break

			cap.release()
		else:
			logging.error("error opening video file")

def main():
	init_logging("debug")
	directory = os.path.dirname(os.path.abspath( __file__ ))

	while True:
		list = os.listdir(directory)
		random.shuffle(list)
		for filename in list:
			play_video_clip(filename, 5)

	cv2.destroyAllWindows()

if __name__ == '__main__':
	main()
