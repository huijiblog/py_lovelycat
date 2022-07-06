# -*- coding:utf-8 -*-
from flask import Flask,request,send_file,jsonify
import requests
from PIL import Image,ImageDraw,ImageFont
import time
import os
import random
import datetime
from catAPI import *
import socket
from zhdate import ZhDate as lunar_date
import re

################################
########## By:  灰机 ###########
######## www.huiji888.cn #######
################################


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
ip_address = socket.getfqdn(socket.gethostname())
Local_Addr = socket.gethostbyname(ip_address)

# 放置下载文件的路径
app.config['DOWNLOAD_FOLDER'] = os.path.join(basedir, 'user_img')

@app.route('/',methods=['GET'])
def index():
    return "<h2>这是一个API测试站</h2>"

@app.route('/user_img/<filename>',methods=['GET','POST'])
def download_file (filename):
    folder = app.config['DOWNLOAD_FOLDER']
    # 构造供下载文件的完整路径
    path = os.path.join(folder, filename)
    return send_file(path, as_attachment=True)

@app.route('/api',methods=['POST', 'GET'])
def msgApi():
    if request.method == 'POST':
        wx_type = request.form.get("type")  # 数据类型
        msg = request.form.get("msg")  # 发送内容
        to_wxid = request.form.get("from_wxid")  # 1级来源id（比如发消息的人的id）
        from_name = request.form.get("from_name")  # 1级来源昵称（比如发消息的人昵称）
        final_from_wxid = request.form.get("final_from_wxid")  # 2级来源id（群消息事件下，1级来源为群id，2级来源为发消息的成员id，私聊事件下都一样）
        final_nickname = request.form.get("final_from_name")  # 2级来源昵称
        robot_wxid = request.form.get("robot_wxid")  # 当前登录的账号（机器人）标识id
        parameters = request.form.get("parameters")  # 附加参数（暂未用到，请忽略）
        ws_time = request.form.get("time")  # 请求时间(时间戳10位版本)
        try:
            file_url = request.form.get("file_url")  # 如果是文件消息（图片、语音、视频、动态表情），这里则是可直接访问的网络地址，非文件消息时为空
        except:
            raise TypeError("请使用 http-api 2.4+以上的版本")

        if wx_type == "100":  # 私聊消息
            if "查询QQ#" in msg:
                uChaGroup = msg.split('#')
                # 判断字符串是否为只由数字组成
                if uChaGroup[1].isdigit():
                    Q_To_Phone(uChaGroup[1], robot_wxid, to_wxid)
                else:
                    send_text_msg(robot_wxid, to_wxid, "ERROR COMMAND！")
            elif msg == "摸鱼":
                gettime = new_moyu(from_name)
                time.sleep(random.randint(1,5))
                pic_path =  basedir + '\\user_img\\' + gettime + '.png'
                send_image_msg(robot_wxid, to_wxid, pic_path)
            else:
                pass
                #send_text_msg(robot_wxid, to_wxid, "hello")

        elif wx_type == "200":  # 群聊消息
            if msg == "摸鱼":
                gettime = new_moyu(final_nickname)
                time.sleep(random.randint(1,5))
                pic_path =  basedir + '\\user_img\\' + gettime + '.png'
                send_image_msg(robot_wxid, to_wxid, pic_path)
            elif "查ip#" in msg:
                uChaGroup = msg.split('#')
                p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
                if p.match(uChaGroup[1]):
                    cx_ip(uChaGroup[1], robot_wxid, to_wxid)
                else:
                    send_text_msg(robot_wxid, to_wxid, "请填写正确的IP地址！")
            elif "搜斗图#" in msg:
                uChaGroup = msg.split('#')
                cx_doutu(uChaGroup[1], robot_wxid, to_wxid)
            elif "去水印#" in msg:
                uChaGroup = msg.split('#')
                douyin_videoJX(uChaGroup[1], "video", robot_wxid, to_wxid)
            elif "取音乐#" in msg:
                uChaGroup = msg.split('#')
                douyin_videoJX(uChaGroup[1], "music", robot_wxid, to_wxid)
            else:
                pass
                # send_group_at_msg(robot_wxid, to_wxid, final_from_wxid, final_nickname, "Hello！请加我私聊")
        else:
            pass
    else:
        return f"GET访问测试页面，本机地址 http://{Local_Addr}"  # 此处的测试地址应该是http://localhost:8074/复制到可爱猫功能-》HTTP多语言对-》消息回调地址
    return jsonify({"code": 200, "data": "result ok"})

