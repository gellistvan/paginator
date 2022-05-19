from site_handlers import *
import sys
from media_utils import *

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


########################
def MergeWithVideo(name, music):
    # name=format(index, '02d')

    seconds = GetMediaLen( tempath + name + ".mp3")
    print(seconds)

    command="./ffmpeg.exe -loop 1 -framerate 1 -i " + imgpath + name + ".png -i " + tempath + name + ".mp3 -i deep2.mp3 -ss 0 -t " + str(seconds) + " -filter_complex amix=inputs=2:duration=longest:weights=\"3 0.82\" -c:v libx264 -r 0.1 -movflags +faststart " + partpath + name + ".mp4"
    subprocess.call(command)
    AppendtoFile(projekt_name+"/list.txt", "file 'part/" + name + ".mp4'")

def CheckPartLength(name, sumlength) :
    hour = int(sumlength/3600)
    minute = int((sumlength - (hour*3600))/60)
    seconds = int(sumlength - (hour * 3600) - (minute * 60))
    AppendtoFile(tempath + "lenghts.txt", str(hour) + ":" + format(minute, "02d") + ":" + format(seconds, "02d"))

    seconds = GetMediaLen(partpath + name + ".mp4")
    print(seconds)
    return sumlen + seconds

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
    if os.path.isdir(projekt_name):
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
# CreateWorkspace(projekt_name)

Lines = file1.readlines()
count = 0
#
skip=False
sumlen=0
for line in Lines:
    count += 1
    url=line.strip()
    index = int(count /2)+1 if count%2 == 1 else int(count /2)
    if os.path.isfile(partpath + format(index, "02d") + ".mp4") :
        continue

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
        HandleImage(line.strip(), int(count /2), tempath, imgpath)
        MergeWithVideo(name, sys.argv[2])
        sumlen = CheckPartLength(name, sumlen)

CreateOutput()
CreateDescription()

# shutil.rmtree(tempath)