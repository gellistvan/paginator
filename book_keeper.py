import os, sys, getopt, pyttsx3,shutil
import subprocess
from collect_names import *
from media_utils import *

from preprocess import *

class BookKeeper:
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
    sumlen=0

    def GenerateMP4 (self, name):
        command="./ffmpeg.exe -stats -i " + self.music_path + name + ".mp3 -f null -"

        with open(self.tempath + "stdout.txt","wb") as out, open(self.tempath + "stderr.txt","wb") as err:
            subprocess.call(command,stdout=out,stderr=err)
        seconds=0

        with open(self.tempath + "stderr.txt","r") as file1:
            Lines = file1.readlines()
            for line in Lines:
                if ("Duration:" in line):
                    times=line.split()[1].split('.')[0].split(":")
                    seconds=int(times[0])*3600 + int(times[1])*60+int(times[2])
                    print(line)
                    print(seconds)

        rate = '1' if seconds < 150 else '0.1'
        command="./ffmpeg.exe -loop 1 -framerate 1 -i " + self.music_path + "cover.png -i " + self.music_path + name + ".mp3 -i " + self.background_music + ".mp3 -ss 0 -t " + str(seconds) + " -filter_complex amix=inputs=2:duration=longest:weights=\"" + self.music_weight + "\" -c:v libx264 -r " + rate + " -movflags +faststart " + self.video_path + name + ".mp4"
        subprocess.call(command)
        file_object = open(self.output_path+"/list.txt", 'a', encoding='utf-8')
        file_object.write("file 'mp4/" + name + ".mp4'\n")
        print(name + 'video')

    def CheckPartLength(self, name, sumlength) :
        hour = int(sumlength/3600)
        minute = int((sumlength - (hour*3600))/60)
        seconds = int(sumlength - (hour * 3600) - (minute * 60))
        AppendtoFile(self.output_path + "/lenghts.txt", str(hour) + ":" + format(minute, "02d") + ":" + format(seconds, "02d"))

        seconds = GetMediaLen(self.video_path + name + ".mp4")
        print(seconds)
        return self.sumlen + seconds

    def Execute(self):
        # Generate media
        speaker = init_speaker()
        # exit(0)

        if os.path.isdir(self.output_path):
            shutil.rmtree(self.output_path)
        os.makedirs(self.output_path, 0o777)
        if not self.collect_names:
            os.makedirs(self.music_path)
        if self.image_path:
            self.video_path = self.output_path + "/mp4/"
            os.makedirs(self.video_path)
        os.makedirs(self.tempath)

        with open(self.input_path, "r", encoding='utf-8') as input:
            input_file = preprocess(input.read())

            if self.dictionary_path != '' :
                with open(self.dictionary_path, "r", encoding='utf-8') as dict_file:
                    pronunciation = dict_file.readlines()

                    for line in pronunciation:
                        values = line.split('\t')
                        input_file=input_file.replace(values[0].lstrip(), values[1].rstrip())

            if self.collect_names :
                CollectNames(input_file, self.output_path)
                exit(0)

            sections=input_file.split(self.chapter_delimiter)

            index=0
            for section in sections:
                name = format(int(index), "02d")
                speaker.save_to_file(section, self.music_path + name + '.mp3')
                speaker.runAndWait()
                if self.image_path:
                    shutil.copyfile(self.image_path, self.music_path + "cover.png")
                    self.GenerateMP4(name)
                    self.sumlen = self.CheckPartLength(name, self.sumlen)
                index += 1

        command="./ffmpeg.exe -f concat -i " + self.output_path + "/list.txt -c copy " + self.output_path + "/output.mp4"
        subprocess.call(command)
        shutil.move(self.output_path + "/list.txt", self.tempath + "list.txt")
        shutil.rmtree(self.tempath)



object = BookKeeper()
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
        object.output_path = a
    elif o in ("-i", "--input"):
        object.input_path = a
    elif o in ("-f", "--find-names"):
        object.collect_names=True
    elif o in ("-r", "--replace"):
        object.dictionary_path = a
    elif o in ("-l", "--limit"):
        object.chapter_delimiter = a
    elif o in ("-w", "--weight"):
        object.music_weight = a
    elif o in ("-b", "--bacground"):
        object.background_music = a
    elif o in ("-p", "--picture"):
        object.image_path = a
    else:
        assert False, "unhandled option"
# ...

if not object.input_path:
    exit (1)

if object.output_path == '':
    output_path='output'

object.music_path = object.output_path+"/mp3/"
object.tempath=object.output_path + "/tmp/"

object.Execute()