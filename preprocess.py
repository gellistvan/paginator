import re
import sys, getopt
from PyPDF2 import PdfReader

def replace_roman(text):
    text = text.replace(" XXX.", " 30.")
    text = text.replace(" XXIX.", " 29.")
    text = text.replace(" XXVIII.", " 28.")
    text = text.replace(" XXVII.", " 27.")
    text = text.replace(" XXVI.", " 26.")
    text = text.replace(" XXV.", " 25.")
    text = text.replace(" XXIV.", " 24.")
    text = text.replace(" XXIII.", " 23.")
    text = text.replace(" XXII.", " 22.")
    text = text.replace(" XXI.", " 21.")
    text = text.replace(" XX.", " 20.")
    text = text.replace(" XIX.", " 19.")
    text = text.replace(" XVIII.", " 18.")
    text = text.replace(" XVII.", " 17.")
    text = text.replace(" XVI.", " 16.")
    text = text.replace(" XV.", " 15.")
    text = text.replace(" XIV.", " 14.")
    text = text.replace(" XIII.", " 13.")
    text = text.replace(" XII.", " 12.")
    text = text.replace(" XI.", " 11.")
    text = text.replace(" IX.", " 9.")
    text = text.replace(" X.", " 10.")
    text = text.replace(" VIII.", " 8.")
    text = text.replace(" VII.", " 7.")
    text = text.replace(" VI.", " 6.")
    text = text.replace(" IV.", " 4.")
    text = text.replace(" V.", " 5.")
    text = text.replace(" III.", " 3.")
    text = text.replace(" II.", " 2.")
    text = text.replace(" I.", " 1.")
    return text

def replace_dates(text):
    text = text.replace(" 10-i", " tizedikei")
    text = text.replace(" 11-i", " tizenegyedikei")
    text = text.replace(" 12-i", " tizenkettedikei")
    text = text.replace(" 13-i", " tizenharmadikai")
    text = text.replace(" 14-i", " tizennegyedikei")
    text = text.replace(" 15-i", " tizenötödikei")
    text = text.replace(" 16-i", " tizenhatodikai")
    text = text.replace(" 17-i", " tizenhetedikei")
    text = text.replace(" 18-i", " tizennyolcadikai")
    text = text.replace(" 19-i", " tizenkilencedikei")
    text = text.replace(" 20-i", " huszadikai")
    text = text.replace(" 21-i", " huszonegyedikei")
    text = text.replace(" 22-i", " huszonkettedikei")
    text = text.replace(" 23-i", " huszonharmadikai")
    text = text.replace(" 24-i", " huszonnegyedikei")
    text = text.replace(" 25-i", " huszonötödikei")
    text = text.replace(" 26-i", " huszonhatodikai")
    text = text.replace(" 27-i", " huszonhetedikei")
    text = text.replace(" 28-i", " huszonnyolcadikai")
    text = text.replace(" 29-i", " huszonkilencedikei")
    text = text.replace(" 30-i", " harmincadikai")
    text = text.replace(" 31-i", " harmincegyedikei")
    text = text.replace(" 1-jei", " elsejei")
    text = text.replace(" 2-i", " másodikai")
    text = text.replace(" 3-i", " harmadikai")
    text = text.replace(" 4-i", " negyedikei")
    text = text.replace(" 5-i", " ötödikei")
    text = text.replace(" 6-i", " hatodikai")
    text = text.replace(" 7-i", " hetedikei")
    text = text.replace(" 8-i", " nyolcadikai")
    text = text.replace(" 9-i", " kilencedikei")
    text = text.replace(" 11-én", " tizenegyedikén")
    text = text.replace(" 12-én", " tizenkettedikén")
    text = text.replace(" 13-án", " tizenharmadikán")
    text = text.replace(" 14-én", " tizennegyedikén")
    text = text.replace(" 15-én", " tizenötödikén")
    text = text.replace(" 16-án", " tizenhatodikán")
    text = text.replace(" 17-én", " tizenhetedikén")
    text = text.replace(" 18-án", " tizennyolcadikán")
    text = text.replace(" 19-én", " tizenkilencedikén")
    text = text.replace(" 20-án", " huszadikán")
    text = text.replace(" 21-én", " huszonegyedikén")
    text = text.replace(" 22-én", " huszonkettedikén")
    text = text.replace(" 23-án", " huszonharmadikán")
    text = text.replace(" 24-én", " huszonnegyedikén")
    text = text.replace(" 25-én", " huszonötödikén")
    text = text.replace(" 26-án", " huszonhatodikán")
    text = text.replace(" 27-én", " huszonhetedikén")
    text = text.replace(" 28-án", " huszonnyolcadikán")
    text = text.replace(" 29-én", " huszonkilencedikén")
    text = text.replace(" 30-án", " harmincadikán")
    text = text.replace(" 31-én", " harmincegyedikén")
    text = text.replace(" 1-jén", " elsején")
    text = text.replace(" 2-án", " másodikán")
    text = text.replace(" 3-án", " harmadikán")
    text = text.replace(" 4-én", " negyedikén")
    text = text.replace(" 5-én", " ötödikén")
    text = text.replace(" 6-án", " hatodikán")
    text = text.replace(" 7-én", " hetedikén")
    text = text.replace(" 8-án", " nyolcadikán")
    text = text.replace(" 9-én", " kilencedikén")
    text = text.replace(" 10-én", " tizedikén")
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
    text = re.sub(r"(\s)dr\. ", r"\rdoktor ", text)
    text = re.sub(r"(\s)Dr\. ", r"\rdoktor ", text)
    text = re.sub(r"(\s)Mr\. ", r"\rmiszter ", text)
    text = re.sub(r"(\s)Mrs\. ", r"\rmiszisz ", text)
    return text

