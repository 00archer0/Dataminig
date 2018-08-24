import pandas as pd
import re
import urllib
import requests
from urllib.request import urlretrieve 
from wand.image import Image
import io
import os
import six
from google.cloud import vision 
from google.cloud import translate
from google.cloud.vision import types
import json

client = vision.ImageAnnotatorClient()
target = 'en'
final = ''
counter = []
station = pd.read_excel('polling_station.xlsx')


link = 'http://ceoharyana.nic.in/docs/election/finalroll2018/'
link_part = 'CMB02/CMB0020022.PDF'
url = link+link_part 
item = [(3400,300,3800,500),(450,1970,2480,3850),(870,4070,2700,4300),(870,4330,2700,4500),
        (3100,2900,3800,3050),(3120,3780,3800,3860),(1300,4980,2000,5250)]


def get_pic(sample_pdf,area):
    img = sample_pdf.clone()
    img.crop(*area)
    return img.make_blob('JPEG')

for x in range(1,21):
    num = re.findall(r'\d+',station.AC[x])
    first_part = 'CMB' + num[0]
    print('here')
    final = ''
    for p in range(1,station['polling_station'][x])+1:                
        print(str(p) +' next here')
        sec_part = 'CMB'+ str(num[0]).zfill(3) + str(p).zfill(4)
        path = first_part + '_' + sec_part +'.pdf'
        url = link + first_part + '/' + sec_part +'.PDF'
        fetched_item = ''

        sample_pdf = Image(filename=path+"[0]", resolution=500)
        for t in item:
            print(t)
            content = get_pic(sample_pdf,t)
            image = types.Image(content= content)
            image_context = vision.types.ImageContext(language_hints=['hi'])    
            response = client.document_text_detection(image=image)
            texts = response.text_annotations
            texts = texts[0].description.replace('\n',' ')
            fetched_item = fetched_item+texts+' ~ '
            print(fetched_item)
        
        final = final+fetched_item+'\n'
        '''final.append(str(fetched_item))
                                print(final)
                            to_save = pd.DataFrame(final)
                            to_save.to_csv('fin.csv',index=False,encoding='utf-8',header=False)   
                                        '''
    with open(station['AC'][x]+'.txt','w+',encoding='utf-8') as file:
            file.write(final)    



print(counter.count(1))
print('here')