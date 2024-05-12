import os
from flask import Flask, render_template, request, jsonify
from safetensors import torch
from spacy.tests import tokenizer
from werkzeug.utils import secure_filename
from moviepy.editor import VideoFileClip

from src.download import download_audio_from_url

from src.transcribe import transcribe_audio
# Set page title
from src.summarize import summarize_transcript
from transformers import AutoModelForCausalLM, AutoTokenizer
# import torch
# Importing the required library (ollama)
import ollama

# Initializing an empty list for storing the chat messages and setting up the initial system message
chat_messages = []
system_message = 'You are a helpful assistant.'



# tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
# model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")


app = Flask(__name__)

@app.route("/")
def index():
    return render_template('chat.html')




@app.route('/upload',methods=["GET", "POST"])
def upload():
    print(request.form)
    input=request.form['text']
    print("ggg",input)
    print(request.files)
    fle = request.files['fileInput']
    video_file_path = secure_filename(fle.filename)
    if "http" in input:
        print("httttttttpppppppppppp")
        audio_file, length = download_audio_from_url(input)
        transcript = transcribe_audio(audio_file)
        with open("transcript.txt", "w") as f:
            f.write(transcript)
        summary = summarize_transcript("transcript.txt")
        print(summary)
        return summary
    elif len(video_file_path)!=0:
        fle=request.files['fileInput']
        video_file_path=secure_filename(fle.filename)
        fle.save(video_file_path)
        audio_file_path = 'audio.mp3'
        extract_audio(video_file_path, audio_file_path)
        transcript = transcribe_audio(audio_file_path)
        with open("transcript.txt", "w") as f:
            f.write(transcript)
        summary = summarize_transcript("transcript.txt")
        print(summary)
        return summary
    else:
        ans=ask(input)
        return ans


def extract_audio(video_file_path, audio_file_path):
    video_clip = VideoFileClip(video_file_path)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(audio_file_path)
    audio_clip.close()
    video_clip.close()
def ask(message):
    chat_messages.append(
        create_message(message, 'user')
    )
    print("\n\n--{message}--\n\n")
    return chat()  # Return the response


def create_message(message, role):
    return {
        'role': role,
        'content': message
    }
def chat():
    # Calling the ollama API to get the assistant response
    ollama_response = ollama.chat(model='mistral', stream=True, messages=chat_messages)

    # Preparing the assistant message by concatenating all received chunks from the API
    assistant_message = ''

    for chunk in ollama_response:
        assistant_message += chunk['message']['content']
        print(chunk['message']['content'], end='', flush=True)

    # Adding the finalized assistant message to the chat log
    chat_messages.append(create_message(assistant_message, 'assistant'))

    # Return the assistant message
    return assistant_message


# def get_Chat_response(text):
#
#     # Let's chat for 5 lines
#     for step in range(5):
#         # encode the new user input, add the eos_token and return a tensor in Pytorch
#         new_user_input_ids = tokenizer.encode(str(text) + tokenizer.eos_token, return_tensors='pt')
#
#         # append the new user input tokens to the chat history
#         bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if step > 0 else new_user_input_ids
#
#         # generated a response while limiting the total chat history to 1000 tokens,
#         chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
#
#         # pretty print last ouput tokens from bot
#         return tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)



if __name__=='__main__':
    app.run()