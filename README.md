# alexa-openai ( English )
This is a Alexa-OpenAI for text-to-speech and speech-to-text conversion. It uses libraries such as pyaudio, wave, numpy, json, os, ffmpeg, google-cloud-speech, and openai.

- Record audio using pyaudio
- Save the audio as a wave file
- Convert the wave file to FLAC using ffmpeg
- Send the FLAC file to Google Cloud Speech for recognition
- Send the recognized text to OpenAI's completion API for answering
- Convert the answer text to speech using Google Text-to-Speech
- Save the speech as an FLAC file.

##In order to use the script, the user needs to have API keys for OpenAI and Google Cloud.

##The user also needs to install the necessary libraries and have access to the Google Cloud Speech API.

<code>pip3 install --upgrade google-cloud-speech pyaudio ffmpeg-python gTTS soundfile sounddevice numpy PyYAML</code>

# alexa-openai ( Português Brasil )
Este código é uma implementação de um sistema de reconhecimento de fala e resposta por meio de inteligência artificial. Ele usa as bibliotecas pyaudio, wave, struct, numpy, os, json, ffmpeg, io, google.cloud, e openai.

Ele começa carregando as credenciais de sua conta OpenAI e Google Cloud. Em seguida, ele possibilita a gravação de um arquivo de áudio com duração de 5 segundos, usando a biblioteca pyaudio. O arquivo gravado é convertido para o formato .flac, usando a biblioteca ffmpeg. O áudio convertido é então enviado para o Google Cloud para reconhecimento de fala, e a transcrição resultante é enviada para a API OpenAI para geração de uma resposta. Por fim, a resposta é convertida em áudio pela biblioteca gTTS do Google Text-to-Speech.