import re
import subprocess
import requests
import sys
#import html2text
import pyttsx3
from PIL import Image
from html.parser import HTMLParser
from bs4 import BeautifulSoup
import os

# proxy = 'http://10.66.243.130:8080'
#
# os.environ['http_proxy'] = proxy
# os.environ['HTTP_PROXY'] = proxy
# os.environ['https_proxy'] = proxy
# os.environ['HTTPS_PROXY'] = proxy

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-GB,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:81.0) Gecko/20100101 Firefox/81.0",
}

def G7(url):
    req = requests.get(url, headers).text
    soup = BeautifulSoup(req, "html.parser")
    title=soup.find("h1").get_text()
    content=soup.find("div", class_='content')
    content.find("div", class_='donate__articleBox -donateArticleBox _ce_measure_widget').decompose()
    content.find("div", class_='fb-share-button').decompose()
    content.find("p", class_='buttons-container _ce_measure_widget').decompose()

    frames = content.findAllNext("iframe")
    for frame in frames:
        frame.decompose()


    print(title)
    print(content.get_text())
    return [title, content.get_text()]

def TELEX(url):
    req = requests.get(url, headers).text
    soup = BeautifulSoup(req, "html.parser")
    title=soup.find("h1").get_text()
    top_section=soup.find("p", class_='article__lead').get_text()
    content=soup.find("div", class_='article-html-content')
    figures = content.findAllNext("figure")
    for figure in figures:
        figure.decompose()

    print(top_section + '\n' + content.get_text())
    return [title, top_section + '\n' + content.get_text()]

def Huszon4hu(url):
    req = requests.get(url, headers).text
    soup = BeautifulSoup(req, "html.parser").find("div", {"class": "is_content"})
    content = soup.find("div", class_='o-post__body o-postCnt post-body')
    figures = content.findAllNext("figure")
    for figure in figures:
        figure.decompose()

    content.find("div", class_='m-riporter').decompose()

    title=soup.find("h1").get_text();

    h3=soup.find("h3")
    if h3 is not None:
        h3.decompose()
    block=soup.find("blockquote", {"class": "embedly-card"})
    if block is not None:
        block.decompose()

    print(title)
    print(content.get_text())
    return [title, content.get_text()]

def NegyNegyNegy(url):
    payload = {
        'username': 'istvan.gellai@gmail.com',
        'password': 's2dt39b4'
    }
    with requests.Session() as s:
        p = s.post('https://kor.444.hu/bejelentkezes', data=payload)
        print (p.text)

        req = s.get(url, headers).text
        soup = BeautifulSoup(req, "html.parser")
        title = soup.find("h1")
        content = soup.find("div", class_='ls eu iP').findChildren("div", recursive=False)[0]
        figures = content.findAllNext("figure")
        for figure in figures:
            figure.decompose()
          # print(figures)
        content_text = content.get_text()
        content_text = re.sub(r'[\n\n]+', r'\n', content_text, re.MULTILINE)
        print(content_text)
        return [title.get_text(), content.get_text()]

def Atlatszo(url):
    req = requests.get(url, headers).text
    soup = BeautifulSoup(req, "html.parser").find("div", {"class": "inner-article_body"})
    title=soup.find("h1")
    content=soup.find("div", {"class": "the_content"})
   # soup.find("div", {"class": "article_head_box"}).decompose()
    #soup.find("div", {"class": "post_author_box"}).decompose()
    #soup.find("div", {"class": "post_intro_box"}).decompose()
    #soup.find("div", {"class": "post_outro_box"}).decompose()
    #soup.find("div", {"class": "the_tags"}).decompose()
    #soup.find("div", {"class": "html_banner"}).decompose()
    h3=soup.find("h3")
    if h3 is not None:
        h3.decompose()
    block=soup.find("blockquote", {"class": "embedly-card"})
    if block is not None:
        block.decompose()
    return [title.get_text(), content.get_text()]


##################
def init_speaker() :
    speaker=pyttsx3.init('sapi5')
    #voices = speaker.getProperty("voices")
