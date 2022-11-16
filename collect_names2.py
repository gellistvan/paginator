import re

vovels = ["a", "á", "e", "é", "i", "í", "o", "ó", "ö", "ő", "u", "ú", "ü", "ű"]
v_declinations = ["val", "vel", "vá", "vé"]
declinations = ["nak", "nek", "ért", "ban", "ben", "ba", "be", "on", "en", "ön", "nál", "nél", "ra", "re", "hoz", "hez", "höz", "ból", "ből", "ról", "ről", "tól", "től", "ig", "ként", "ul", "ül"]



def BuildDictionary(dictionary_path):
    output = []
    with open(dictionary_path, "r", encoding='utf-8') as dict_file:
        pronunciation = dict_file.readlines()

        for line in pronunciation:
            values = line.split('\t')
            values = list(map(lambda c: c.lstrip(), values))
            found = False
            if " " in values[0] and " " in values[1]:
                terms = values[0].split()
                items = values[1].split()
                if len(terms) == len(items):
                    found = True
                    for i in range(len(terms)):
                        output.append((terms[i], items[i]))
                        # print(terms[i] + " ---> " + items[i])

            #if not found:
            output.append((values[0].lstrip(), values[1].rstrip()))

    return output

def FindNames(input_file):
    matches = re.findall(r"[^\.\?\!\-”\]–] (([A-ZÖÜÓŐÚÉÁŰÍ][a-zöüóőúéáűí]{3,}[ \.\!\?\,\-])+)", input_file)
    keys=[]
    for item in matches:
        keys.append(item[0][0:-1])
    keys.sort()
    return keys

def GetTranscriptions(dictionary, key):
    output = []
    for entry in dictionary:
        if entry[0] == key and entry[1] not in output:
            output.append(entry[1])
    return output

def TranscribeKnownNames(dictionary, keys):
    transcribed = []
    unknown = []
    for key in keys:
        transcriptions = GetTranscriptions(dictionary, key)
        if len(transcriptions) > 0:
            transcribed.append(key + "\t" + "\t".join(transcriptions))
        else:
            unknown.append(key)

    return unknown, transcribed

def RemovePrefixes(keys):
    last = keys[0]
    for key in keys[:]:
        if last != key and ((last not in key) or abs(len(key) - len(last)) > 3):
            if (last + ' ') in key :
                keys.remove(key)
                keys.append(key[len(last) + 1 :])
            else:
                last=key
        else:
            keys.remove(key)

    keys.sort()
    return keys

def SplitNames(keys, delimiter):
    output=[]
    for key in keys:
        entries = key.split(delimiter)
        for entry in entries:
            if entry not in output:
                output.append(entry)
    output.sort()
    return output

def FindAbreviations(input_file):
    matches = re.findall(r"[^\.\?\!\-”\]] (([A-Z]{2,}[ \.\!\?\,\-])+)", input_file)
    keys=[]
    for item in matches:
        keys.append(item[0][0:-1])
    keys.sort()
    return keys

def FindShortenings(input_file):
    # TODO
    return []

def FindLowercase(keys, inputfile):
    output = []
    for key in keys:
        output.append(key)
        matches = re.findall(key.lower() + "[^\s]*", inputfile)
        for item in matches:
            output.append(item)
    return list(dict.fromkeys(output))

def FilterDeclinations(keys):
    output = []
    print()
    print()
    for key in keys:
        found = False
        for d in declinations:
            if key.endswith(d):
                trunk = key[0:-1*len(d)]
                output.append(trunk)
                if trunk[-1] == 'á':
                    trunk = trunk[0:-1] +'a'
                    output.append(trunk)
                elif trunk[-1] == 'é':
                    trunk = trunk[0:-1] +'e'
                    output.append(trunk)

                if len(d) < 3:
                    output.append(key)
                found = True
                break

        if found:
            continue

        for v in v_declinations:
            if key.endswith(v):
                trunk = key[0:-1*len(v)]
                output.append(trunk)
                found = True

                if trunk[-1] not in "áéiíoóöőuúüűv":
                    output.append(key)  # fake rag
                    break

                output.append(trunk)
                if trunk[-1] == 'á':
                    trunk = trunk[0:-1] +'a'
                    output.append(trunk)
                elif trunk[-1] == 'é':
                    trunk = trunk[0:-1] +'e'
                    output.append(trunk)

        if found:
           continue

        for v in v_declinations:
            if key.endswith(v[1:]):
                trunk = key[0:-1*len(v)+1]
                found = True
                if trunk[-1] in "aáeéiíoóöőuúüűv":
                    output.append(key) #fake match
                    break

                if trunk[-1] == trunk[-2]:
                    trunk = trunk[0:-1]
                    output.append(trunk)
        if found:
           continue
        output.append(key)

    output = list(dict.fromkeys(output))
    return output

def CollectNames(input_file, output_path, dictionary_path):
    dictionary = BuildDictionary(dictionary_path)

    keys = FindNames(input_file)
    keys = SplitNames(SplitNames(keys, " "), "-")
    keys = RemovePrefixes(keys)
    keys = FilterDeclinations(keys)

    keys = FindLowercase(keys, input_file)

    keys, transcribed = TranscribeKnownNames(dictionary, keys)
    abs, known_abs = TranscribeKnownNames(dictionary, FindAbreviations(input_file))
    shortenings = FindShortenings(input_file)

    print(keys)

    print("Collect")

with open("./dictimprove/probafile.txt", "r", encoding='utf-8') as input:
    content = input.read()
    CollectNames(content, "output.txt", "./dictimprove/probafile_dict.txt")

