import string

from deep_translator import GoogleTranslator
from pydub import AudioSegment
import re
import nltk.data
from gtts import gTTS
import os
from langdetect import detect

from datetime import datetime

import languages


def read_sanitize_text(input_text):
    if input_text == "":
        with open("text_to_translate.txt", 'r') as file:
            return file.read()
    return input_text.strip().replace('\n', '').replace('\\n', '')


def extract_sentences_from_file(input_text, org_lan):
    print(f"Raw input text: {input_text}")

    tokenizer = nltk.data.load(f'tokenizers/punkt/{languages.LANGUAGES[org_lan].lower()}.pickle')
    sentences = tokenizer.tokenize(read_sanitize_text(input_text))
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]

    print(f"Number of sentences - {len(sentences)} : {sentences}")
    return sentences


def text_to_speech(text, file_name, language='en', slow=False):
    if text == "":
        silence = AudioSegment.silent(duration=1000)
        silence.export(f"audio_files/{file_name}", format="mp3")
    else:
        tts = gTTS(text=text, lang=language, slow=slow)
        tts.save(f"audio_files/{file_name}")


def mp3_join(addition, base, silence_length=0):
    base_sound = AudioSegment.from_mp3(f"audio_files/{base}")
    addition_sound = AudioSegment.from_mp3(f"audio_files/{addition}")

    if silence_length != 0:
        silence = AudioSegment.silent(duration=silence_length * 1000)
        addition_sound = addition_sound + silence

    combined = base_sound + addition_sound
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


def get_title(title, input_text):
    if title != "":
        print(f"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX.mp3")
        title = title.rstrip(string.punctuation + string.whitespace).replace("\n", "").replace("/n", "")
        print(f"{title}.mp3")
        return f"{title}.mp3".rstrip(string.punctuation + string.whitespace)
    else:
        title = f"{datetime.now().strftime('%Y-%m-%d %Hh%Mm%Ss')}.mp3"
        print(f"title - {title}")
        return f"{datetime.now().strftime('%Y-%m-%d %Hh%Mm%Ss')}.mp3"


def get_audio_from_text(target_lan, original_lan="", base_title="", is_slow_org=False, is_slow_tra=False, silence_seconds=0,
                        first_original=True, input_text=""):
    # get file title (has mp3 in title)
    base_title = f"{get_title(base_title, input_text)}"

    # detect language
    org_len = detect_language(original_lan, read_sanitize_text(input_text))

    # parse and create a list out of input text
    sentences_org = extract_sentences_from_file(input_text, org_len)

    # get base mp3 file
    text_to_speech(text="", file_name=base_title, language="en")

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
        mp3_join(org_mp3_title, base_title, silence_length=silence_seconds)  # added silence always goes after original audio
        # add translated mp3 to base
        mp3_join(tra_mp3_title, base_title)
        print(f"added {index + 1} sentence / {len(sentences_org)}")

    delete_files_except_base_title()
    print(
        f"+++ added file - audio_files/{base_title} | original language - {org_len} | target language - {target_lan}")
    print("------------------FINISHED---------------------")
    return base_title