def replace_uinits(text):
    text = re.sub(r"(\d) *km(\s)", r"\1 kilométer\2", text)
    text = re.sub(r"(\d) *m(\s)", r"\1 méter\2", text)
    text = re.sub(r"(\d) *dm(\s)", r"\1 deciméter\2", text)
    text = re.sub(r"(\d) *cm(\s)", r"\1 centiméter\2", text)
    text = re.sub(r"(\d) *mm(\s)", r"\1 miliméter\2", text)
    text = re.sub(r"(\d) *l(\s)", r"\1 liter\2", text)
    text = re.sub(r"(\d) *dl(\s)", r"\1 deciliter\2", text)
    text = re.sub(r"(\d) *cl(\s)", r"\1 centiliter\2", text)
    text = re.sub(r"(\d) *ml(\s)", r"\1 mililiter\2", text)
    text = re.sub(r"(\d) *m3(\s)", r"\1 köbméter\2", text)
    text = re.sub(r"(\d) *cm3(\s)", r"\1 köbcenti\2", text)
    text = re.sub(r"(\d) *m2(\s)", r"\1 négyzetméter\2", text)
    text = re.sub(r"(\d) *cm2(\s)", r"\1 négyzetcentiméter\2", text)
    text = re.sub(r"(\d) *g(\s)", r"\1 gramm\2", text)
    text = re.sub(r"(\d) *kg(\s)", r"\1 kilogramm\2", text)
    text = re.sub(r"(\d) *dkg(\s)", r"\1 dekagramm\2", text)
    text = re.sub(r"(\d) *J(\s)", r"\1 zsúl\2", text)
    text = re.sub(r"(\d) *W(\s)", r"\1 vatt\2", text)
    text = re.sub(r"(\d) *V(\s)", r"\1 volt\2", text)
    text = re.sub(r"(\d) *A(\s)", r"\1 amper\2", text)
    text = re.sub(r"(\d) *T(\s)", r"\1 teszla\2", text)
    text = re.sub(r"(\d) *km/h(\s)", r"\1 kilométer per óra\2", text)
    text = re.sub(r"(\d) *m/s(\s) ", r"\1 méter per szekundum\2", text)
    text = re.sub(r"(\d) *h(\s)", r"\1 óra\2", text)
    text = re.sub(r"(\d) *p(\s)", r"\1 perc\2", text)
    text = re.sub(r"(\d) *mp(\s)", r"\1 másodperc\2", text)
    text = re.sub(r"(\d) *Ft(\s)", r"\1 forint\2", text)
    text = re.sub(r"(\d) *ft(\s)", r"\1 forint\2", text)
    text = re.sub(r"(\d) *Ft\.(\s)", r"\1 forint\2", text)
    text = re.sub(r"(\d) *HUF(\s)", r"\1 forint\2", text)
    text = re.sub(r"(\d) *USD(\s)", r"\1 dollár\2", text)
    text = re.sub(r"(\d) *CHF(\s)", r"\1 svájci frank\2", text)
    text = re.sub(r"(\d) *GBP(\s)", r"\1 angol font\2", text)
    text = re.sub(r"(\d) *EUR(\s)", r"\1 euró\2", text)
    text = re.sub(r"(\d) *C(\s)", r"\1 celziuszfok\2", text)
    text = re.sub(r"(\d) *°C(\s)", r"\1 celziuszfok\2", text)
    return text

