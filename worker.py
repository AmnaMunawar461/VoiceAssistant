from openai import OpenAI
import requests

openai_client = OpenAI()


def speech_to_text(audio_binary):
    base_url = 'https://sn-watson-stt.labs.skills.network'
    api_url = base_url+'/speech-to-text/api/v1/recognize'
    params = {
        'model': 'en-US_Multimedia',
    }
    body = audio_binary
    response = requests.post(api_url, params=params, data=audio_binary).json()
    text = 'null'
    while bool(response.get('results')):
        print('speech to text response:', response)
        text = response.get('results').pop().get('alternatives').pop().get('transcript')
        print('recognized text ', text)
        return text
    


def text_to_speech(text, voice=""):
    base_url = 'https://sn-watson-tts.labs.skills.network'
    api_url = base_url + '/text-to-speech/api/v1/synthesize?output=output_text.wav'
    if voice != "" and voice != "default":
        api_url += "&voice=" + voice
    
    headers = {
        'Accept': 'audio/wav',
        'Content-Type': 'application/json',
    }

    # Set the body of our HTTP request
    json_data = {
        'text': text,
    }
    response = requests.post(api_url, headers=headers, json=json_data)
    print('text to speech response:', response)
    return response.content


def openai_process_message(user_message):
    prompt = "Act like a personal assistant. You can respond to questions, translate sentences, summarize news, and give recommendations."
    open_ai_response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role":"system","content":prompt},
            {"role":"user","content":user_message}
        ],
        max_tokens=4000
    )
    print("openai response:", open_ai_response)
    return open_ai_response.choices[0].message.content

