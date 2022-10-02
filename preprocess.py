import re
import sys, getopt
from PyPDF2 import PdfReader

def replace_dates(text):
    text = text.replace("10-i", "tizedikei")
    text = text.replace("11-i", "tizenegyedikei")
    text = text.replace("12-i", "tizenkettedikei")
    text = text.replace("13-i", "tizenharmadikai")
    text = text.replace("14-i", "tizennegyedikei")
    text = text.replace("15-i", "tizenötödikei")
    text = text.replace("16-i", "tizenhatodikai")
    text = text.replace("17-i", "tizenhetedikei")
    text = text.replace("18-i", "tizennyolcadikai")
    text = text.replace("19-i", "tizenkilencedikei")
    text = text.replace("20-i", "huszadikai")
    text = text.replace("21-i", "huszonegyedikei")
    text = text.replace("22-i", "huszonkettedikei")
    text = text.replace("23-i", "huszonharmadikai")
    text = text.replace("24-i", "huszonnegyedikei")
    text = text.replace("25-i", "huszonötödikei")
    text = text.replace("26-i", "huszonhatodikai")
    text = text.replace("27-i", "huszonhetedikei")
    text = text.replace("28-i", "huszonnyolcadikai")
    text = text.replace("29-i", "huszonkilencedikei")
    text = text.replace("30-i", "harmincadikai")
    text = text.replace("31-i", "harmincegyedikei")
    text = text.replace("1-jei", "elsejei")
    text = text.replace("2-i", "másodikai")
    text = text.replace("3-i", "harmadikai")
    text = text.replace("4-i", "negyedikei")
    text = text.replace("5-i", "ötödikei")
    text = text.replace("6-i", "hatodikai")
    text = text.replace("7-i", "hetedikei")
    text = text.replace("8-i", "nyolcadikai")
    text = text.replace("9-i", "kilencedikei")
    text = text.replace("11-én", "tizenegyedikén")
    text = text.replace("12-én", "tizenkettedikén")
    text = text.replace("13-án", "tizenharmadikán")
    text = text.replace("14-én", "tizennegyedikén")
    text = text.replace("15-én", "tizenötödikén")
    text = text.replace("16-án", "tizenhatodikán")
    text = text.replace("17-én", "tizenhetedikén")
    text = text.replace("18-án", "tizennyolcadikán")
    text = text.replace("19-én", "tizenkilencedikén")
    text = text.replace("20-án", "huszadikán")
    text = text.replace("21-én", "huszonegyedikén")
    text = text.replace("22-én", "huszonkettedikén")
    text = text.replace("23-án", "huszonharmadikán")
    text = text.replace("24-én", "huszonnegyedikén")
    text = text.replace("25-én", "huszonötödikén")
    text = text.replace("26-án", "huszonhatodikán")
    text = text.replace("27-én", "huszonhetedikén")
    text = text.replace("28-án", "huszonnyolcadikán")
    text = text.replace("29-én", "huszonkilencedikén")
    text = text.replace("30-án", "harmincadikán")
    text = text.replace("31-én", "harmincegyedikén")
    text = text.replace("1-jén", "elsején")
    text = text.replace("2-án", "másodikán")
    text = text.replace("3-án", "harmadikán")
    text = text.replace("4-én", "negyedikén")
    text = text.replace("5-én", "ötödikén")
    text = text.replace("6-án", "hatodikán")
    text = text.replace("7-én", "hetedikén")
    text = text.replace("8-án", "nyolcadikán")
    text = text.replace("9-én", "kilencedikén")
    text = text.replace("10-én", "tizedikén")
    text = text.replace(" jan.", " január")
    text = text.replace(" feb.", " február")
    text = text.replace(" márc.", " márchius")
    text = text.replace(" ápr.", " április")
    text = text.replace(" máj.", " május")
    text = text.replace(" jún.", " június")
    text = text.replace(" júl.", " július")
    text = text.replace(" aug.", " augusztus")
    text = text.replace(" szept.", " szeptember")
    text = text.replace(" okt.", " október")
    text = text.replace(" nov.", " november")
    text = text.replace(" dec.", " december")
    text = text.replace(" Sir ", " szőr ")
    return text

def preprocess(text):
    text = re.sub(r"(\d)\-(\d+)", r"\1 - \2", text)
    text = re.sub(r"(\d)–(\d+)", r"\1 - \2", text)
    text = re.sub(r"\[\d+\]", r"", text)
    text = re.sub(r"(\r\n)+", r"\r\n", text)
    text = re.sub(r"(\d) (\d{3})([\\., :?!%])", r"\1\2\3", text, 2)
    text = re.sub(r"(\d) (\d{3})([\\., :?!%])", r"\1\2\3", text, 2)
    text = re.sub(r"(\d) (\d{3})([\\., :?!%])", r"\1\2\3", text, 2)
    text = re.sub(r"(\d) (\d{3})([\\., :?!%])", r"\1\2\3", text, 2)
    text = re.sub(r"(\d+)\. (jan|feb|márc|ápr|máj|jún|júl|aug|szept|okt|nov|dec)", r"\1 \2", text)
    text = re.sub(r"\r\n\s*\d+\s*\r\n", r"\r\n", text)
    text = replace_dates(text)
    return text


#input_path=''
#output_path=''
#header_range='0'
#page_range='0'
#try:
#    opts, args = getopt.getopt(sys.argv[1:], "ho:i:H:R:", ["help", "output="])
#except getopt.GetoptError as err:
#    # print help information and exit:
#    print(err)  # will print something like "option -a not recognized"
#    # usage()
#    sys.exit(2)
#for o, a in opts:
#    if o in ("-h", "--help"):
#        # usage()
#        sys.exit()
#    elif o in ("-o", "--output"):
#        output_path = a
#    elif o in ("-i", "--input"):
#        input_path = a
#    elif o in ("-H", "--header-range"):
#        header_range=a
#    elif o in ("-R", "--range"):
#        page_range = a
#
#def parse_range(text, num_pages):
#    items = text.split(",")
#    output = []
#    for item in items:
#        if item.isnumeric():
#            output.append(int(item))
#
#        elif re.fullmatch(r"\d+\-\d*", item):
#            limits = item.split("-")
#            r = range(int(limits[0]), int(limits[1])) if limits[1] != '' else range(int(limits[0]), num_pages)
#            for val in r:
#                output.append(val)
#    return output
#
#reader = PdfReader(input_path)
#num_pages = reader.getNumPages()
#valid_pages = parse_range(page_range, num_pages)
#header_pages = parse_range(header_range, num_pages)
#
#text = ""
#for pagenum in range(0, num_pages):
#    if pagenum in valid_pages:
#        page_text = reader.pages[pagenum].extractText()
#        if pagenum in header_pages:
#            lines = page_text.split("\n")
#            page_text = "\n".join(lines[1:])
#        text += page_text
#
#with open(output_path, "w", encoding='utf-8') as output:
#    output.write(text)
#
#
##page4 = reader.pages[3]
##print(page4.extractText())