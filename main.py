import io
import requests
import urllib
import json
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont

with open('config.json') as config:
    r = requests.get('https://na.finalfantasyxiv.com/lodestone/character/' + json.load(config)['character_id'])

soup = BeautifulSoup(r.text, 'lxml')

text_offset = [(77, 64), (77, 104), (77, 142),
            (180, 64), (180, 104), (180, 142),
            (282, 64), (282, 104), (282, 142), (282, 182),
            (385, 64), (385, 104),
            (490, 64), (490, 104), (490, 142),

            (77, 292), (77, 331), (77, 370), (77, 409),
            (180, 292), (180, 331), (180, 370), (180, 409),
            (282, 292), (282, 331), (282, 370)]

job_icon_offset = [(51, 64), (51, 103), (51, 142),
                (256, 64), (256, 103), (256, 142), (256, 181),
                (153, 64), (153, 103), (153, 142),
                (358, 64), (358, 103),
                (461, 64), (461, 103), (461, 142)]

job_names = soup.find_all(class_ = 'character__job__name')
levels = soup.find_all(class_ = 'character__job__level')
exps = soup.find_all(class_ = 'character__job__exp')

job_icons = soup.find_all(class_ = 'character__job__icon')

chara_img = Image.open(io.BytesIO(urllib.request.urlopen(soup.find(class_ = 'character__detail__image').select('a')[0].get('href')).read()))
chara_img = chara_img.resize((334, 455))

img = Image.open('image.png')
draw = ImageDraw.Draw(img)
font = ImageFont.truetype('Quicksand-Regular.ttf', 15)
draw.text( (300, 464), u'FINAL FANTASY XIV © 2010 - 2018 SQUARE ENIX CO., LTD. All Rights Reserved.', fill=(255, 255, 255), font=ImageFont.truetype('font.ttf', 10))

img.paste(chara_img, (680, 25))

for i in range(0, len(job_icon_offset)):
    job_icon = Image.open(io.BytesIO(urllib.request.urlopen(job_icons[i].select('img')[0].get('src')).read()))
    job_icon = job_icon.convert('RGBA')
    job_icon = job_icon.resize((24, 24))
    img.paste(job_icon, job_icon_offset[i], job_icon)

for i in range(0, len(text_offset)):
    n, m = exps[i].getText().split(' / ')
    try:
        p = '{:.2f}%'.format(int(n) / int(m) * 100)
    except:
        p = '-'
    
    draw.text(text_offset[i], levels[i].getText() + '  ' + p, fill=(255, 255, 255), font=font)

img.save('image_gen.png')
