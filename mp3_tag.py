import os
import music_tag


input_path='./new_books_Copy/new_new_books/életmód/elhizas_jav/mp3/'
input_path='./TARKI/mp3/'
album_title=''
author=''
cover=input_path + 'cover.png'
year=0
genre = 'Audiobook'

def get_mp3_path():
    output = []
    for filename in os.listdir(input_path):
        f = os.path.join(input_path, filename)
        if os.path.isfile(f):
            if ".m4a" in f:
                output.append(f)
    return output

def set_meta(file_url, title, track_no):
    f = music_tag.load_file(file_url)
    f['title'] = title.strip()
    f['album'] = album_title.strip()
    f['artist'] = author.strip()
    f['genre'] = genre.strip()
    f['tracknumber'] = track_no
    if year > 0:
        f['year'] = year
    f['albumartist'] = 'Microsoft Szabolcs'
    print(f['title'].values)
    f.save()


with open(input_path + 'meta.info', "r", encoding='utf-8') as input:
    lines = input.readlines()
    meta = lines[0].split(';')
    author = meta[0]
    album_title = meta[1]
    if len(meta) > 2:
        year = int(meta[2])
    if len(meta) > 3:
        genre = meta [3]

    mp3_files = get_mp3_path()
    if len(mp3_files) +1 != len(lines):
        print('number of files is not equal to number of titles')

    if len(mp3_files) >= len(lines):
        exit(1)

    index = 1
    for file in mp3_files:
        set_meta(file, lines[index], index)
        index = index + 1
