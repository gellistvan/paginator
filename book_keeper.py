import os, sys, getopt, pyttsx3, shutil
import ntpath
from pathlib import Path
from typing import Callable

from collect_names import *
from media_utils import *
from datetime import timezone
import datetime
from preprocess import *

from threading import Thread

def ExtractMusic(folder, filename, outfolder, temp_path):
    command="./ffmpeg.exe -i \""+ folder + filename + ".mp4\" -map 0:a -c copy " + outfolder + filename + ".m4a"

    with open(temp_path + "thread_stdout.txt", "wb") as out, open(temp_path + "thread_stdout.txt", "wb") as err:
        subprocess.call(command,stdout=out,stderr=err)

def utc_timestamp():
    dt = datetime.datetime.now(timezone.utc)
    utc_time = dt.replace(tzinfo=timezone.utc)
    return utc_time.timestamp()

class BookKeeper:
    temp_path = ''
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
    progress=0.0
    sumchars=0
    actualstep=0.0
    subprogress=0.0
    set_progress_bar_callback: Callable = None
    is_stop_progressing_requested_callback: Callable = None
    CPUs = os.cpu_count()
    trigger_sleep = False
    starttime = 0
    video_chapter_generating_process: subprocess.Popen = None

    temp_folder_path: str
    PREVIEW_FILENAME = "preview.wav"
    SPEECH_PREVIEW_FILENAME = "speech_preview.wav"

    def __init__(self):
        self.temp_folder_path = os.path.expandvars("%TEMP%") + "\\book_keeper"
        if not os.path.isdir(self.temp_folder_path):
            try:
                os.mkdir(self.temp_folder_path)
            except Exception as e:
                print(e, file=sys.stderr)
                self.temp_folder_path = "."

    def ReportProgress(self):
        percent = int(100*(self.progress + self.subprogress * self.actualstep))
        time_remaining = 0 if percent == 0 else (100-percent)*((utc_timestamp() - self.starttime) / percent)

        if self.set_progress_bar_callback is not None:
            self.set_progress_bar_callback(percent, time_remaining)
        # else:
            # print("=======> " + str(self.Progress()))

    def GenerateMP4 (self, name):
        command="./ffmpeg.exe -stats -i \"" + self.temp_path + name + ".mp3\" -f null -"

        with open(self.temp_path + "stdout.txt", "wb") as out, open(self.temp_path + "stderr.txt", "wb") as err:
            subprocess.call(command,stdout=out,stderr=err)
        seconds=0

        with open(self.temp_path + "stderr.txt", "r") as file1:
            Lines = file1.readlines()
            for line in Lines:
                if ("Duration:" in line):
                    times=line.split()[1].split('.')[0].split(":")
                    seconds=int(times[0])*3600 + int(times[1])*60+int(times[2]) + 10

        rate = '1' if seconds < 150 else '0.5'
        command="./ffmpeg.exe -loop 1 -framerate 1 -i " + self.temp_path + "cover.png -i \"" + self.temp_path + name + ".mp3\" -i " + self.background_music + ".mp3 -ss 0 -t " + str(seconds) + " -filter_complex amix=inputs=2:duration=longest:weights=\"" + self.music_weight + "\" -c:v libx264 -r " + rate + " -threads " + str(self.CPUs) + " -movflags +faststart \"" + self.video_path + name + ".mp4\""
        subprocess.call(command)
        rate = '1' if seconds < 150 else '0.1'
        command="./ffmpeg.exe -loop 1 -framerate 1 -i " + self.music_path + "cover.png -i \"" + self.music_path + name + ".mp3\" -i " + self.background_music + ".mp3 -ss 0 -t " + str(seconds) + " -filter_complex amix=inputs=2:duration=longest:weights=\"" + self.music_weight + "\" -c:v libx264 -r " + rate + " -threads " + str(self.CPUs) + " -movflags +faststart \"" + self.video_path + name + ".mp4\""
        self.video_chapter_generating_process = subprocess.Popen(command)
        self.video_chapter_generating_process.communicate()
        self.video_chapter_generating_process = None

        file_object = open(self.output_path+"/list.txt", 'a', encoding='utf-8')
        file_object.write("file 'mp4/" + name + ".mp4'\n")

    def TriggerSleep(self):
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

    def CheckPartLength(self, name, sumlength) :
        hour = int(sumlength/3600)
        minute = int((sumlength - (hour*3600))/60)
        seconds = int(sumlength - (hour * 3600) - (minute * 60))
        AppendtoFile(self.output_path + "/lenghts.txt", str(hour) + ":" + format(minute, "02d") + ":" + format(seconds, "02d"))

        seconds = GetMediaLen(self.video_path + name + ".mp4")
        print(seconds)
        return self.sumlen + seconds

    def Estimate(self):
        if self.input_path == "" or not Path(self.input_path).is_file():
            return "", ""
        kilobytes = (os.stat(self.input_path).st_size / 1024.0)
        sum_seconds = 62 * kilobytes
        out_size = (1.35 * kilobytes)
        hours = int(sum_seconds / 3600)
        sum_seconds -= hours * 3600
        minutes = int (sum_seconds / 60)
        sum_seconds -= minutes * 60
        seconds = int(sum_seconds + 1)
        length_text = "{hours:02d}:{minutes:02d}:{seconds:02d}".format(hours = hours, minutes = minutes, seconds = seconds)
        size_text = "{size:.2f} MB".format(size = out_size)
        return length_text, size_text

    def GeneratePreview(self):
        SAMPLE_TEXT = "A szöveget felolvassa: Microsoft Szabolcs."
        SPEECH_PREVIEW_PATH = self.temp_folder_path + "\\" + self.SPEECH_PREVIEW_FILENAME
        result_path = SPEECH_PREVIEW_PATH

        if not os.path.isfile(SPEECH_PREVIEW_PATH):
            speaker = init_speaker()
            speaker.save_to_file(SAMPLE_TEXT, SPEECH_PREVIEW_PATH)
            speaker.runAndWait()

        if os.path.isfile(self.background_music):
            command = "./ffmpeg.exe -y -i \"" + SPEECH_PREVIEW_PATH + "\" -ss 15 -i \"" + self.background_music + "\" " \
                      + "-filter_complex amix=inputs=2:duration=shortest:weights=\"" + self.music_weight + "\" -f wav " + self.temp_folder_path + "\\" + self.PREVIEW_FILENAME
            completed_proc = subprocess.run(command)

            if completed_proc.returncode == 0:
                result_path = self.temp_folder_path + "\\" + self.PREVIEW_FILENAME
            else:
                raise Exception("An error occurred while generating preview.\nffmpeg error code: " + str(completed_proc.returncode))

        return result_path

    def KillVideoGeneratingProcess(self):
        if self.video_chapter_generating_process and self.video_chapter_generating_process.poll() is None:
            self.video_chapter_generating_process.kill()
            self.video_chapter_generating_process = None

    def Execute(self):
        self.starttime = utc_timestamp()
        self.music_path = self.output_path + "/mp3/"
        self.temp_path = self.output_path + "/tmp/"

        # Generate media
        speaker = init_speaker()
        # exit(0)

        if os.path.isdir(self.output_path):
            shutil.rmtree(self.output_path)
        os.makedirs(self.output_path, 0o777)
        os.makedirs(self.music_path)
        if self.image_path:
            self.video_path = self.output_path + "/mp4/"
            os.makedirs(self.video_path)
        os.makedirs(self.temp_path)

        with open(self.input_path, "r", encoding='utf-8') as input:
            input_file = preprocess(input.read())

            if self.collect_names:
                filename=ntpath.basename(self.input_path)[0:-4]
                outpath = self.output_path + "/" + filename + "_dict"
                names = CollectNames(input_file, outpath + ".txt", self.dictionary_path)

                speaker.save_to_file(names, self.temp_path + filename + '.mp3')
                speaker.runAndWait()

                if self.image_path != '' and self.background_music != '':
                    shutil.copyfile(self.image_path, self.temp_path + "cover.png")
                    self.GenerateMP4(filename)
                    ExtractMusic(self.video_path, filename, self.music_path, self.temp_path)

                self.progress = 1
                self.ReportProgress()
                return

            if self.dictionary_path != '':
                with open(self.dictionary_path, "r", encoding='utf-8') as dict_file:
                    pronunciation = dict_file.readlines()

                    for line in pronunciation:
                        values = line.split('\t')
                        input_file = input_file.replace(values[0].lstrip(), values[1].rstrip())

            self.sumchars = len(input_file)
            sections=input_file.split(self.chapter_delimiter)
            self.ReportProgress()
            index=0
            for section in sections:
                self.progress += self.actualstep
                self.subprogress = 0.0
                self.actualstep = len(section)/self.sumchars
                self.ReportProgress()
                name = format(int(index), "02d")
                speaker.save_to_file(section, self.temp_path + name + '.mp3')
                speaker.runAndWait()
                self.ReportProgress()
                self.subprogress = 0.35

                if self.is_stop_progressing_requested_callback and self.is_stop_progressing_requested_callback():
                    return

                if self.image_path:
                    shutil.copyfile(self.image_path, self.temp_path + "cover.png")
                    self.GenerateMP4(name)
                    self.sumlen = self.CheckPartLength(name, self.sumlen)

                    thread = Thread(target=ExtractMusic(self.video_path, name, self.music_path, self.temp_path))
                    thread.start()

                index += 1
                self.ReportProgress()

                if self.is_stop_progressing_requested_callback and self.is_stop_progressing_requested_callback():
                    return

        self.progress = 0.99
        self.subprogress = 0.0
        self.actualstep = 1.0
        self.ReportProgress()
        command="./ffmpeg.exe -f concat -i " + self.output_path + "/list.txt -c copy " + self.output_path + "/output.mp4"
        subprocess.call(command)
        shutil.move(self.output_path + "/list.txt", self.temp_path + "list.txt")
        shutil.rmtree(self.temp_path)
        self.progress = 1.0
        self.actualstep = 0.0
        self.ReportProgress()

        if self.trigger_sleep:
            self.TriggerSleep()


if __name__ == "__main__":
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

    object.Execute()