def replace_math(text):
    text = re.sub(r"(\d+)-(\d+)(.{0,8}) között", r"\1 és \2\3 között", text)
    text = re.sub(r"(\d+)–(\d+)(.{0,8}) között", r"\1 és \2\3 között", text)
    text = re.sub(r"(\d+) *\+ *(\d+)", r"\1 plusz \2" ,text)
    text = re.sub(r"(\d+) *\* *(\d+)", r"\1 szorozva \2" ,text)
    text = re.sub(r"(\d+) */ *(\d+)", r"\1 per \2" ,text)
    text = re.sub(r"(\d+) *= *(\d+)", r"\1 egyenlő \2" ,text)
    text = re.sub(r"(\d+),5 ", r"\1 és fél ", text)
    text = re.sub(r"(\d+),(\d+)%", r"\1,\2 százalék", text)
    text = re.sub(r"(\d+),(\d) ", r"\1 egész \2 tized ", text)
    text = re.sub(r"(\d+),(\d\d) ", r"\1 egész \2 század ", text)
    text = re.sub(r"(\d+),(\d\d\d) ", r"\1 egész \2 ezred ", text)
    text = re.sub(r"(\d) (\d{3}) ", r"\1\2", text)
    text = re.sub(r"(\d) (\d{3}) ", r"\1\2", text)
    text = re.sub(r"(\d) (\d{3}) ", r"\1\2", text)
    text = re.sub(r"(\d)\.(\d{3})([ .])", r"\1\2\3", text)
    text = re.sub(r"(\d)\.(\d{3})([ .])", r"\1\2\3", text)
    text = re.sub(r"(\d)\.(\d{3})([ .])", r"\1\2\3", text)
    text = re.sub(r"([\r\n])\d+[\r\n]", r"\1", text)
    text = re.sub(r"(\d)-(\d+)", r"\1 - \2", text)
    text = re.sub(r"(\d)–(\d+)", r"\1 - \2", text)
    return text

def preprocess(text):
    text = re.sub(r"\[\d+]", r"", text)
    text = re.sub(r"(\r\n)+", r"\r\n", text)
    text = re.sub(r"(\d) (\d{3})([\\., :?!%])", r"\1\2\3", text, 2)
    text = re.sub(r"(\d) (\d{3})([\\., :?!%])", r"\1\2\3", text, 2)
    text = re.sub(r"(\d) (\d{3})([\\., :?!%])", r"\1\2\3", text, 2)
    text = re.sub(r"(\d) (\d{3})([\\., :?!%])", r"\1\2\3", text, 2)
    text = re.sub(r"\((\d{1,2}[14579]0) - (\d{3,4})\)", r"\1-től \2-ig", text)
    text = re.sub(r"\((\d{1,2}[2368]0) - (\d{3,4})\)", r"(\1-tól \2-ig)", text)
    text = re.sub(r"\((\d{2,3}[368]) - (\d{3,4})\)", r"(\1-tól \2-ig)", text)
    text = re.sub(r"\((\d{2,3}[124579]) - (\d{3,4})\)", r"(\1-től \2-ig)", text)
    text = re.sub(r"Kr\. e\.", "krisztus előtt", text)
    text = re.sub(r"Kr\. e\.", "krisztus előtt", text)
    text = re.sub(r"Kr\.u\.", "krisztus után", text)
    text = re.sub(r"Kr\. u\.", "krisztus után", text)
    text = re.sub(r"i\.e\.", "időszámításunk előtt", text)
    text = re.sub(r"i\. e\.", "időszámításunk előtt", text)
    text = re.sub(r"(\d+)\. (jan|feb|márc|ápr|máj|jún|júl|aug|szept|okt|nov|dec)", r"\1 \2", text)
    text = re.sub(r"\r\n\s*\d+\s*\r\n", r"\r\n", text)
    text = replace_dates(text)
    text = replace_roman(text)
    text = replace_uinits(text)
    text = replace_math(text)
    text = re.sub(r"\[\d+]", "", text)
    text = re.sub(r"{\d+}", "", text)


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