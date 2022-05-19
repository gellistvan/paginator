from media_utils import *
from collect_names import *
import getopt
import sys

project_name = ''
tmppath = ''
mp3path = ''
imgpath = ''
mp4path = ''
dictionary_path = ''
chapter_delimiter = ''
music_weight = ''
background_music = ''
input_filename =''
image_list='1'
collect_names=False

try:
    opts, args = getopt.getopt(sys.argv[1:], "hP:i:fr:l:p:b:w:", ["help", "output="])
except getopt.GetoptError as err:
    # print help information and exit:
    print(err)  # will print something like "option -a not recognized"
    # usage()
    sys.exit(2)
for o, a in opts:
    if o in ("-h", "--help"):
        # usage()
        sys.exit()
    elif o in ("-P", "--project-name"):
        project_name = a
    elif o in ("-i", "--input"):
        input_path = a
        input_filename= input_path.split(".")[-1]
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
        image_list = a
    else:
        assert False, "unhandled option"
# ...

if not input_path:
    exit (1)

if project_name == '':
    output_path=input_filename

tmppath = project_name + "/tmp/"
mp3path = project_name + "/mp3/"
imgpath = project_name + "/img/"
mp4path = project_name + "/mp4/"

def CreateWorkspace():
    shutil.rmtree(project_name)
    os.umask(0)
    os.makedirs(project_name, 0o777)
    os.makedirs(tmppath, 0o777)
    os.makedirs(mp3path, 0o777)
    os.makedirs(imgpath, 0o777)
    os.makedirs(mp4path, 0o777)

CreateWorkspace()

if collect_names :
    CollectNames(input_path, project_name)
    exit(0)

speaker = init_speaker()


input_file = ''
with open(input_path, "r", encoding='utf-8') as input:
    input_file = input.read()

if dictionary_path != '' :
    with open(dictionary_path, "r", encoding='utf-8') as dict_file:
        pronunciation = dict_file.readlines()

        for line in pronunciation:
            values = line.split('\t')
            input_file=input_file.replace(values[0].lstrip(), values[1].rstrip())

sections=input_file.split(chapter_delimiter)
index=0
sumlen=0

img_tile_path = 'cover.png' #    to be read from list later
music_lengths = []
# 1. Create padded MP3s and legth list
for section in sections:
    name = format(int(index), "02d")
    # first round: tmp mp3
    speaker.save_to_file(section, tmppath + name + '.mp3')
    speaker.runAndWait()

    #second round: add padding
    seconds = GetMediaLen(tmppath + name + ".mp3")
    command="./ffmpeg.exe -f concat -i " + tmppath + name + ".mp3 -ss 0 -t " + str(seconds + 3) + " -c copy " + mp3path + name + ".mp3"
    subprocess.call(command)

    music_lengths.append(GetMediaLen(mp3path + name + ".mp3"))
    AppendtoFile(mp3path + "list.txt", "file \'" + name + ".mp3\'")

    index += 1,

#2. Merge padded mp3s
command="./ffmpeg.exe -f concat -i " + mp3path + "list.txt -c copy " + mp3path + "output.mp3"
subprocess.call(command)

#3. Add background music
seconds = GetMediaLen(mp3path + "output.mp3")
command="./ffmpeg.exe -i " + mp3path + "output.mp3 -i deep2.mp3 -ss 0 -t " + str(seconds + 10) + " -filter_complex amix=inputs=2:duration=longest:weights=\"3 0.82\"" + mp3path + input_filename + ".mp3"
subprocess.call(command)

#4. Generate mp4 chunks
index = 0
with open(image_list, "r", encoding='utf-8') as images:
    for url in input.readlines():
        HandleImage(url, index, imgpath, tmppath)
        index += 1

sumlen = 0
for count in range(0,len(music_lengths)):
    img_idx = count if count < index else index -1
    name = format(int(count), "02d")
    rate = '0.1' if music_lengths[count] < 100 else '1'
    command = "./ffmpeg.exe -loop 1 -framerate 1 -i " + imgpath + format(img_idx, "02d") + ".png " + \
                "-i " + mp3path + input_filename + ".mp3 -ss " + str(sumlen) + " -t " + str(music_lengths[count]) + \
                " -c:v libx264 -r " + rate + " -movflags +faststart " + mp4path + name + ".mp4"
    subprocess.call(command)
    AppendtoFile(mp4path + "list.txt", "file '" + name + ".mp4'")
    sumlen += music_lengths[count]
    print(count)

#5. Merge MP4
command="./ffmpeg.exe -f concat -i " + mp4path + "list.txt -c copy " + project_name + "output.mp4"
subprocess.call(command)