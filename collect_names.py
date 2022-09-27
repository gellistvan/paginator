import re

def CollectNames(input_file, output_path):
    print('collect')
    # input_file = input.read()
    matches = re.findall(r"[^\.\?\!\-”\]] (([A-ZÖÜÓŐÚÉÁŰÍ][a-zöüóőúéáűí]{3,}[ \.\!\?\,\-])+)", input_file)
    keys=[]
    for item in matches:
        keys.append(item[0][0:-1])
    keys.sort()

    with open(output_path + "/output.txt", "w", encoding='utf-8') as output:
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

        last = keys[0]
        keys.sort()
        for key in keys[:]:
            if last != key and ((last not in key) or abs(len(key) - len(last)) > 3):
                last=key
                output.write(key + "\n")
            else:
                keys.remove(key)
    matches = re.findall(r"[^\.\?\!\-”\]] (([A-Z]{2,}[ \.\!\?\,\-])+)", input_file)
    keys=[]
    for item in matches:
        keys.append(item[0][0:-1])
    keys.sort()
    last = keys[0]
    with open(output_path + "/output.txt", "a", encoding='utf-8') as output:
        for key in keys[:]:
            if last != key and ((last not in key) or abs(len(key) - len(last)) > 3):
                last=key
                output.write(key + "\n")
            else:
                keys.remove(key)
