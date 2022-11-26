import re

vovels = ["a", "á", "e", "é", "i", "í", "o", "ó", "ö", "ő", "u", "ú", "ü", "ű"]
v_declinations = ["val", "vel", "vá", "vé"]
declinations = ["nak", "nek", "ért", "ban", "ben", "ba", "be", "on", "en", "ön", "nál", "nél", "ra", "re", "hoz", "hez", "höz", "ból", "ből", "ról", "ről", "tól", "től", "ig", "ként", "ul", "ül"]
plurals = ["ak", "ok", "ek", "ök"]

def is_plural(key):
    if len(key) < 6:
        return False

    for p in plurals:
        if key.endswith(p) and key[-3] not in vovels:
            return True
    return False


def PostprocessDictionary(dictionary):
    output = []

    for entry in dictionary:
        found = False
        for d in declinations:
            if entry[0].endswith(d) and entry[0].endswith(d):
                trunk = entry[0][0:-1*len(d)]
                trunk_pron = entry[1][0:-1*len(d)]
                output.append((trunk, trunk_pron))
                if trunk[-1] == 'á':
                    trunk = trunk[0:-1] +'a'
                    trunk_pron = trunk_pron[0:-1] +'a'
                    output.append((trunk, trunk_pron))
                elif trunk[-1] == 'é':
                    trunk = trunk[0:-1] +'e'
                    trunk_pron = trunk_pron[0:-1] +'e'
                    output.append((trunk, trunk_pron))

                if len(d) < 3:
                    output.append(entry)
                found = True
                break

        if found:
            continue

        for v in v_declinations:
            if entry[0].endswith(v) and entry[1].endswith(v):
                trunk = entry[0][0:-1*len(v)]
                trunk_pron = entry[1][0:-1*len(v)]
                output.append((trunk, trunk_pron))
                found = True

                if trunk[-1] not in "áéiíoóöőuúüűv":
                    output.append(entry)  # fake rag
                    break

                output.append((trunk, trunk_pron))
                if trunk[-1] == 'á':
                    trunk = trunk[0:-1] +'a'
                    trunk_pron = trunk_pron[0:-1] +'a'
                    output.append((trunk, trunk_pron))
                elif trunk[-1] == 'é':
                    trunk = trunk[0:-1] +'e'
                    trunk_pron = trunk_pron[0:-1] +'e'
                    output.append((trunk, trunk_pron))

        if found:
            continue

        for v in v_declinations:
            if entry[0].endswith(v[1:]) and entry[1].endswith(v[1:]):
                trunk = entry[0][0:-1*len(v)+1]
                trunk_pron = entry[1][0:-1*len(v)+1]
                found = True
                if trunk[-1] in "aáeéiíoóöőuúüűv":
                    output.append(entry) #fake match
                    break

                if trunk[-1] == trunk[-2]:
                    trunk = trunk[0:-1]
                    trunk_pron = trunk_pron[0:-1]
                    output.append((trunk, trunk_pron))
        if found:
            continue

        output.append(entry)

    return output

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

            #if not found:
            output.append((values[0].lstrip(), values[1].rstrip()))

    return PostprocessDictionary(output)

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
    if len(keys) < 2:
        return keys

    output = [keys[0]]
    start_index = 0
    i = 1
    while i < len(keys):
        if keys[i] != keys[start_index] and ((keys[start_index] not in keys[i]) or abs(len(keys[i]) - len(keys[start_index])) > 3):
            start_index = i

            output.append(keys[i])
        i = i + 1

    output.sort()
    return output

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

def find_steams(key):
    output = []
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

            # if len(d) < 3:
            #     output.append(key)
            return output

    for v in v_declinations:
        if key.endswith(v):
            trunk = key[0:-1*len(v)]

            if trunk[-1] not in "áéiíoóöőuúüűv":
                break

            output.append(trunk)
            if trunk[-1] == 'á':
                trunk = trunk[0:-1] +'a'
                output.append(trunk)
            elif trunk[-1] == 'é':
                trunk = trunk[0:-1] +'e'
                output.append(trunk)

            return output

    for v in v_declinations:
        if key.endswith(v[1:]):
            trunk = key[0:-1*len(v)+1]
            if trunk[-1] in "aáeéiíoóöőuúüűv":
                break

            if trunk[-1] == trunk[-2]:
                trunk = trunk[0:-1]
                output.append(trunk)

    return output

