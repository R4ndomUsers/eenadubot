from PIL import Image
import os
import json
import img2pdf
import requests
import time
import threading
import os
from datetime import datetime
import pytz

bg1 = []
over1 = []
com = []
co = 0
total = 0
quality = 85
# for the fixed connection purpose
headers = {
    'Host': 'epaper.eenadu.net',
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/javascript, /; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'Content-Type': 'application/json; charset=utf-8',
    'Referer': 'https://epaper.eenadu.net/Home/Index',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9'
}

# for giving warning for invalid entry


def warn():
    print('invalid entry')
    exit(0)

# m=2 for disricts and m=3 for town edition ::-
# getting the districts list in state or towns in districts


def get_regions(m, n):
    with requests.Session() as s:
        regions = s.get('https://epaper.eenadu.net/Home/GetEditionListById?type=' +
                        str(m)+'&EditionId='+str(n), headers=headers)
        regions = regions.json()
    divisions = {}
    for i in regions[0]:
        divisions[i['EditionDisplayName']] = i['EditionId']
    return divisions

# getting the background image and the front image ::-
# mixing the two images and overlap one another


def get_network(path):
    print('connecting to internet .....')
    url1 = 'https://intra-b0805.firebaseio.com/'+path+'/.json'
    if path == '':
        url1 = 'https://intra-b0805.firebaseio.com/.json'
    auth_key = '8nqwhzUcjQbFfhnyb3TXbdi5EVg6ehvAR90TFuQr'
    try:
        r1 = requests.get(url1 + '?auth=' + auth_key)
        return r1.json()
    except Exception as e:
        print('no internet')
        return 0


header1 = {'Referer': 'https://epaper.eenadu.net/Home/Index', 'Sec-Fetch-Mode': 'no-cors',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}


def load_bg(url, no):
    global co, total
    img_data = requests.get(url, headers=header1).content
    with open('bg'+str(no)+'.jpg', 'wb') as handler:
        handler.write(img_data)
    bg1[no] = False
    co += 1
    if ((co/total) == 1):
        print(' ', '■'*int((co/total)*50), '  ', str(int((co/total)*100))+'%')
    else:
        print(' ', '■'*int((co/total)*50), '  ',
              str(int((co/total)*100))+'%', end='\r')


def load_over(url, no):
    global co, total
    url = url[:-3]+'png'
    img_data = requests.get(url, headers=header1).content
    with open('over'+str(no)+'.png', 'wb') as handler:
        handler.write(img_data)
    over1[no] = False
    co += 1
    if ((co/total) == 1):
        print(' ', '■'*int((co/total)*50), '  ', str(int((co/total)*100))+'%')
    else:
        print(' ', '■'*int((co/total)*50), '  ',
              str(int((co/total)*100))+'%', end='\r')


def load_page(url, no):
    global quality
    page = str(no)+'.jpeg'
    k1 = threading.Thread(target=load_bg, args=(url, no))
    k1.start()
    k2 = threading.Thread(target=load_over, args=(url, no))
    k2.start()
    while (bg1[no] | over1[no]):
        pass
    img = Image.open('over'+str(no)+'.png').convert("RGBA")
    background = Image.open('bg'+str(no)+'.jpg')
    background.paste(img, (0, 0), img)
    background.save(page, 'jpeg', optimize=True, quality=quality)
    os.remove('bg'+str(no)+'.jpg')
    os.remove('over'+str(no)+'.png')
    com[no] = 0
# get all the desired papers


