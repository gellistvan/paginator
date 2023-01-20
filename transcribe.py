

import pronouncing

def get_phonetic_transcription(name):
    # Use the pronouncing library to get the IPA transcription of the name
    transcription = pronouncing.phones_for_word(name)
    # If there are multiple transcriptions, take the first one
    if len(transcription) > 0:
        return transcription[0]
    else:
        return None

# Test the function with the list of names
names = ["Alboise", "Angèle", "Antoine", "Cavaignac", "Poujols"]
for name in names:
    transcription = get_phonetic_transcription(name)
    if transcription:
        print(f"{name}: {transcription}")
    else:
        print(f"No transcription found for {name}")