import pandas as pd
import re
from urllib.request import urlretrieve 
station = pd.read_excel('polling_station.xlsx')

link = 'http://ceoharyana.nic.in/docs/election/finalroll2018/'
link_part = 'CMB68/CMB0680139.PDF'

num = re.findall(r'\d+',station.AC[1])

for x in range(1,2):
    num = re.findall(r'\d+',station.AC[x])
    first_part = 'CMB' + num[0]
    for p in range(1,5):
        sec_part = 'CMB'+ str(num[0]).zfill(3) + str(p).zfill(4)
        path = first_part + '_' + sec_part +'.pdf'
        url = link + first_part + '/' + sec_part +'.PDF'
        download_file(url,path)
        print(url)
   
def download_file(download_url,path):
    print(path)
    urlretrieve(download_url,path)
