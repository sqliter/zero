#coding=utf-8
'''
zero player
backend.py 是共享的后端部分。类似于mvc中的模型。
zero播放器设计中采用的传统的文档视图结构。但不是严格
的这种结构。也就是缺乏认真设计的。希望可以在以后不断完善这种设计。
找到一种比较好的mvc的app设计范式。

author:raymond liu
website:github.com/sqliter/zero
last edited:2017-05-01
'''
from zmplayer import ZMPlayer
# from PySide.QtCore import QObject
# class Backend(QObject):
#     def __init__(self):
#         super(Backend,self).__init__()
#         self.mplayer = ZMPlayer()
#
# import sys
# sys.modules[__name__]=Backend()
mplayer=ZMPlayer()
