import io
import string
from datetime import datetime

import nltk.data
from deep_translator import GoogleTranslator
from gtts import gTTS
from langdetect import detect
from pydub import AudioSegment

import languages


def read_sanitize_text(input_text):
    if input_text == "":
        with open("text_to_translate.txt", 'r') as file:
            return file.read()
    return input_text.strip().replace('\n', '').replace('\\n', '').replace('.', '. ').replace('?', '? ')


def extract_sentences_from_file(input_text, org_lan):
    print(f"Raw input text: {input_text}")

    tokenizer = nltk.data.load(f'tokenizers/punkt/{languages.LANGUAGES[org_lan].lower()}.pickle')
    sentences = tokenizer.tokenize(read_sanitize_text(input_text))
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]

    print(f"Number of sentences - {len(sentences)} : {sentences}")
    return sentences


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
        title = title.rstrip(string.punctuation + string.whitespace).replace("\n", "").replace("/n", "")
        print(f"{title}.mp3")
        return f"{title}.mp3".rstrip(string.punctuation + string.whitespace)
    else:
        title = f"{datetime.now().strftime('%Y-%m-%d %Hh%Mm%Ss')}.mp3"
        print(f"title - {title}")
        return f"{datetime.now().strftime('%Y-%m-%d %Hh%Mm%Ss')}.mp3"


def generate_tts_audio_io(text, lang="en", slow=False):
    tts = gTTS(text=text, lang=lang, slow=slow)
    audio_io = io.BytesIO()
    tts.write_to_fp(audio_io)
    audio_io.seek(0)
    return audio_io


def get_audio_from_text(target_lan, original_lan="", base_title="", is_slow_org=False, is_slow_tra=False, silence_seconds=0,
                        first_original=True, input_text=""):
    # detect language
    org_lan = detect_language(original_lan, read_sanitize_text(input_text))

    # parse and create a list out of input text
    sentences_org = extract_sentences_from_file(input_text, org_lan)
    sentences_tra = [GoogleTranslator(source='auto', target=target_lan).translate(sen) for sen in sentences_org]

    final = AudioSegment.silent(duration=1000)
    for index, _ in enumerate(sentences_org):
        org_audio_io = generate_tts_audio_io(text=sentences_org[index], lang=org_lan, slow=is_slow_org)
        tra_audio_io = generate_tts_audio_io(text=sentences_tra[index], lang=target_lan, slow=is_slow_tra)

        org_audio_segment = AudioSegment.from_file(org_audio_io, format="mp3")
        tra_audio_segment = AudioSegment.from_file(tra_audio_io, format="mp3")

        # swap check
        if not first_original:
            temp = org_audio_segment
            org_audio_segment = tra_audio_segment
            tra_audio_segment = temp

        combined_audio = org_audio_segment + AudioSegment.silent(duration=silence_seconds * 1000) + tra_audio_segment + AudioSegment.silent(duration=0.5 * 1000)
        final = final + combined_audio

        print(f"added {index + 1} sentence / {len(sentences_org)}")

    final_file_path = f"audio_files/{get_title(base_title, input_text)}"
    final.export(final_file_path, format="mp3")

    print(
        f"+++ added file - {final_file_path} | original language - {org_lan} | target language - {target_lan}")
    print("------------------FINISHED---------------------")
    return final_file_path
