import pyaudio
import wave
import struct
import numpy as np

import os
import json

def credentials():
    # Carregando o arquivo JSON
    with open("/Users/romuloconceicao/.openai/credentials.json") as json_file:
        credentials = json.load(json_file)

    os.environ["OPENAI_API_KEY"] = credentials['api_key']

    #https://codelabs.developers.google.com/codelabs/cloud-speech-text-python3#3
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/romuloconceicao/.gcp/credentials.json"

    return 0

def recording(path, filename):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = f"{path}/{filename}.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    return 0

def convert(path, filename):
    import ffmpeg

    stream = ffmpeg.input(f"{path}/{filename}.wav")
    stream = ffmpeg.output(stream, f"{path}/{filename}.flac")

    return ffmpeg.run(stream, overwrite_output=True)

def recognize(path, filename):
    import io

    from google.cloud import speech_v1p1beta1

    # Cria um cliente de reconhecimento de fala
    client = speech_v1p1beta1.SpeechClient()

    # Carrega o arquivo .flac
    with io.open(f"{path}/{filename}.flac", "rb") as audio_file:
        content = audio_file.read()

    # Configura a requisição de reconhecimento de fala
    audio = speech_v1p1beta1.types.RecognitionAudio(content=content)
    config = speech_v1p1beta1.types.RecognitionConfig(
        encoding=speech_v1p1beta1.RecognitionConfig.AudioEncoding.FLAC,
        language_code="pt-BR",
        sample_rate_hertz=44100,
        audio_channel_count=2
    )

    # Cria uma requisição de reconhecimento de fala
    request = speech_v1p1beta1.types.RecognizeRequest(audio=audio, config=config)

    # Envia a requisição de reconhecimento de fala
    response = client.recognize(request)

    # Imprime a transcrição resultante
    for result in response.results:
        transcricao = result.alternatives[0].transcript

    return transcricao

def openai(pergunta):
    import openai

    # Inicialize a chave da API OpenAI
    openai.api_key = os.environ["OPENAI_API_KEY"]

    # Defina os parâmetros da sua solicitação à API
    model_engine = "text-davinci-002"
    prompt = (f"{pergunta}")

    # Faça a solicitação à API e receba a resposta
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # Imprima a resposta
    return response["choices"][0]["text"]

def speech(path, text, filename):
    #Google Text-to-Speech
    from gtts import gTTS

    # Crie um objeto gTTS a partir do texto
    tts = gTTS(text, lang='pt-br')

    # Salve o áudio como um arquivo .flac
    return tts.save(f"{path}/{filename}.flac")

def play(path, filename):
    import soundfile as sf
    import sounddevice as sd

    # Carregue o arquivo flac
    data, samplerate = sf.read(f"{path}/{filename}.flac")

    # Reproduza o arquivo flac
    sd.play(data, samplerate)

    # Aguarde até que a reprodução seja concluída
    return sd.wait()

if __name__ == "__main__":
    # Defina o caminho absoluto para o novo diretório de trabalho
    path = "/tmp"

    # Mude para o novo diretório de trabalho
    os.chdir(path)

    credentials()

    recording(path, "recording")

    convert(path, "recording")

    pergunta = recognize(path, "recording")

    resposta = openai(pergunta)
    
    print(f"{pergunta}: {resposta}")

    speech(path, resposta, "resposta")

    play(path, "resposta")