#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pip3 install matplotlib wxpy jieba wordcloud
from wxpy import *
import matplotlib.pyplot as plot
from matplotlib.font_manager import FontManager, FontProperties
import re
import jieba
from wordcloud import WordCloud

cnFontPath = '/System/Library/Fonts/PingFang.ttc'
cnFont = FontProperties(fname=cnFontPath)

bot = Bot(console_qr=True, cache_path=True)

xiaoi = XiaoI('t0T13ypOyooD', 'peJl3US6B7W0xRr6WxgR')

jiuxiaGroup = ensure_one(bot.groups().search('桃园酒侠'))

IS_BOT = False
def setBot(isBot):
    global IS_BOT
    IS_BOT = isBot

def getBot():
    return IS_BOT

@bot.register(jiuxiaGroup,except_self=False)
def receiveGroupMessage(msg):
    if msg.text == 'bot':
        jiuxiaGroup.send('开启肥龙机器人模式')
        setBot(True)

    elif msg.text == 'endbot':
        jiuxiaGroup.send('退出肥龙机器人模式')
        setBot(False)

    elif getBot():
        xiaoi.do_reply(msg)

    elif msg.text.find('@'+bot.self.name) >=0 and msg.text.find('help') >= 0:
        jiuxiaGroup.send("'bot' - 开启肥龙机器人模式\n'endbot' - 退出肥龙机器人模式")


def sendGroup(image, toGroup):
    groups = bot.groups().search(toGroup)
    if len(groups) > 0:
        groups[0].send_image(image)
    else:
        print('Not Found %s' % toGroup)


def sendFriend(image, toFriend):
    friends = bot.groups().search(toFriend)
    if len(friends) > 0:
        friends[0].send_image(image)
    else:
        print('Not Found %s' % toFriend)


def sexRatio():
    ratio = [0, 0, 0]
    for friend in bot.friends():
        ratio[friend.sex] += 1

    other, male, female = tuple(map(lambda r: r / float(len(bot.friends())), ratio))

    print(other, male, female)
    plot.figure(1, figsize=[6, 6])
    plot.title('The proportion of male and female friends')
    plot.pie([other, male, female],
             explode=[0, 0.1, 0],
             labels=['other', 'male', 'female'],
             autopct='%1.2f%%',
             pctdistance=0.8,
             shadow=True)
    sexDistImg = 'sex.png'
    plot.savefig(sexDistImg)
    plot.close('all')
    return sexDistImg


def provinceDist():
    dist = {}
    for friend in bot.friends():
        province = friend.province if friend.province.strip() else 'other'
        if province in dist:
            dist[province] += 1
        else:
            dist[province] = 1

    plot.figure(1, figsize=[10, 6])
    plot.title('\"%s\"的微信朋友地区分布统计' % bot.self.name, fontproperties=cnFont)
    plot.xlabel('城市', fontproperties=cnFont)
    plot.ylabel('分布人数', fontproperties=cnFont)

    x = range(0, len(dist.keys()))
    plot.bar(left=x,
             height=list(dist.values()),
             align='center',
             )

    plot.xticks(x, list(dist.keys()), fontproperties=cnFont, rotation=90)

    for (x, key) in enumerate(dist.keys()):
        plot.text(x - 0.25, dist[key] + 1.5, '%d' % dist[key], fontproperties=cnFont, rotation=90)
    provinceDistImg = 'province.png'
    plot.savefig(provinceDistImg)
    plot.close('all')
    return provinceDistImg

def signatureWordCloud():
    signatureText ="".join(list(map(lambda f: re.compile('<[^>]+>').sub("",f.signature), bot.friends())))
    space_split_words = " ".join(jieba.cut(signatureText, cut_all=True))
    gen_word_cloud = WordCloud(background_color='white', max_words = 2000, max_font_size=40, random_state=42, font_path=cnFontPath).generate(space_split_words)

    word_file = "wordcloud.png"
    gen_word_cloud.to_file(word_file)
    return word_file

def analyze():

    # 发送到群组
    # sendGroup(provinceDist(),'桃园酒侠')

    # 发给自己的文件小助手
    bot.file_helper.send_image(sexRatio())
    bot.file_helper.send_image(provinceDist())
    bot.file_helper.send_image(signatureWordCloud())

if __name__ == '__main__':
    # analyze()
    embed()
