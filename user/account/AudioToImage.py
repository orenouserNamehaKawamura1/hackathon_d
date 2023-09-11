from pydub import AudioSegment
import speech_recognition as sr
from dotenv import load_dotenv
import os
import json
import openai
import MeCab
import collections
import io

class AudioToImage:
    def __init__(self, audio_path):
        self.audio_path = audio_path

        # APIキー関係
        load_dotenv(verbose=True)
        dotenv_path = os.path.join(os.getcwd(), '.env')
        load_dotenv(dotenv_path)
        openai.api_key = os.environ["OPENAI_API_KEY"]

    # mp3から画像へ変換する関数
    def convert_mp3_to_wav(self):
        if self.audio_path.endswith(".mp3"):
            audio = AudioSegment.from_mp3(self.audio_path)
        elif self.audio_path.endswith(".wav"):
            audio = AudioSegment.from_wav(self.audio_path)
        else:
            raise Exception("対応していない拡張子です")
        
        return audio

    # 音声を分割して文字起こしする関数
    def process_audio_segments(self, audio, segment_length):
        recognizer = sr.Recognizer()
        words = []

        for i, start in enumerate(range(0, len(audio), segment_length * 1000)):
            segment = audio[start:start + segment_length * 1000]

            temp_wav = io.BytesIO()
            segment.export(temp_wav, format="wav")
            temp_wav.seek(0)

            with sr.AudioFile(temp_wav) as source:
                audio_segment = recognizer.record(source)

                try:
                    text = recognizer.recognize_google(audio_segment, language="ja-JP")
                    words.extend(text.split())
                    print(f"Segment {i} の文字起こし結果:", text)
                except sr.UnknownValueError:
                    print(f"Segment {i} の音声を認識できませんでした")
                except sr.RequestError as e:
                    print(f"Segment {i} のAPIリクエストでエラーが発生しました:", e)

        return words
    
    # 文字列を受け取って、人気のある単語を返す関数
    def convert_words_to_popular_prompt(self, words):
        final_text = "".join(words)

        model = MeCab.Tagger("-Owakati")
        parsed_words = model.parse(final_text).split()
        parsed_words = [word for word in parsed_words if len(word) > 1]
        counter = collections.Counter(parsed_words)

        return json.dumps(counter.most_common(20), ensure_ascii=False)

    # DALL-Eにリクエストして画像のURLを返す関数
    def convert_word_to_image(self, word):
        # DALL-E リクエスト
        response = openai.Image.create(
            model="image-alpha-001",
            prompt=word,
            n=1,
            size="512x512",
            response_format="url"
        )

        return response['data'][0]['url']

# 処理が重いのでスレッド化
def thread_func(filename):
    segment_length = 30  # 30秒ごとに分割

    audio_processor = AudioToImage(f'./temp/uploads/{filename}')
    audio = audio_processor.convert_mp3_to_wav()
    words = audio_processor.process_audio_segments(audio, segment_length)
    prompt = audio_processor.convert_words_to_popular_prompt(words)
    image_url = audio_processor.convert_word_to_image(prompt)

    # データベース登録用処理ここに書く
    print(image_url)