# 摸鱼小助手功能
def new_moyu(from_uname):
    # 创建一个新的Image对象
    bgimg = Image.new(mode='RGB', size=(480, 800), color="#FFFFFF")
    choice = random.randint(1, 51)
    isGetFish = False
    if choice % 2 == 0:
        files = os.listdir("./picture")
        # print(files)
        fishImgName = random.choice(files)
        fish_img = Image.open("./picture/" + fishImgName)
        fish_img = fish_img.resize((480, 280))
        ################title##################
        # 创建 ImageDraw 对象 , 标题
        title_bgimg = ImageDraw.Draw(fish_img)
        # 以左上角为原点，绘制矩形。元组坐标序列表示矩形的位置、大小；fill设置填充色为红色，outline设置边框线为黑色
        title_bgimg.rectangle((163, 232, 318, 272), fill=(255, 127, 107), outline=(255, 127, 107))
        # 加载计算机本地字体文件
        font = ImageFont.truetype('msyh.ttc', size=18)
        # 在原图像上添加文本
        title_bgimg.text(xy=(178, 240), text='提醒摸鱼小助手', fill=(255, 255, 255), font=font)
        #################END####################
        isGetFish = True
        Image.Image.paste(bgimg, fish_img, (0, 0))
    else:
        ################title##################
        # 创建 ImageDraw 对象 , 标题
        title_bgimg = ImageDraw.Draw(bgimg)
        # 以左上角为原点，绘制矩形。元组坐标序列表示矩形的位置、大小；fill设置填充色为红色，outline设置边框线为黑色
        title_bgimg.rectangle((163, 232, 318, 272), fill=(255, 127, 107), outline=(255, 127, 107))
        # 加载计算机本地字体文件
        font = ImageFont.truetype('msyh.ttc', size=18)
        # 在原图像上添加文本
        title_bgimg.text(xy=(178, 240), text='提醒摸鱼小助手', fill=(255, 255, 255), font=font)
        #################END####################
        isGetFish = False

    template = Image.open('template.jpg')
    Alltext = ImageDraw.Draw(template)
    font1 = ImageFont.truetype('msyh.ttc', size=16)
    # 是否摸到鱼
    if isGetFish:
        # 一个中文 占16px空隙。一个符号占12px
        Alltext.text(xy=(49, 20), text=from_uname, fill=(70, 81, 232), font=font1)
        Alltext.text(xy=(49 + 16 + 16 + 16 + 16 + 12, 20), text='摸到了一条', fill=(0, 0, 0), font=font1)
        fishName = fishImgName.rstrip('.jpg')
        Alltext.text(xy=(49 + 16 + 16 + 16 + 16 + 12 + 80, 20), text=fishName, fill=(203, 2, 25), font=font1)
    else:
        Alltext.text(xy=(49, 20), text=from_uname, fill=(70, 81, 232), font=font1)
        Alltext.text(xy=(49 + 16 + 16 + 16 + 16 + 12, 20), text='本次未摸到鱼', fill=(0, 0, 0), font=font1)

    # 时间
    nowDate = datetime.datetime.now()
    theDate = nowDate.strftime('%m月%d日')
    weekDict = {'0': '周日', '1': '周一', '2': '周二', '3': '周三', '4': '周四', '5': '周五', '6': '周六'}
    weekCN = weekDict[nowDate.strftime('%w')]
    today0H = nowDate.replace(hour=0, minute=0, second=0, microsecond=0)
    today6H = nowDate.replace(hour=6, minute=0, second=0, microsecond=0)
    today11H = nowDate.replace(hour=11, minute=0, second=0, microsecond=0)
    today13H = nowDate.replace(hour=13, minute=0, second=0, microsecond=0)
    today18H = nowDate.replace(hour=18, minute=0, second=0, microsecond=0)
    today20H = nowDate.replace(hour=20, minute=0, second=0, microsecond=0)
    moment = ''
    if (nowDate >= today0H) and nowDate < today6H:
        moment = "凌晨"
    elif (nowDate >= today6H) and nowDate < today11H:
        moment = "上午"
    elif (nowDate >= today11H) and nowDate < today13H:
        moment = "中午"
    elif (nowDate >= today13H) and nowDate < today18H:
        moment = "下午"
    elif (nowDate >= today18H) and nowDate < today20H:
        moment = "傍晚"
    elif nowDate >= today20H:
        moment = "晚上"

    Alltext.text(xy=(179, 119), text=theDate + weekCN + moment, fill=(0, 237, 0), font=font1)

    # 下班
    dictTime = {}
    timeTotolSec = (today18H - nowDate).seconds
    if timeTotolSec > 0 and timeTotolSec < 60:
        dictTime['hours'] = 0
        dictTime['minutes'] = 0
    else:
        timeMin = timeTotolSec // 60
        if ((timeMin / 60) >= 1) and ((timeMin % 60) != 0):
            dictTime['hours'] = timeMin // 60
            dictTime['minutes'] = timeMin % 60
        else:
            dictTime['hours'] = 0
            dictTime['minutes'] = timeMin
    ### 小时
    font2 = ImageFont.truetype('digital-7-mono-3.ttf', size=22)
    if len(str(dictTime['hours'])) == 1:
        Alltext.text(xy=(162, 223), text=str(dictTime['hours']), fill=(255, 0, 0), font=font2)
    elif len(str(dictTime['hours'])) == 2:
        Alltext.text(xy=(162, 223), text=str(dictTime['hours'])[1], fill=(255, 0, 0), font=font2)
        Alltext.text(xy=(162 - 11, 223), text=str(dictTime['hours'])[0], fill=(255, 0, 0), font=font2)
    else:
        # 防止不可预知的bug报错
        Alltext.text(xy=(162, 223), text='?', fill=(255, 0, 0), font=font2)
    # Alltext.text(xy=(162 - 11, 223), text='5', fill=(255, 0, 0), font=font2)
    # Alltext.text(xy=(162 - 11 - 11, 223), text='0', fill=(255, 0, 0), font=font2)

    ### 分钟
    if len(str(dictTime['minutes'])) == 1:
        Alltext.text(xy=(162 + 16 + 16 + 16 + 15, 223), text=str(dictTime['minutes']), fill=(255, 0, 0), font=font2)
    elif len(str(dictTime['minutes'])) == 2:
        Alltext.text(xy=(162 + 16 + 16 + 16 + 15, 223), text=str(dictTime['minutes'])[1], fill=(255, 0, 0), font=font2)
        Alltext.text(xy=(162 + 16 + 16 + 16 + 15 - 11, 223), text=str(dictTime['minutes'])[0], fill=(255, 0, 0),
                     font=font2)
    # 周末
    # font2=ImageFont.truetype('digital-7-mono-3.ttf',size=22)
    if nowDate.strftime('%w') != '0':
        Alltext.text(xy=(162, 248), text=str(6 - int(nowDate.strftime('%w'))), fill=(255, 0, 0), font=font2)
    else:
        Alltext.text(xy=(162, 248), text='0', fill=(255, 0, 0), font=font2)
        # Alltext.text(xy=(162 - 11, 248), text='5', fill=(255, 0, 0), font=font2)
        # Alltext.text(xy=(162 - 11 - 11, 248), text='0', fill=(255, 0, 0), font=font2)

    #
    today = datetime.date.today()
    # print(today.year, today.month, today.day)
    # print("大年时间: ", lunar_date(today.year+1, 1, 1).to_datetime().date())
    # print("端午时间: ", lunar_date(today.year, 5, 5).to_datetime().date())
    # print("中秋时间: ", lunar_date(today.year, 8, 15).to_datetime().date())
    # print("元旦时间: ", f"{today.year+1}-01-01")
    # print("清明时间: ", f"{today.year+1}-04-05")
    # print("劳动时间: ", f"{today.year+1}-05-01")
    # print("国庆时间: ", f"{today.year+1}-10-01")
    distance_big_year = (lunar_date(today.year + 1, 1, 1).to_datetime().date() - today).days
    distance_5_5 = (lunar_date(today.year, 5, 5).to_datetime().date() - today).days
    distance_5_5 = distance_5_5 if distance_5_5 > 0 else (lunar_date(today.year + 1, 5, 5).to_datetime().date() - today).days
    distance_8_15 = (lunar_date(today.year, 8, 15).to_datetime().date() - today).days
    distance_8_15 = distance_8_15 if distance_8_15 > 0 else (lunar_date(today.year + 1, 8, 15).to_datetime().date() - today).days
    distance_year = (datetime.datetime.strptime(f"{today.year + 1}-01-01", "%Y-%m-%d").date() - today).days
    distance_4_5 = (datetime.datetime.strptime(f"{today.year}-04-05", "%Y-%m-%d").date() - today).days
    distance_4_5 = distance_4_5 if distance_4_5 > 0 else (datetime.datetime.strptime(f"{today.year + 1}-04-05", "%Y-%m-%d").date() - today).days
    distance_5_1 = (datetime.datetime.strptime(f"{today.year}-05-01", "%Y-%m-%d").date() - today).days
    distance_5_1 = distance_5_1 if distance_5_1 > 0 else (datetime.datetime.strptime(f"{today.year + 1}-05-01", "%Y-%m-%d").date() - today).days
    distance_10_1 = (datetime.datetime.strptime(f"{today.year}-10-01", "%Y-%m-%d").date() - today).days
    distance_10_1 = distance_10_1 if distance_10_1 > 0 else (datetime.datetime.strptime(f"{today.year + 1}-10-01", "%Y-%m-%d").date() - today).days

    time_ = {
        'chunjie' : distance_big_year ,
        'qingming' : distance_4_5 ,
        'laodong' : distance_5_1 ,
        'duanwu' : distance_5_5 ,
        'zhongqiu' : distance_8_15,
        'guoqing' : distance_10_1 ,
        'yuandan' : distance_year
    }

    #春节倒计时
    if len(str(time_['chunjie'])) == 1:
        Alltext.text(xy=(162, 248 + 25), text=str(time_['chunjie']), fill=(255, 0, 0), font=font2)
    elif len(str(time_['chunjie'])) == 2:
        Alltext.text(xy=(162, 248 + 25), text=str(time_['chunjie'])[1], fill=(255, 0, 0), font=font2)
        Alltext.text(xy=(162 - 11, 248 + 25), text=str(time_['chunjie'])[0], fill=(255, 0, 0), font=font2)
    elif len(str(time_['chunjie'])) == 3:
        Alltext.text(xy=(162, 248 + 25), text=str(time_['chunjie'])[2], fill=(255, 0, 0), font=font2)
        Alltext.text(xy=(162 - 11, 248 + 25), text=str(time_['chunjie'])[1], fill=(255, 0, 0), font=font2)
        Alltext.text(xy=(162 - 11 - 11, 248 + 25), text=str(time_['chunjie'])[0], fill=(255, 0, 0), font=font2)
    else:
        Alltext.text(xy=(162, 248 + 25), text='?', fill=(255, 0, 0), font=font2)

    #清明节倒计时
    if len(str(time_['qingming'])) == 1:
        Alltext.text(xy=(162, 248 + 25 + 25), text=str(time_['qingming']), fill=(255, 0, 0), font=font2)
    elif len(str(time_['qingming'])) == 2:
        Alltext.text(xy=(162, 248 + 25 + 25), text=str(time_['qingming'])[1], fill=(255, 0, 0), font=font2)
        Alltext.text(xy=(162-11, 248 + 25 + 25), text=str(time_['qingming'])[0], fill=(255, 0, 0), font=font2)
    elif len(str(time_['qingming'])) == 3:
        Alltext.text(xy=(162, 248 + 25 + 25), text=str(time_['qingming'])[2], fill=(255, 0, 0), font=font2)
        Alltext.text(xy=(162 - 11, 248 + 25 + 25), text=str(time_['qingming'])[1], fill=(255, 0, 0), font=font2)
        Alltext.text(xy=(162 - 11 - 11, 248 + 25 + 25), text=str(time_['qingming'])[0], fill=(255, 0, 0), font=font2)

    #劳动节倒计时
    if len(str(time_['laodong'])) == 1:
        Alltext.text(xy=(162, 248 + 25 + 25 + 26), text=str(time_['laodong']), fill=(255, 0, 0), font=font2)
    elif len(str(time_['laodong'])) == 2:
        Alltext.text(xy=(162, 248 + 25 + 25 + 26), text=str(time_['laodong'])[1], fill=(255, 0, 0), font=font2)
        Alltext.text(xy=(162 - 11, 248 + 25 + 25 + 26), text=str(time_['laodong'])[0], fill=(255, 0, 0), font=font2)
    elif len(str(time_['laodong'])) == 3:
        Alltext.text(xy=(162, 248 + 25 + 25 + 26), text=str(time_['laodong'])[2], fill=(255, 0, 0), font=font2)
        Alltext.text(xy=(162 - 11, 248 + 25 + 25 + 26), text=str(time_['laodong'])[1], fill=(255, 0, 0), font=font2)
        Alltext.text(xy=(162 - 11 - 11, 248 + 25 + 25 + 26), text=str(time_['laodong'])[0], fill=(255, 0, 0), font=font2)

    #端午节倒计时
    if len(str(time_['duanwu'])) == 1:
        Alltext.text(xy=(162, 248 + 25 + 25 + 26 + 26), text=str(time_['duanwu']), fill=(255, 0, 0), font=font2)
    elif len(str(time_['duanwu'])) == 2:
        Alltext.text(xy=(162, 248 + 25 + 25 + 26 + 26), text=str(time_['duanwu'])[1], fill=(255, 0, 0), font=font2)
        Alltext.text(xy=(162 - 11, 248 + 25 + 25 + 26 + 26), text=str(time_['duanwu'])[0], fill=(255, 0, 0), font=font2)
    elif len(str(time_['duanwu'])) == 3:
        Alltext.text(xy=(162, 248 + 25 + 25 + 26 + 26), text=str(time_['duanwu'])[2], fill=(255, 0, 0), font=font2)
        Alltext.text(xy=(162 - 11, 248 + 25 + 25 + 26 + 26), text=str(time_['duanwu'])[1], fill=(255, 0, 0), font=font2)
        Alltext.text(xy=(162 - 11 - 11, 248 + 25 + 25 + 26 + 26), text=str(time_['duanwu'])[0], fill=(255, 0, 0), font=font2)

    #中秋节倒计时
    if len(str(time_['zhongqiu'])) == 1:
        Alltext.text(xy=(162, 248 + 25 + 25 + 26 + 26 + 26), text=str(time_['zhongqiu']), fill=(255, 0, 0), font=font2)
    elif len(str(time_['zhongqiu'])) == 2:
        Alltext.text(xy=(162, 248 + 25 + 25 + 26 + 26 + 26), text=str(time_['zhongqiu'])[1], fill=(255, 0, 0), font=font2)
        Alltext.text(xy=(162 - 11, 248 + 25 + 25 + 26 + 26 + 26), text=str(time_['zhongqiu'])[0], fill=(255, 0, 0), font=font2)
    elif len(str(time_['zhongqiu'])) == 3:
        Alltext.text(xy=(162, 248 + 25 + 25 + 26 + 26 + 26), text=str(time_['zhongqiu'])[2], fill=(255, 0, 0), font=font2)
        Alltext.text(xy=(162 - 11, 248 + 25 + 25 + 26 + 26 + 26), text=str(time_['zhongqiu'])[1], fill=(255, 0, 0), font=font2)
        Alltext.text(xy=(162 - 11 - 11, 248 + 25 + 25 + 26 + 26 + 26), text=str(time_['zhongqiu'])[0], fill=(255, 0, 0),
                     font=font2)

    #国庆节倒计时
    if len(str(time_['guoqing'])) == 1:
        Alltext.text(xy=(162, 248 + 25 + 25 + 26 + 26 + 26 + 26), text=str(time_['guoqing']), fill=(255, 0, 0), font=font2)
    elif len(str(time_['guoqing'])) == 2:
        Alltext.text(xy=(162, 248 + 25 + 25 + 26 + 26 + 26 + 26), text=str(time_['guoqing'])[1], fill=(255, 0, 0), font=font2)
        Alltext.text(xy=(162 - 11, 248 + 25 + 25 + 26 + 26 + 26 + 26), text=str(time_['guoqing'])[0], fill=(255, 0, 0),
                     font=font2)
    elif len(str(time_['guoqing'])) == 3:
        Alltext.text(xy=(162, 248 + 25 + 25 + 26 + 26 + 26 + 26), text=str(time_['guoqing'])[2], fill=(255, 0, 0), font=font2)
        Alltext.text(xy=(162 - 11, 248 + 25 + 25 + 26 + 26 + 26 + 26), text=str(time_['guoqing'])[1], fill=(255, 0, 0),
                     font=font2)
        Alltext.text(xy=(162 - 11 - 11, 248 + 25 + 25 + 26 + 26 + 26 + 26), text=str(time_['guoqing'])[0], fill=(255, 0, 0),
                     font=font2)

    #元旦节倒计时
    if len(str(time_['yuandan'])) == 1:
        Alltext.text(xy=(162, 248 + 25 + 25 + 26 + 26 + 26 + 26 + 26), text=str(time_['yuandan']), fill=(255, 0, 0), font=font2)
    elif len(str(time_['yuandan'])) == 2:
        Alltext.text(xy=(162, 248 + 25 + 25 + 26 + 26 + 26 + 26 + 26), text=str(time_['yuandan'])[1], fill=(255, 0, 0), font=font2)
        Alltext.text(xy=(162 - 11, 248 + 25 + 25 + 26 + 26 + 26 + 26 + 26), text=str(time_['yuandan'])[0], fill=(255, 0, 0), font=font2)
    elif len(str(time_['yuandan'])) == 3:
        Alltext.text(xy=(162, 248 + 25 + 25 + 26 + 26 + 26 + 26 + 26), text=str(time_['yuandan'])[2], fill=(255, 0, 0), font=font2)
        Alltext.text(xy=(162 - 11, 248 + 25 + 25 + 26 + 26 + 26 + 26 + 26), text=str(time_['yuandan'])[1], fill=(255, 0, 0), font=font2)
        Alltext.text(xy=(162 - 11 - 11, 248 + 25 + 25 + 26 + 26 + 26 + 26 + 26), text=str(time_['yuandan'])[0], fill=(255, 0, 0),
                 font=font2)

    Image.Image.paste(bgimg, template, (0, 280))
    shijianchuo = str(int(time.time()))
    bgimg.save(fp="user_img\\" + shijianchuo + ".png")
    return shijianchuo

