import string

from deep_translator import GoogleTranslator
from pydub import AudioSegment
import re
from gtts import gTTS
import os
from langdetect import detect

from datetime import datetime

import languages


def read_text(input_text):
    if input_text == "":
        with open("text_to_translate.txt", 'r') as file:
            return file.read()
    return input_text.strip()


def extract_sentences_from_file(input_text):
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', read_text(input_text))
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    return sentences


def text_to_speech(text, file_name, language='en', slow=False):
    tts = gTTS(text=text, lang=language, slow=slow)
    tts.save(f"audio_files/{file_name}")


def mp3_join(addition, base, silence_length=0):
    sound1 = AudioSegment.from_mp3(f"audio_files/{base}")
    sound2 = AudioSegment.from_mp3(f"audio_files/{addition}")

    if silence_length != 0:
        silence = AudioSegment.silent(duration=silence_length * 1000)
        sound2 = sound2 + silence

    combined = sound1 + sound2
    combined.export(f"audio_files/{base}", format="mp3")


def delete_files_except_base_title():
    files = os.listdir("audio_files")

    for file in files:
        if "_expendable" in file:
            os.remove(f"audio_files/{file}")


def detect_language(original_lan, text):
    if original_lan == "":
        try:
            language = detect(text)
            print(f"original language DETECTED - {languages.LANGUAGES.get(language)}")
            return language
        except:
            return "Language detection failed."

    if original_lan not in languages.LANGUAGES:
        raise Exception(f"!!! Language {original_lan} is not supported")
    print(f"original language SPECIFIED - {languages.LANGUAGES.get(original_lan)}")
    return original_lan


def get_title(title):
    if title != "":
        title = title.rstrip(string.punctuation + string.whitespace)
        print(f"{title}.mp3")
        return f"{title}.mp3".rstrip(string.punctuation + string.whitespace)
    else:
        print(f"title - {title}")
        return f"{datetime.now().strftime('%Y-%m-%d %Hh%Mm%Ss')}.mp3"


def get_audio_from_text(target_lan, original_lan="", base_title="", is_slow_org=False, is_slow_tra=False, silence=0,
                        first_original=True, input_text=""):
    org_len = detect_language(original_lan, read_text(input_text))
    # has mp3 in title
    base_title = f"{get_title(base_title)}"

    # get base mp3 file
    text_to_speech(text="a", file_name=base_title, language="en")
    sentences_org = extract_sentences_from_file(input_text)

    for index, s_org_text in enumerate(sentences_org):
        s_tra_text = GoogleTranslator(source='auto', target=target_lan).translate(s_org_text)

        org_mp3_title = f"org_{index}_expendable.mp3"
        tra_mp3_title = f"tra_{index}_expendable.mp3"

        text_to_speech(s_org_text, org_mp3_title, org_len, is_slow_org)
        text_to_speech(s_tra_text, tra_mp3_title, target_lan, is_slow_tra)

        # swap check
        if not first_original:
            temp = org_mp3_title
            org_mp3_title = tra_mp3_title
            tra_mp3_title = temp

        # add original mp3 to base
        mp3_join(org_mp3_title, base_title, silence_length=silence)  # added silence always goes after original audio
        # add translated mp3 to base
        mp3_join(tra_mp3_title, base_title)
        print(f"added {index + 1} sentence / {len(sentences_org)}")

        return base_title

    delete_files_except_base_title()
    print(
        f"+++ added file - audio_files/{base_title} | original language - {org_len} | target language - {target_lan}")
    print("------------------FINISHED---------------------")
