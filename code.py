import io
import os
import six
from google.cloud import vision 
from google.cloud import translate
from google.cloud.vision import types
import json

client = vision.ImageAnnotatorClient()

file_name = os.path.join(os.path.dirname(__file__),'PHTO/Capture100.png')
# file_name = 'PHTO/Capture3.png'
with io.open(file_name,'rb') as image_file:
     content = image_file.read()
	 
image = types.Image(content= content)

image_context = vision.types.ImageContext(
        language_hints=['hi'])
		
		
response = client.document_text_detection(image=image)
texts = response.text_annotations

def translate_text(target, text):
    
    translate_client = translate.Client()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    result = translate_client.translate(text, target_language=target)

    
    print(u'Translation: {}'.format(result['translatedText']))
    print(u'Detected source language: {}'.format(
        result['detectedSourceLanguage']))
		
target = 'en'
translate_text(target,texts[4].description)