def get_paper(d, m, y, n, z, edition_name, folder):
    global total
    tz = pytz.timezone('Asia/Kolkata')
    now = datetime.now(tz)
    date = now.strftime("%d-%m-%Y")
    with requests.Session() as s:
        r = s.get('https://epaper.eenadu.net/Home/GetAllpages?editionid=' +
                  str(n)+'&editiondate='+d+'%2F'+m+'%2F'+y, headers=headers)
        k = r.json()
    j = []
    for i in k:
        j.append(i['XHighResolution'])
    if (z != 0):
        with requests.Session() as s:
            r = s.get('https://epaper.eenadu.net/Home/GetAllpages?editionid=' +
                      str(z)+'&editiondate='+d+'%2F'+m+'%2F'+y, headers=headers)
            k = r.json()
        for i in k:
            j.append(i['XHighResolution'])
    print('geting all the pages')
    total = len(j)*2
    for i in range(len(j)):
        over1.append(True)
        bg1.append(True)
        com.append(1)
        k = threading.Thread(target=load_page, args=(j[i], i))
        k.start()
    while (sum(com) != 0):
        pass
    l = []
    for i in range(len(j)):
        l.append(str(i)+'.jpeg')
    try:
        os.mkdir(folder)
    except Exception:
        pass
    with open(folder+"/"+f'{edition_name} {date}'+".pdf", "wb") as f:
        f.write(img2pdf.convert(l))
    for i in l:
        os.remove(i)


# for the date dicision

# date=input('enter todays date (in format dd-mm-yyyy) or press 1 to continue with todays date :-\t')
date = '1'
if (date == '1'):
    tz = pytz.timezone('Asia/Kolkata')
    now = datetime.now(tz)
    dt = now.strftime("%d-%m-%Y").split('-')

else:
    try:
        dt = date.split('-')
    except Exception:
        warn()

# for selecting the state or main_region


l = {'TS': 1, 'AP': 2, 'hyd': 3}
# print('enter the quality you want')
quality = int(80)
# print(':-\n\t1. Main Papers\n\t2. District papers-AP\n\t3. District papers-TS\n\t4. Sunday Magzine')
ch = int(3)
if (ch == 1):
    state = 'hyd'
    try:
        get_paper(dt[0], dt[1], dt[2], l[state], 0, state, 'main')
        print('your pdf is saved as '+state+'.pdf')
    except Exception as e:
        print(str(e))
        print('paper not found')
    state = 'AP'
    try:
        bg1 = []
        over1 = []
        com = []
        co = 0
        total = 0
        get_paper(dt[0], dt[1], dt[2], l[state], 0, state, 'main')
        print('your pdf is saved as '+state+'.pdf')
    except Exception:
        print('paper not found')
    state = 'TS'
    try:
        bg1 = []
        over1 = []
        com = []
        co = 0
        total = 0
        get_paper(dt[0], dt[1], dt[2], l[state], 0, state, 'main')
        print('your pdf is saved as '+state+'.pdf')
    except Exception:
        print('paper not found')
if (ch == 2):
    state = 'AP'
    dr = get_regions(2, l[state])
    dr1 = list(dr.keys())
    for i in range(len(dr)):
        bg1 = []
        over1 = []
        com = []
        co = 0
        total = 0
        print(i+1, dr1[i])
        an = i+1
        try:
            q = dr1[an-1].split(' ')
            try:
                q = q[0]+'_'+q[1]
            except Exception:
                q = q[0]
            print(q)
            get_paper(dt[0], dt[1], dt[2], dr[dr1[an-1]], 0, q, 'apdist')
            print('your pdf is saved as eenadu_'+dr1[an-1]+'.pdf')
        except Exception:
            print('paper not found')
if (ch == 3):
    state = 'TS'
    dr = get_regions(2, l[state])
    dr1 = list(dr.keys())
    for i in range(len(dr)):
        bg1 = []
        over1 = []
        com = []
        co = 0
        total = 0
        print(i+1, dr1[i])
        an = i+1
        try:
            q = dr1[an-1].split(' ')
            try:
                q = q[0]+'_'+q[1]
            except Exception:
                q = q[0]
            # print(q)
            get_paper(dt[0], dt[1], dt[2], dr[dr1[an-1]], 0, q, 'tsdist')
            print('your pdf is saved as eenadu_'+dr1[an-1]+'.pdf')
        except Exception:
            print('paper not found')
elif (ch == 4):
    try:
        bg1 = []
        over1 = []
        com = []
        co = 0
        total = 0
        get_paper(dt[0], dt[1], dt[2], 367, 0, 'sunday', 'sunday')
        print('your pdf is saved as eenadu_sunday.pdf')
    except Exception as e:
        print(str(e))
        print('paper not found')

'''
# 35.4s
# 50.9s
'''
