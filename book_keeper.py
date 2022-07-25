import os, sys, getopt, pyttsx3,shutil
import subprocess
from collect_names import *
from media_utils import *

tempath = ''
music_path=''
video_path=''
output_path=''

input_path=''
dictionary_path=''
chapter_delimiter='<<LIMIT>>'

collect_names=False
image_path=''
background_music='./deep2.mp3'
music_weight='3 0.82'


def GenerateMP4 (name):
    command="./ffmpeg.exe -stats -i " + music_path + name + ".mp3 -f null -"

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
    command="./ffmpeg.exe -loop 1 -framerate 1 -i " + music_path + "cover.png -i " + music_path + name + ".mp3 -i " + background_music + ".mp3 -ss 0 -t " + str(seconds) + " -filter_complex amix=inputs=2:duration=longest:weights=\"" + music_weight + "\" -c:v libx264 -r " + rate + " -movflags +faststart " + video_path + name + ".mp4"
    subprocess.call(command)
    file_object = open(output_path+"/list.txt", 'a', encoding='utf-8')
    file_object.write("file 'mp4/" + name + ".mp4'\n")
    print(name + 'video')


def CheckPartLength(name, sumlength) :
    hour = int(sumlength/3600)
    minute = int((sumlength - (hour*3600))/60)
    seconds = int(sumlength - (hour * 3600) - (minute * 60))
    file_object = open(output_path + "/lenghts.txt", 'a', encoding='utf-8')
    file_object.write(str(hour) + ":" + format(minute, "02d") + ":" + format(seconds, "02d") + "\n")
    second = GetMediaLen(video_path + name + ".mp4")
    print(seconds)
    return sumlen + seconds

try:
    opts, args = getopt.getopt(sys.argv[1:], "ho:i:fr:l:p:b:w:", ["help", "output="])
except getopt.GetoptError as err:
    # print help information and exit:
    print(err)  # will print something like "option -a not recognized"
    # usage()
    sys.exit(2)
for o, a in opts:
    if o in ("-h", "--help"):
        # usage()
        sys.exit()
    elif o in ("-o", "--output"):
        output_path = a
    elif o in ("-i", "--input"):
        input_path = a
    elif o in ("-f", "--find-names"):
        collect_names=True
    elif o in ("-r", "--replace"):
        dictionary_path = a
    elif o in ("-l", "--limit"):
        chapter_delimiter = a
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

if output_path == '':
    output_path='output'

music_path = output_path+"/mp3/"
tempath=output_path + "/tmp/"


# Generate media
speaker = init_speaker()
exit(0)


if os.path.isdir(output_path):
    shutil.rmtree(output_path)
os.makedirs(output_path, 0o777)
if not collect_names:
    os.makedirs(music_path)
if image_path:
    video_path = output_path + "/mp4/"
    os.makedirs(video_path)
os.makedirs(tempath)


with open(input_path, "r", encoding='utf-8') as input:
    input_file = input.read()

    if dictionary_path != '' :
        with open(dictionary_path, "r", encoding='utf-8') as dict_file:
            pronunciation = dict_file.readlines()

            for line in pronunciation:
                values = line.split('\t')
                input_file=input_file.replace(values[0].lstrip(), values[1].rstrip())

    if collect_names :
        CollectNames(input_file, output_path)
        exit(0)

    sections=input_file.split(chapter_delimiter)
    index=0
    sumlen=0
    for section in sections:
        name = format(int(index), "02d")
        speaker.save_to_file(section, music_path + name + '.mp3')
        speaker.runAndWait()
        if image_path:
            shutil.copyfile(image_path, music_path + "cover.png")
            GenerateMP4(name)
            sumlen = CheckPartLength(name, sumlen)
        index += 1

command="./ffmpeg.exe -f concat -i " + output_path + "/list.txt -c copy " + output_path + "/output.mp4"
subprocess.call(command)
shutil.move(output_path + "/list.txt", tempath + "list.txt")
shutil.rmtree(tempath)