# 查询全球ip地理位置和信息
def cx_ip(IP, botID, to_wxID):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }
    html = requests.get(url='http://ip-api.com/json/' + IP + '?lang=zh-CN', headers=headers)
    jsonarr = json.loads(html.content.decode('utf-8'))
    if jsonarr["status"] == "success":
        Allresult = '====查询ip' + IP + '====' + '\n' \
                    '国家：' + jsonarr["country"] + '\n' \
                    '省份：' + jsonarr["regionName"] + '\n' \
                    '城市：' + jsonarr["city"] + '\n' \
                    '纬度：' + str(jsonarr["lat"]) + '\n' \
                    '经度：' + str(jsonarr["lon"]) + '\n' \
                    '时区：' + jsonarr["timezone"] + '\n' \
                    'ISP：' + jsonarr["isp"]
        time.sleep(random.randint(1, 5))
        send_text_msg(botID, to_wxID, Allresult)
    else:
        time.sleep(random.randint(1, 5))
        send_text_msg(botID, to_wxID, jsonarr["message"])

# 搜索斗图
def cx_doutu(text, botID, to_wxID):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }
    #获取图片内容
    html = requests.get(url='http://api.wpbom.com/api/bucket.php?msg=' + text, headers=headers)
    url_path = html.content.decode('utf-8')
    arr = url_path.split('/')
    img_downPath = basedir + '\\user_img\\' + arr[-1]
    IMG = requests.get(url=url_path, headers=headers)
    with open(img_downPath,'wb') as fp:
        for data in IMG.iter_content(1024):
            fp.write(data)
    time.sleep(random.randint(1, 5))
    send_image_msg(botID, to_wxID, img_downPath)

