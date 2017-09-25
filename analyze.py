#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pip3 install matplotlib wxpy

from wxpy import *
import matplotlib.pyplot as plot
from matplotlib.font_manager import FontManager, FontProperties

cnFont = FontProperties(fname='/System/Library/Fonts/PingFang.ttc')

bot = Bot(console_qr=True, cache_path=True)

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


def analyze():
    # sendGroup(provinceDist(),'桃园酒侠')

    # 发给自己的文件小助手
    bot.file_helper.send_image(provinceDist())

if __name__ == '__main__':
    analyze()
