import os, sys, getopt, pyttsx3,shutil
import subprocess
from collect_names import *
from media_utils import *


tempath = ''
music_path=''
video_path=''
output_path=''

input_path=''

image_path=''
background_music='./a55.mp3'
music_weight='3 0.82'


def GenerateMP4 (name, outname):
    command="./ffmpeg.exe -stats -i " + name + " -f null -"

    with open(tempath + "stdout.txt","wb") as out, open(tempath + "stderr.txt","wb") as err:
        subprocess.call(command,stdout=out,stderr=err)
    seconds=0

    with open(tempath + "stderr.txt","r") as file1:
        Lines = file1.readlines()
        for line in Lines:
            if ("Duration:" in line):
                times=line.split()[1].split('.')[0].split(":")
                seconds=int(times[0])*3600 + int(times[1])*60+int(times[2])
                print(line)
                print(seconds)

    rate = '1' if seconds < 150 else '0.1'
    command="./ffmpeg.exe -loop 1 -framerate 1 -i " + image_path + " -i " + name + " -i " + background_music + ".mp3 -ss 0 -t " + str(seconds) + " -filter_complex amix=inputs=2:duration=longest:weights=\"" + music_weight + "\" -c:v libx264 -r " + rate + " -movflags +faststart " + video_path + outname + ".mp4"
    subprocess.call(command)
    file_object = open(input_path+"/list.txt", 'a', encoding='utf-8')
    file_object.write("file 'mp4/" + outname + ".mp4'\n")
    print(name + 'video')

def CheckPartLength(name, sumlength) :
    hour = int(sumlength/3600)
    minute = int((sumlength - (hour*3600))/60)
    seconds = int(sumlength - (hour * 3600) - (minute * 60))
    AppendtoFile(tempath + "lenghts.txt", str(hour) + ":" + format(minute, "02d") + ":" + format(seconds, "02d"))

    seconds = GetMediaLen(video_path + name + ".mp4")
    print(seconds)
    return sumlen + seconds


try:
    opts, args = getopt.getopt(sys.argv[1:], "hi:p:b:w:", ["help", "output="])
except getopt.GetoptError as err:
    # print help information and exit:
    print(err)  # will print something like "option -a not recognized"
    # usage()
    sys.exit(2)
for o, a in opts:
    if o in ("-h", "--help"):
        # usage()
        sys.exit()
    elif o in ("-i", "--input"):
        input_path = a
    elif o in ("-w", "--weight"):
        music_weight = a
    elif o in ("-b", "--bacground"):
        background_music = a
    elif o in ("-p", "--picture"):
        image_path = a
    else:
        assert False, "unhandled option"
# ...



if not input_path:
    exit (1)


tempath=input_path + "/tmp/"
video_path = input_path + "/mp4/"
os.makedirs(video_path)
os.makedirs(tempath)


index = 0
sumlen=0
for filename in os.listdir(input_path):
    f = os.path.join(input_path, filename)
    if os.path.isfile(f):
        if ".mp3" in f:
            print(f)
            name = format(int(index), "02d")
            GenerateMP4(f, name)
            sumlen = CheckPartLength(name, sumlen)
            index+=1


command="./ffmpeg.exe -f concat -i " + input_path + "/list.txt -c copy " + input_path + "/output.mp4"
subprocess.call(command)