#    for voice in voices:
#        print(voice.id)
        
    speaker.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_hu-HU_Szabolcs')
    speaker.setProperty('rate', 160)   
    speaker.runAndWait()
    return speaker
    
########################

def AppendtoFile(path, string):
    file_object = open(path, 'a')
    file_object.write(string + '\n')

########################

def HandleImage(url, index):
    name=format(index, '02d')
    print('image')
    with open(name + '.jpg', 'wb') as handle:
        response = requests.get(url, headers, stream=True)
        print(response)

        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                print(block)
                break

            handle.write(block)
   
    image=Image.open(name + '.jpg')
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

    image.save(name + '.png', "PNG")   
    
def HandleArticle(url, index, speaker):
    title=''
    content=''
    name=format(index, '02d')
    if ('atlatszo.hu' in url):
        [title, content] = Atlatszo(url)
    else:
        return 0

    AppendtoFile('desc.txt', title)
    AppendtoFile('source.txt', url)
    
    article_file = open(name + '.txt', 'w')
    article_file.write(title + '\n' + content + '\n')
    
    speaker.save_to_file(title + '\n' + content, name + '.mp3')
    speaker.runAndWait()
    
    return index
    
########################
def MergeWithVideo(index, music):
    name=format(index, '02d')

    command="./ffmpeg.exe -stats -i " + name + ".mp3 -f null -"  
    
    with open("stdout.txt","wb") as out, open("stderr.txt","wb") as err:
        subprocess.call(command,stdout=out,stderr=err)
    seconds=0
    
    with open("stderr.txt","r") as file1:
        Lines = file1.readlines()
        for line in Lines:
            if ("Duration:" in line):
                times=line.split()[1].split('.')[0].split(":")
                seconds=int(times[0])*3600 + int(times[1])*60+int(times[2])
                print(line)
                print(seconds)
                
        
    command="./ffmpeg.exe -loop 1 -framerate 1 -i " + name + ".png -i " + name + ".mp3 -i deep2.mp3 -ss 0 -t " + str(seconds) + " -filter_complex amix=inputs=2:duration=longest:weights=\"3 0.82\" -c:v libx264 -r 0.1 -movflags +faststart " + name + ".mp4" 
    subprocess.call(command)
    
    #AppendtoFile('list.txt' 'file \'' + name + '.mp4\'\n')



# Atlatszo('https://atlatszo.hu/kozugy/2022/05/07/cikkunk-utan-3-nappal-elerhetetlenne-valt-az-agressziv-tartalmakat-kozlo-mindenszo/')
# NegyNegyNegy('https://444.hu/2022/05/09/ugyanolyan-rossz-velemennyel-vannak-a-magyarok-ukrajnarol-mint-oroszorszagrol')
# Huszon4hu('https://24.hu/kultura/2022/05/09/dave-gahan-depeche-mode-60-hatvan-eves-heroin-tuladagolas-elvonokura/')
# NegyNegyNegy('https://444.hu/2022/05/09/a-bekeert-haboruznak-mondta-putyin-a-gyozelem-napjan')
# TELEX('https://telex.hu/sport/2022/05/09/hosszu-katinka-film-bemutato-shane-tusup')
G7('https://g7.hu/adat/20220503/ha-tovabbra-is-igy-futunk-abbol-nem-lesz-energiafuggetlenseg/')

########################

file1 = open(sys.argv[1], 'r')
Lines = file1.readlines()
count = 0

speaker=init_speaker()

skip=False
for line in Lines:
    count += 1
    #print("Line{}: {}".format(count, line.strip()))
    if (count % 2) == 1:
        HandleArticle(line.strip(), int(count /2) + 1, speaker)
    elif (not skip):
        HandleImage(line.strip(), int(count /2))
        MergeWithVideo(int(count /2), sys.argv[2])
    




#Atlatszo('https://atlatszo.hu/kozugy/2022/05/07/cikkunk-utan-3-nappal-elerhetetlenne-valt-az-agressziv-tartalmakat-kozlo-mindenszo/')
#Atlatszo('https://atlatszo.hu/kozugy/2022/05/04/esztergomi-szoftverfejlesztot-talaltunk-egy-agressziv-alhiroldal-mogott/')