import epitran

epi = epitran.Epitran('eng-Latn')
value=epi.transliterate(u'Edmund Veesenmayer')
print(value + "\n")
print(value + "\n")