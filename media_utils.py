import pyttsx3
import os
import subprocess
from PIL import Image
import shutil
import requests

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-GB,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:81.0) Gecko/20100101 Firefox/81.0",
}

def init_speaker() :
    speaker=pyttsx3.init('sapi5')
    for voice in speaker.getProperty('voices'):
        print(voice)
    speaker.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_hu-HU_Szabolcs')
    speaker.setProperty('rate', 160)
    speaker.runAndWait()
    return speaker

def GetMediaLen(path):
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE

    command="./ffmpeg.exe -stats -i " + path + " -f null -"

    with open("stdout.txt","wb") as out, open("stderr.txt","wb") as err:
        subprocess.call(command,stdout=out,stderr=err,startupinfo=startupinfo)
    seconds = 0
    with open("stderr.txt","r") as file1:
        Lines = file1.readlines()
        for line in Lines:
            if ("Duration:" in line):
                times=line.split()[1].split('.')[0].split(":")
                seconds=int(times[0])*3600 + int(times[1])*60+int(times[2])

    os.remove("stdout.txt")
    os.remove("stderr.txt")
    return seconds

def AppendtoFile(path, string):
    file_object = open(path, 'a', encoding='utf-8')
    file_object.write(string + '\n')

def ResizeImage(input, output, W=1024, H=576):
    image=Image.open(input)

    width, height = image.size
    if (width*9 == 16 * height):
        image = image.resize((W, H), Image.ANTIALIAS)
    elif (width*9 > 16 * height):
        baseheight = H
        hpercent = (baseheight/float(height))
        wsize = int(float(width)*float(hpercent))
        image = image.resize((wsize, baseheight), Image.ANTIALIAS)
        x=int((wsize-W)/2)
        image = image.crop((x, 0, x+W , H))
    else:
        basewidth = W
        wpercent = (basewidth/float(width))
        hsize = int(float(height)*float(wpercent))
        image = image.resize((basewidth,hsize), Image.ANTIALIAS)
        y = int((hsize-H)/2)
        image = image.crop((0, y, W, y+H))

    image.save(output + '.png', "PNG")

def HandleImage(url, index, imgpath, tempath, W = 1024, H=573):
    name=format(index, '02d')
    print('image')
    filename=''
    if "file://" not in url:
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
        filename = tempath + "/" + name + '.jpg'
    else:
        filename=url.split("\\")[-1];
        ext=filename.split(".")[-1]
        shutil.copy(url.split("//")[1], tempath + "/" + name + '.' + ext)
        filename = tempath + "/" + name + '.' + ext

    ResizeImage(filename, imgpath + "/" + name, W, H)