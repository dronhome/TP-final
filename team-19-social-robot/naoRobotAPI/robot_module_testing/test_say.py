# -*- coding: utf-8 -*-
from gtts import gTTS
import os
import time

def speak_or_message(sentence, is_physical=False):
    if is_physical:
        print(sentence)  # You can replace this with robot logic
    else:
        tts = gTTS(text=sentence, lang='cs', slow=True)
      
        tts.save("output.mp3")
       
        os.system("mpg123 output.mp3")

# Example usage
end_msg1 = u'Ďakujeme za spoluprácu'
end_msg2 = u'budeme sa ťešiť aj na budúce.'

message = u'Prosím, o trošku posunťe choďidla od seba'
speak_or_message(message, is_physical=False)
print("Koniec")
