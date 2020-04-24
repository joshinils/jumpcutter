import subprocess
import argparse
import math
import os


# https://stackoverflow.com/questions/3844430/how-to-get-the-duration-of-a-video-in-python
# length of video file in seconds
def get_length(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)


parser = argparse.ArgumentParser(description='snips a video into small chunks, jumpcuts those, stitches them back together and converts the result with vlc')
parser.add_argument('-f', type=str,  help='the video file you want modified')
parser.add_argument('-c', type=float, default=600, help="chunk length in seconds to cut the video up into")

args = parser.parse_args()

fileName = args.f
assert fileName != None , "why u put no input file, that dum"

chunkLength = args.c
assert chunkLength > 0, "chunks cant be of that length"

VideoLengthInSeconds = get_length(fileName);
chunksAmount = math.ceil(VideoLengthInSeconds / chunkLength);

command = "echo " + str(chunksAmount) + " " + str(chunkLength) 
subprocess.call(command, shell=True)



print(chunksAmount)
for i in range(chunksAmount):
	fName, fExtension = os.path.splitext(fileName)
	chunkName = fName + "_chunk_" + str(i) + fExtension
	secondsIn = i*chunkLength
	command = "ffmpeg -ss " + "{:1.0f}".format(secondsIn//3600) + ":" + "{:1.0f}".format((secondsIn// 60) % 60) + ":" + "{:1.0f}".format((secondsIn) % 60) + " -i " + fileName + " -acodec copy -vcodec copy -t " + "{:1.0f}".format(chunkLength// 3600) + ":" + "{:1.0f}".format((chunkLength// 60) % 60) + ":" + "{:1.0f}".format(chunkLength % 60) + " " + chunkName
	print(command)
	subprocess.call(command, shell=True)
	
	subprocess.call("rm TEMP -r -f", shell=True)
	command = "python3 ~/jumpcutter/jumpcutter.py --input_file " + chunkName + " --output_file " + fName + "_chunk_" + str(i) + "_jumped" + fExtension + " --silent_threshold 0.5 --sounded_speed 1 --silent_speed 999999 --frame_margin 30 --frame_rate 60 --frame_quality 1"
	subprocess.call(command, shell=True)
	subprocess.call("rm TEMP -r -f", shell=True)
	subprocess.call("rm " + chunkName + " -r -f", shell=True)
	print("\n\n\n\n")
	#break


























