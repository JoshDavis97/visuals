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

def play_random_video(directory):
	list = os.listdir(directory)
	random.shuffle(list)

	for filename in list:
		if ".mp4" in filename:
			cap = cv2.VideoCapture(filename)

			if not cap.isOpened():
				logging.error("error opening video file")

			width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
			height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
			fps = cap.get(cv2.CAP_PROP_FPS)
			frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
			video_length = frame_count/30

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

			while(cap.isOpened()):
				ret, frame = cap.read()



				if ret == True:
					capsize = cv2.resize(frame, (1920,1080))
					cv2.imshow('Frame', capsize)

					if cv2.waitKey(25) & 0xFF == ord('q'):
						break

				else:
					break

			cap.release()

def main():
	init_logging("debug")
	directory = os.path.dirname(os.path.abspath( __file__ ))
	while True:
			play_random_video(directory)

	cv2.destroyAllWindows()

if __name__ == '__main__':
	main()