def FilterDeclinations(keys):
    all_steams = []
    for key in keys:
        steams = find_steams(key)
        if len(steams) == 1 and is_plural(steams[0]) :
            steams = [steams[0][0:-2]]
            # print("\t" + str(steams))
        if len(steams) and  4 < len(sorted(steams, reverse=True, key=len)[0]):
            all_steams.append(steams)
        else:
            all_steams.append([])
        print(key + " " + str(all_steams[-1]))

    output = [keys[0]]

    for index in range(1, len(keys)):
        if len(all_steams[index]) and 4 > len(sorted(all_steams[index], reverse=True, key=len)[0]):
            output.append(keys[index])
            output.extend(all_steams[index])
            continue

        has_other = False

        for steam in all_steams[index]:
            if len(steam) > 3:
                for i in range(index + 1, len(keys)):
                    if keys[index][0:3] != keys[i][0:3]:
                        break

                    if steam in all_steams[i] or keys[i].startswith(steam):
                        # if keys[i].startswith(steam):
                        #     print(str(all_steams[index]) + " " + keys[i])
                        has_other = True
                        break

                if not has_other:
                    for i in range(index -1, 0, -1):
                        if keys[index][0:3] != keys[i][0:3]:
                            break
                        if steam in all_steams[i] or keys[i].startswith(steam):
                            has_other = True
                            break

                if has_other:
                    break

        if has_other:
            output.extend(all_steams[index])
        else:
            output.append(keys[index])

    return list(dict.fromkeys(output))

def FilterDeclinations2(keys):
    output = []
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
                if trunk[-1] in "aáeéiíoóöőuúüűv":
                    output.append(key) #fake match
                    break

                if trunk[-1] == trunk[-2]:
                    found = True
                    trunk = trunk[0:-1]
                    output.append(trunk)
        if found:
           continue
        output.append(key)

    output = list(dict.fromkeys(output))
    return output


def WriteEntries(entries, output_path, mode):
    if len(entries) == 0:
        return

    last = entries[0]
    with open(output_path, mode, encoding='utf-8') as output:
        for key in entries[:]:
            if last != key and ((last not in key) or abs(len(key) - len(last)) > 3):
                last=key
                output.write(key + "\n")
            else:
                entries.remove(key)

def CollectNames2(input_file, output_path, dictionary_path):
    print()
    print()
    dictionary = BuildDictionary(dictionary_path)
    print(dictionary)
    print("----------------")
    keys = FindNames(input_file)
    keys = SplitNames(SplitNames(keys, " "), "-")
    keys = RemovePrefixes(keys)
    keys = FilterDeclinations(keys)

    #keys = FindLowercase(keys, input_file)

    keys, transcribed = TranscribeKnownNames(dictionary, keys)
    abs, known_abs = TranscribeKnownNames(dictionary, FindAbreviations(input_file))
    shortenings = FindShortenings(input_file)

    WriteEntries(keys, output_path, "w")
    WriteEntries(abs, output_path, "a")
    WriteEntries(transcribed, output_path, "a")
    WriteEntries(known_abs, output_path, "a")

    return "\n ".join(keys) + "\n " + "\n ".join(abs)
#

import os
for filename in os.listdir("./new_books/06. Oknyomozás, életrajz/"):
    f = os.path.join("./new_books/06. Oknyomozás, életrajz/", filename)
    if not filename.endswith("txt"):
        continue
    with open(f, "r", encoding='utf-8') as input:
        content = input.read()
        keys = CollectNames2(content, "./new_books/06. Oknyomozás, életrajz/dict/dict_" + filename, "./big_dict.txt")

# with open("./09 doberdo_isonzo_tirol.txt", "r", encoding='utf-8') as input:
#     content = input.read()
#     keys = CollectNames2(content, "dictimprove/output.txt", "./big_dict.txt")
#
