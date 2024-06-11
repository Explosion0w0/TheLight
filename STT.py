import vosk
import pyaudio
import json
from pypinyin import lazy_pinyin
from threading import Thread
import os
import requests





class VoiceControl:

    def __init__(self, modelPath:str="", outputPath:str="recognized.txt") -> None:
        self.model = vosk.Model(modelPath)
        self.reconizer = vosk.KaldiRecognizer(self.model, 16000)
        self.pAudio = pyaudio.PyAudio()
        self.stream = self.pAudio.open(format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=8192)
        self.outputPath = outputPath

    def regulate(self, command:str) -> bool:
        #開燈
        if "kaideng" in command:
            rq = requests.get("http://127.0.0.1/open")
            if (rq.status_code == 200):
                print("\033[1;32;40mPi: open the light\033[0m")

        #關燈
        elif "guandeng" in command:
            rq = requests.get("http://127.0.0.1/close")
            if (rq.status_code == 200):
                print("\033[1;31;40mPi: close the light\033[0m")

        #日光
        elif "riguang" in command:
            rq = requests.get("http://127.0.0.1/enviroment")
            if (rq.status_code == 200):
                print("\033[1;33;40mPi: adjust the enviroment light\033[0m")

        #升高
        elif "shengao" in command:
            print("\033[1;36;40mPi: increase brightness\033[0m")

        #降低
        elif "jiangdi" in command:
            print("\033[1;34;40mPi: decrease brightness\033[0m")

        #離開
        elif "likai" in command:
            print("\033[1;35;40mPi: stop\033[0m")
            return False
        else:
            pass
        return True
    def startThread(self):
        thread = Thread(target=self.start)
        thread.start()
        


        
    def start(self) -> None:
        with open(self.outputPath, "w") as outputFile:
            print("Listening for speech. Say \"離開\" to stop.")
    # Start streaming and recognize speech
            try:
                keep = True
                while True:
                    data = self.stream.read(4096)#read in chunks of 4096 bytes
                    if self.reconizer.AcceptWaveform(data):#accept waveform of input voice
                # Parse the JSON result and get the recognized text
                        result = json.loads(self.reconizer.Result())
                        recognizedText = result["text"]

                # Write recognized text to the file
                        outputFile.write(recognizedText + "\n")
                        pinyin = "".join(lazy_pinyin(recognizedText)).replace(" ", "")
                        print("%s (%s)"%(recognizedText, pinyin))
                        keep = self.regulate(pinyin)

                # Check for the termination keyword
                    if not keep:
                        print("Termination keyword detected. Stopping...")
                        break
            except KeyboardInterrupt:
                self.stream.stop_stream()
                self.stream.close()
                self.pAudio.terminate()

            outputFile.close()
                


## Set the model path
#modelPath = "vosk-model-small-cn-0.22"
##model_path = "vosk-model-small-en-us-0.15"
## Initialize the model with model-path
#model = vosk.Model(modelPath)
#
## Create a recognizer
#reconizer = vosk.KaldiRecognizer(model, 16000)
#
## Open the microphone stream
#pAudio = pyaudio.PyAudio()
#stream = pAudio.open(format=pyaudio.paInt16,
#                channels=1,
#                rate=16000,
#                input=True,
#                frames_per_buffer=8192)
#
## Specify the path for the output text file
#outputPath = "recognized.txt"
#
#
#def regulate(command:str) -> bool:
#    #開燈
#    if "kaideng" in command:
#        print("\033[1;32;40mPi: open the light\033[0m")
#
#    #關燈
#    elif "guandeng" in command:
#        print("\033[1;31;40mPi: close the light\033[0m")
#
#    #日光
#    elif "riguang" in command:
#        print("\033[1;33;40mPi: adjust the enviroment light\033[0m")
#
#    #升高/身高
#    elif "shengao" in command:
#        print("\033[1;36;40mPi: increase brightness\033[0m")
#
#    #降低
#    elif "jiangdi" in command:
#        print("\033[1;34;40mPi: decrease brightness\033[0m")
#
#    #離開
#    elif "likai" in command:
#        print("\033[1;35;40mPi: stop\033[0m")
#        return False
#    
#    else:
#        pass
#
#    return True


if __name__ =="__main__":
    vc = VoiceControl("vosk-model-small-cn-0.22", "reconized.txt")
    vc.startThread()
    print("OK")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        os._exit(0)

