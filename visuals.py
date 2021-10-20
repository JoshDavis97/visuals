import os, random, logging, sys, argparse
import cv2

def get_args():
	parser = argparse.ArgumentParser(description='plays random videos from a directory, from a random frame, for a given number of seconds.')
	parser.add_argument(
		"directory",
		metavar = "DIRECTORY",
		type = str,
		help = "the directory to play videos from",
	)

	parser.add_argument(
		"-s",
		"--seconds",
		metavar = "SECONDS",
		type = int,
		default = 15,
		help = "number of seconds to play each clip for, defaults to '15'",
	)

	parser.add_argument(
		"-l",
		"--logging-level",
		choices=["debug", "info", "warning", "error", "critical"],
		default="debug",
		help="logging level, defaults to 'debug'",
	)

	return parser.parse_args()

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

def play_video_clip(filename, length, window_name):

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
			max_frame_index = None

			if video_length > length: #only skip to a random section if vid is longer than the defined clip length
				max_frame_index = int(frame_count - (fps*length)) #max frame index we can start video from, so it doesn't go over the actual video length
				start_frame_index = random.randint(0, max_frame_index) #get a random frame to start from
				end_frame_index = int(start_frame_index + (length * fps))
				cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame_index) #set current position of video to the random start frame

			logging.debug(
				"playing video: filename={}, width={}, height={}, fps={:.2f}, frame_count={}, video_length={:.2f}s, start_frame_index={}, end_frame_index={}, max_frame_index={}".format(
					filename,
					width,
					height,
					fps,
					frame_count,
					video_length,
					start_frame_index,
					end_frame_index,
					max_frame_index,
				)
			)

			while(cap.isOpened()):
				ret, frame = cap.read()
				current_frame_index = cap.get(cv2.CAP_PROP_POS_FRAMES)

				if ret == True and current_frame_index <= end_frame_index:
					#capsize = cv2.resize(frame, (1280,720))
					cv2.imshow(window_name, frame)

					if cv2.waitKey(25) & 0xFF == ord('q'):
						break

				else:
					break

			cap.release()
		else:
			logging.error("error opening file '{}'".format(filename))

def get_absolute_paths(directory):
    for dirpath,_,filenames in os.walk(directory):
        for f in filenames:
            yield os.path.abspath(os.path.join(dirpath, f))

def main():
	args = get_args()
	init_logging(args.logging_level)
	logging.debug(args)

	paths = list(get_absolute_paths(args.directory))
	random_index = random.randint(0, len(paths)-1)
	last_index = None

	window_name = "visuals.py"
	cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
	cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

	while True:
		while random_index == last_index:
			random_index = random.randint(0, len(paths)-1)

		play_video_clip(paths[random_index], args.seconds, window_name)
		last_index = random_index

	cv2.destroyAllWindows()

if __name__ == '__main__':
	main()
