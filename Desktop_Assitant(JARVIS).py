import pyttsx3  # text-to-speech conversion library
import datetime
import speech_recognition as sr # use to recognise what you speak
import wikipedia # used to get about something from wikipedia
import webbrowser # Interfaces for launching and remotely controlling Web browsers
import os
import pywhatkit # to use whats app
# import pyautogui as pg
 
""" 
There are many TTS (Text-to-Speech) engine (used to set voices):
    1. sapi5 - SAPI5 on Windows
    2. nsss - NSSpeechSynthesizer on Mac OS X
    3. espeak - eSpeak on every other platform

Here I have used sapi5 which is a Microsoft Speech API (SAPI) 5.3, the native API for Windows
"""

engine = pyttsx3.init('sapi5')  # Object creation (if we don't mention sapi5, by default it will take sapi5 as tts engine)
voices = engine.getProperty('voices')  # to get details of current voices
# print(voices[0].id)
engine.setProperty('voice', voices[1].id)    # to set a voice (0 for male and 1 for female)

def speak(audio):
    '''
    speak what we give as input
    '''
    engine.say(audio)   # use to speak
    engine.runAndWait() # Runs an event loop until all commands queued up until this method call complete

def welcome(name):
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour <= 11:
        speak(f'Good Morning {name}')
    elif hour >= 12 and hour <= 16:
        speak(f'Good Afternoon {name}')
    else:
        speak(f'Good Evening {name}')
    
    speak('I am Jarvis, How may I help you')

def hearWhatIHaveSaid():
    '''
    It take input through microphone given by user and return display it as string
    '''
    
    r = sr.Recognizer()
    with sr.Microphone() as source:   # open the microphone and start recording
        print('Listening...')
        r.pause_threshold = 1   # time to wait (in seconds) to consider that the phrase is completed. Here it is on second
        r.energy_threshold = 3000   # how much loud we need to speak (this can also help if there is any background noise)
        # ----------- Below are some a to customize 
        # r.energy_threshold = 300  # minimum audio energy to consider for recording (i.e., how much loud we need to speak)
        # r.dynamic_energy_threshold = True
        # r.dynamic_energy_adjustment_damping = 0.15
        # r.dynamic_energy_ratio = 1.5
        # r.pause_threshold = 0.8  # seconds of non-speaking audio before a phrase is considered complete
        # r.operation_timeout = None  # seconds after an internal operation (e.g., an API request) starts before it times out, or ``None`` for no timeout
        # r.phrase_threshold = 0.3  # minimum seconds of speaking audio before we consider the speaking audio a phrase - values below this are ignored (for filtering out clicks and pops)
        # r.non_speaking_duration = 0.5  # seconds of non-speaking audio to keep on both sides of the recording
        audio = r.listen(source)    # This is used to listen the audio

    try:
        print('Recognizing what you spoke...')
        query = r.recognize_google(audio, language = 'en-in')    # Performs speech recognition on ``audio_data`` using the Google Speech Recognition API (language en-in means english india)
        print(f'You said: {query}\n')

    except Exception as e:
        print(e,'\nI am unable to recognize what you are saying. Please repeat it again..')
        speak('I am unable to recognize what you are saying. Please repeat it again')
        return "NONE"
    return query

if __name__ == '__main__':
    # speak('this is nice')
    
    welcome('Suchir')
    while 1:
        print('1. Search for someone in wikipedia ("name" wikipedia')
        print('2. Open Youtube, whatsapp')
        print('3. Play Songs')
        print('4. What is the time')
        print('5. Send a Message on Whatsapp')
        print('6. Bye')
        ask = hearWhatIHaveSaid().lower()
        
        if 1: # ask[:6].lower() == 'jarvis'
            
            if 'wikipedia' in ask:
                speak(f'Searching Wikipedia for {ask[:-9]}')
                ask = ask.replace('wikipedia', '')
                result = wikipedia.summary(ask, sentences = 2)
                # speak()
                print(result)
                speak(f'According to Wikipedia {result}')
            
            elif 'bye' in ask:
                speak('I am sorry to see you go. Bye Bye')
                break
            
            elif 'open youtube' in ask:
                webbrowser.open('youtube.com')
                speak(f'Opening {ask[-7:]}')
            
            elif 'play songs' in ask:
                song_dir_path = 'C:\\Users\\Suchir\\Desktop\\music'
                songs = os.listdir(song_dir_path)   # listdir will list all the songs in the directory given
                print(songs, len(songs))
                # here random module can be used to play random songs
                os.startfile(os.path.join(song_dir_path, songs[0])) # used to start any file
            
            elif 'what is the time' in ask:
                hour = datetime.datetime.now().hour
                minute = datetime.datetime.now().minute
                speak(f'{hour} {minute}')
            
            elif 'open whatsapp' in ask:
                path = 'C:\\Users\\Suchir\\AppData\\Local\\WhatsApp\\WhatsApp.exe'
                speak(f'Opening {ask[-8:]}')
                os.startfile(path)
                    
            elif 'send a message on whatsapp' in ask:
                phone = {'didi': '12345', 'saswat': '67890'}
                while 1:
                    print('What is you message')
                    speak('What is you message')
                    message = 'none'
                    message = hearWhatIHaveSaid().lower()
                    if message != 'none':
                        break
                while 1:
                    print('Please confirm your message (if correct say yes)')
                    print(message)
                    speak('Please confirm your message')
                    confirm = hearWhatIHaveSaid().lower()
                    if confirm.lower() == 'yes':
                        break
                while 1:
                    speak('who do you want to message')
                    name = 'none'
                    name = hearWhatIHaveSaid().lower()
                    if name != 'none':
                        break
                while 1:
                    print('confirm the sender name (if correct say yes)')
                    print(name)
                    speak('confirm the sender name')
                    confirm = hearWhatIHaveSaid().lower()
                    if confirm.lower() == 'yes':
                        pywhatkit.start_server()
                        pywhatkit.sendwhatmsg_instantly(phone.get(name), message, 20, 22)
                        # pg.press("enter")
                        speak('Message sent')
                        break

        # elif ask[:6].lower() != 'jarvis' and ask != 'none':
        #     print("I don't know whom you are asking")
        #     speak("I don't know whom you are asking")
            
            
        










'''
REFERENCES
==========

1. For pyttsx3:
    - https://pyttsx3.readthedocs.io/en/latest/engine.html
    - https://pypi.org/project/pyttsx3/

2. For SpeechRecognition:
    - https://github.com/Uberi/speech_recognition/blob/master/reference/library-reference.rst
    - https://www.geeksforgeeks.org/speech-recognition-in-python-using-google-speech-api/
    - https://pypi.org/project/SpeechRecognition/
    
3. For wikipedia:
    - https://www.geeksforgeeks.org/wikipedia-module-in-python/

4. For webbrowser:
    - https://www.geeksforgeeks.org/python-launch-a-web-browser-using-webbrowser-module/

5. For pywhatkit:
    - https://pypi.org/project/pywhatkit/
    

'''
'''
Got idea from here:
    - https://pythonspot.com/personal-assistant-jarvis-in-python/
'''