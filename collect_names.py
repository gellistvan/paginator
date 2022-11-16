import re

vovels = ["a", "á", "e", "é", "i", "í", "o", "ó", "ö", "ő", "u", "ú", "ü", "ű"]
v_declinations = ["al", "el", "á", "é", "ár", "ér"]
declinations = ["t", "nak", "nek", "ért", "ban", "ben", "ba", "be", "on", "en", "ön", "nál", "nél", "ra", "re", "hoz", "hez", "höz", "ból", "ből", "ról", "ről", "tól", "től", "ig", "ként", "ul", "ül", "i"]

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

            if not found:
                output.append((values[0].lstrip(), values[1].rstrip()))

    return output

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

def FindNames(input_file):
    matches = re.findall(r"[^\.\?\!\-”\]–] (([A-ZÖÜÓŐÚÉÁŰÍ][a-zöüóőúéáűí]{3,}[ \.\!\?\,\-])+)", input_file)
    keys=[]
    for item in matches:
        keys.append(item[0][0:-1])
    keys.sort()
    return keys

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

def FindAbreviations(input_file):
    matches = re.findall(r"[^\.\?\!\-”\]] (([A-Z]{2,}[ \.\!\?\,\-])+)", input_file)
    keys=[]
    for item in matches:
        keys.append(item[0][0:-1])
    keys.sort()
    return keys

def WriteEntries(entries, output_path, mode):
    last = entries[0]
    with open(output_path, mode, encoding='utf-8') as output:
        for key in entries[:]:
            if last != key and ((last not in key) or abs(len(key) - len(last)) > 3):
                last=key
                output.write(key + "\n")
            else:
                entries.remove(key)

def SplitNames(keys, delimiter):
    output=[]
    for key in keys:
        entries = key.split(delimiter)
        for entry in entries:
            if entry not in output:
                output.append(entry)
    output.sort()
    return output

def CollectNames(input_file, output_path, dictionary_path):
    dictionary = BuildDictionary(dictionary_path)

    keys = FindNames(input_file)
    keys = SplitNames(SplitNames(keys, " "), "-")
    keys = RemovePrefixes(keys)


    keys, transcribed = TranscribeKnownNames(dictionary, keys)
    abs, known_abs = TranscribeKnownNames(dictionary, FindAbreviations(input_file))

    WriteEntries(keys, output_path, "w")
    WriteEntries(abs, output_path, "a")
    WriteEntries(transcribed, output_path, "a")
    WriteEntries(known_abs, output_path, "a")

    return "\n ".join(keys) + "\n " + "\n ".join(abs)