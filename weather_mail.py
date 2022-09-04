# coding=UTF-8
import json
import smtplib
from email.mime.text import MIMEText
import string
import datetime
import requests
import re
from importlib import reload
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.image import MIMEImage
import bs4
from bs4 import BeautifulSoup
import time 
import random,sys
from charset_normalizer.cli import normalizer
# import charset-normalizer


reload(sys)
# sys.setdefaultencoding('utf8')
boy_name = '老公'
girl_name = '老婆'
province = 'hubei'   #省份,
city = 'wuhan'   #城市
special_day = '2021-03-17'  #纪念日
mailto_list=['2571577737@qq.com'] #发给哪个邮箱
# 2571577737
mail_host="smtp.qq.com"  #设置邮箱服务器
sender = "1505031156@qq.com"
# mail_user="北天"    #用户名
mail_user = ""
mail_pass="wgyaxsptruhahgij"   #密码 授权码
name = '老公'   #邮件发件人名称
mail_title = '给老婆的每日天气预报' #邮件名称

def get_day():
    d1 = datetime.datetime.strptime(special_day, '%Y-%m-%d')
    d2 = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')
    delta = d2 - d1
    return delta.days

def get_weathertip():
    url = "https://tianqi.moji.com/weather/china/%s/%s"%(province,city)
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text,'html.parser',from_encoding="utf-8")
    all_tertiaryconsumers = soup.find_all(class_='wea_tips clearfix')
    for tertiaryconsumer in all_tertiaryconsumers:
        return re.search('<em>(.+?)</em>',str(tertiaryconsumer)).group(1)

def get_chp():
    url = "https://api.shadiao.pro/chp"
    resp = requests.get(url)
    return resp.json()['data']['text']

def get_weather():
    url = "https://tianqi.moji.com/weather/china/%s/%s"%(province,city)
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text,"html.parser",from_encoding="utf-8")
    all_tertiaryconsumers = soup.find_all(class_='days clearfix') 
    html = ''
    for tertiaryconsumer in all_tertiaryconsumers:
        day = tertiaryconsumer.find(name='a').text
        url = re.search('src="(.+?)"',str(tertiaryconsumer)).group(1)
        weather = re.search('<img alt="(.+?)"',str(tertiaryconsumer)).group(1)
        temperature = re.search('(\w+° \/ \w+°)',str(tertiaryconsumer)).group(1)
        if 'level_1' in str(tertiaryconsumer):
            WindLevel = tertiaryconsumer.find(class_='level_1').text.strip()
            color = '#8fc31f'
        if 'level_2' in str(tertiaryconsumer):
            WindLevel = tertiaryconsumer.find(class_='level_2').text.strip()
            color = '#d7af0e'
        if 'level_3' in str(tertiaryconsumer):
            WindLevel = tertiaryconsumer.find(class_='level_3').text.strip()
            color = '#f39800'
        if 'level_4' in str(tertiaryconsumer):
            WindLevel = tertiaryconsumer.find(class_='level_4').text.strip()
            color = '#e2361a'
        if 'level_5' in str(tertiaryconsumer):
            WindLevel = tertiaryconsumer.find(class_='level_5').text.strip()
            color = '#5f52a0'
        if 'level_6' in str(tertiaryconsumer):
            WindLevel = tertiaryconsumer.find(class_='level_6').text.strip()
            color = '#631541'
        html += """<div style="display: flex;margin-top:5px;height: 30px;line-height: 30px;justify-content: space-around;align-items: center;">
        <span style="width:15%%; text-align:center;">%s</span>
        <div style="width:10%%; text-align:center;">
            <img style="height:26px;vertical-align:middle;" src='%s' alt="">
        </div>
        <span style="width:25%%; text-align:center;">%s</span>
        <div style="width:35%%; ">
            <span style="display:inline-block;padding:0 8px;line-height:25px;color:%s; border-radius:15px; text-align:center;">%s</span>
        </div>
        </div>
        """ % (day, url, temperature, color, WindLevel)
    return html

def get_image():  #加载图片
  url = "http://wufazhuce.com/"
  resp = requests.get(url)
  soup = BeautifulSoup(resp.text,'html.parser',from_encoding="utf-8")
  img_url = re.search('src="(.+?)"',str(soup.find(class_='fp-one-imagen'))).group(1)
  res = requests.get(img_url)
  # print(res.text)
  # return re.search('src="(.+?)"',str(soup.find(class_='fp-one-imagen'))).group(1)
  return res.content

def get_today():
    i = datetime.datetime.now()
    date = "%s/%s/%s" % (i.year, i.month, i.day)
    return date


mail_content = """<!DOCTYPE html>
<html>

<head>
    <title>
    </title>
    <meta name="viewport" content="width=device-width,minimum-scale=1.0,maximum-scale=1.0,user-scalable=no">
    <link rel='stylesheet' href='/stylesheets/style.css' />
    
</head>

<body style="margin:0;padding:0;">
    <div style="width:100%; margin: 40px auto;font-size:20px; color:#5f5e5e;text-align:center">
        <span>今天是我们在一起的第</span>
        <span style="font-size:24px;color:rgb(221, 73, 73)"  >{0}</span>
        <span>天</span>
    </div>
    <div style="width:100%; margin: 0 auto;color:#5f5e5e;text-align:center">
        <span style="display:block;color:#676767;font-size:20px">{1}</span>
        <span style="display:block;color:#676767;font-size:20px">{2}</span>
        <span style="display:block;margin-top:15px;color:#676767;font-size:15px">近期天气预报</span>

{3}
    </div>
    <div style="text-align:center;margin:35px 0;">
            <span style="display:block;margin-top:55px;color:#676767;font-size:15px">{4} ❤️ {5}</span>
            <span style="display:block;margin-top:25px;font-size:22px; color:#9d9d9d; ">{6}</span>
             <img src='cid:image1' style="width:100%;margin-top:10px;"  alt="">
    </div>
    

</body>

</html>""".format(str(get_day()),get_weathertip(),get_chp(),get_weather(),boy_name,girl_name,get_today())

def send_mail(to_list,sub,content):
    me=name+"<"+mail_user+">"
    msg = MIMEMultipart()
    msg.attach(MIMEText(content,'html', 'utf-8'))
    fp = get_image() #加载图片
    msgImage = MIMEImage(fp) #加载图片
    msgImage.add_header('Content-ID', '<image1>') #加载图片
    msg.attach(msgImage) #加载图片
    msg['Subject'] = Header(sub)
    msg['From'] = ",".join(sender)
    msg['To'] = ",".join(mailto_list)
    # print(msg.as_string())
    # exit(0)
    try:
        server = smtplib.SMTP("smtp.qq.com", 25)
        # server = smtplib.SMTP_SSL("smtp.qq.com")
        # server.connect(mail_host, 465)
        # server.connect(mail_host,465)
        server.login(sender,mail_pass)
        server.sendmail(sender, to_list, msg.as_string())
        server.close()
        return True
    except Exception as e:
        print(e)
        print(str(str(e.__traceback__.tb_lineno)))
        return False
    
    
if __name__ == '__main__':
    try:
        if send_mail(mailto_list,mail_title,mail_content):
            print("发送成功")
        else:
            print("发送失败")
    except Exception as e:
        print(e)
        print(str(e.__traceback__.tb_lineno))
    # print(get_image())
    # print(get_weather())