# 抖音视频无水印解析和背景音乐解析
def douyin_videoJX(v_url, mode, botID, to_wxID):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }
    html = requests.get(url='https://api.oick.cn/douyin/api.php?url=' + v_url , headers=headers)
    jsonarr = json.loads(html.content.decode('utf-8'))
    if jsonarr['play'] == False:
        send_text_msg(botID, to_wxID, "ERROR：Please enter a correct URL!")
        return
    # 时间戳
    sjc = str(int(time.time()))
    if mode == 'music':
        Music_downPath = basedir + '\\user_img\\' + sjc + '.mp3'
        getMusicdata = requests.get(url=jsonarr['music'], stream=True, headers=headers)
        with open(Music_downPath,'wb') as fp:
            for data in getMusicdata.iter_content():
                fp.write(data)
        time.sleep(random.randint(2, 5))
        send_file_msg(botID, to_wxID, Music_downPath)
    elif mode == 'video':
        Video_downPath = basedir + '\\user_img\\' + sjc + '.mp4'
        getVideodata = requests.get(url=jsonarr['play'], stream=True, headers=headers)
        with open(Video_downPath,'wb') as fp:
            for data in getVideodata.iter_content():
                fp.write(data)
        time.sleep(random.randint(3,6))
        send_video_msg(botID, to_wxID, Video_downPath)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)