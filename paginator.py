import shutil

from site_handlers import *
import subprocess
import requests
import sys
import pyttsx3
from PIL import Image
import os

# proxy = 'http://10.66.243.130:8080'
#
# os.environ['http_proxy'] = proxy
# os.environ['HTTP_PROXY'] = proxy
# os.environ['https_proxy'] = proxy
# os.environ['HTTPS_PROXY'] = proxy

textpath = ''
partpath = ''
imgpath = ''
tempath = ''

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-GB,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:81.0) Gecko/20100101 Firefox/81.0",
}

def init_speaker() :
    speaker=pyttsx3.init('sapi5')
    #voices = speaker.getProperty("voices")
#    for voice in voices:
#        print(voice.id)
        
    speaker.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_hu-HU_Szabolcs')
    speaker.setProperty('rate', 160)   
    speaker.runAndWait()
    return speaker
    
def AppendtoFile(path, string):
    file_object = open(path, 'a', encoding='utf-8')
    file_object.write(string + '\n')

def HandleImage(url, index):
    name=format(index, '02d')
    print('image')
    with open(tempath + "/" + name + '.jpg', 'wb') as handle:
        response = requests.get(url, headers, stream=True)
        print(response)

        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                print(block)
                break

            handle.write(block)
   
    image=Image.open(tempath + "/" + name + '.jpg')
    width, height = image.size
    if (width*9 == 16 * height):
        image = image.resize((1024, 576), Image.ANTIALIAS)
    elif (width*9 > 16 * height):
        baseheight = 576
        hpercent = (baseheight/float(height))
        wsize = int(float(width)*float(hpercent))
        image = image.resize((wsize, baseheight), Image.ANTIALIAS)
        x=int((wsize-1024)/2)
        image = image.crop((x, 0, x+1024 , 576))
    else:
        basewidth = 1024
        wpercent = (basewidth/float(width))
        hsize = int(float(height)*float(wpercent))
        image = image.resize((basewidth,hsize), Image.ANTIALIAS)
        y = int((hsize-576)/2)
        image = image.crop((0, y, 1024, y+576))

    image.save(imgpath + "/" + name + '.png', "PNG")

    
########################
def MergeWithVideo(name, music):
    # name=format(index, '02d')

    command="./ffmpeg.exe -stats -i " + tempath + name + ".mp3 -f null -"
    
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

    command="./ffmpeg.exe -loop 1 -framerate 1 -i " + imgpath + name + ".png -i " + tempath + name + ".mp3 -i deep2.mp3 -ss 0 -t " + str(seconds) + " -filter_complex amix=inputs=2:duration=longest:weights=\"3 0.82\" -c:v libx264 -r 0.1 -movflags +faststart " + partpath + name + ".mp4"
    subprocess.call(command)
    AppendtoFile(projekt_name+"/list.txt", "file 'part/" + name + ".mp4'")

def CheckPartLength(name, sumlength) :
    hour = int(sumlength/3600)
    minute = int((sumlength - (hour*3600))/60)
    seconds = int(sumlength - (hour * 3600) - (minute * 60))
    AppendtoFile(tempath + "lenghts.txt", str(hour) + ":" + format(minute, "02d") + ":" + format(seconds, "02d"))

    command="./ffmpeg.exe -stats -i " + partpath + name + ".mp4 -f null -"

    with open(tempath + "stdout.txt","wb") as out, open(tempath + "stderr.txt","wb") as err:
        subprocess.call(command,stdout=out,stderr=err)

    with open(tempath + "stderr.txt","r") as file1:
        Lines = file1.readlines()
        for line in Lines:
            if ("Duration:" in line):
                times=line.split()[1].split('.')[0].split(":")
                seconds=int(times[0])*3600 + int(times[1])*60+int(times[2])
                print(line)
                print(seconds)
                return sumlen+seconds

def CreateOutput():
    command="./ffmpeg.exe -f concat -i " + projekt_name + "/list.txt -c copy " + projekt_name + "/" + projekt_name+ ".mp4"
    subprocess.call(command)
    shutil.move(projekt_name + "/list.txt", tempath + "list.txt")

def CreateDescription():
    lengths = []
    titles = []

    AppendtoFile(projekt_name + "/description.txt", "Tartalom:")

    with open(tempath + "lenghts.txt", "r", encoding='utf-8') as lengthfile:
        lengths = lengthfile.readlines()
    with open(tempath + "desc.txt", "r", encoding='utf-8') as title_file:
        titles = title_file.readlines()
    if len(lengths) == len(titles):
        for i in range(len(lengths)):
            AppendtoFile(projekt_name + "/description.txt", lengths[i].strip() + " - " + titles[i].strip())
    else:
        for title in titles:
            AppendtoFile(projekt_name + "/description.txt", title.strip())

    AppendtoFile(projekt_name + "/description.txt", "\nForrások:")

    with open(tempath + "source.txt", "r", encoding='utf-8') as sources:
        for url in sources.readlines():
            AppendtoFile(projekt_name + "/description.txt", url.strip())


    print(lengths)
########################

def CreateWorkspace(projekt):
    shutil.rmtree(projekt_name)
    os.umask(0)
    os.makedirs(projekt_name, 0o777)
    os.makedirs(textpath, 0o777)
    os.makedirs(imgpath, 0o777)
    os.makedirs(partpath, 0o777)
    os.makedirs(tempath, 0o777)

############### MAIN #################
speaker=init_speaker()

filepath = sys.argv[1]
file1 = open(filepath, 'r')
projekt_name=filepath.split("/")[-1].split(".")[0]

textpath = projekt_name + "/text/"
imgpath = projekt_name + "/img/"
partpath = projekt_name + "/part/"
tempath = projekt_name + "/tmp/"
CreateWorkspace(projekt_name)

Lines = file1.readlines()
count = 0

skip=False
sumlen=0
for line in Lines:
    count += 1
    url=line.strip()

    if (count % 2) == 1:
        index= int(count /2) + 1
        [title, content] = HandleArticle(url)

        name=format(index, '02d')

        AppendtoFile(tempath + '/desc.txt', title)
        AppendtoFile(tempath + '/source.txt', url)

        article_file = open(textpath + "/" + name + '.txt', 'w', encoding="utf-8")
        article_file.write(title + '\n' + content + '\n')

        speaker.save_to_file(title + '\n' + content, tempath + "/" + name + '.mp3')
        speaker.runAndWait()

    elif (not skip):
        name=format(int(count /2), '02d')
        HandleImage(line.strip(), int(count /2))
        MergeWithVideo(name, sys.argv[2])
        sumlen = CheckPartLength(name, sumlen)

CreateOutput()
CreateDescription()

shutil.rmtree(tempath)