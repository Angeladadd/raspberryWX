#coding=utf-8
import itchat
import threading
import time
import subprocess
import os

from neteaseApi import api


class music:
	def __init__(self):
		self.netease = api.NetEase()
		self.help_msg = \
		 u"H: 帮助信息\n" \
		 u"L: 登陆网易云音乐\n" \
         u"S: search <name>\n" \
         u"N: 下一曲\n"
		self.playlist = []
	
	def msg_handler(self, args):
		arg_list = args.split(" ")  # 参数以空格为分割符
		res = "default"
		if len(arg_list) == 1 and len(arg_list[0]) == 1:  # 如果接收长度为1
			arg = arg_list[0]
			if arg == u'H':  # 帮助信息
				res = self.help_msg
			else:
				# self.play()
				res = u'默认播放本地歌曲：卡农'
		elif len(arg_list) == 2:
			arg = arg_list[0]
			res = u""
			if arg == u'S':
				song_list = self.search(arg_list[1])
				for i in range(0,len(song_list)):
					res = res +str(i)+' '+ song_list[i]['name']+' '+song_list[i]['artist'] + '\n';
					self.playlist.append(song_list[i]['id'])
				res = res + 'N <order> to play' 
			elif arg == u'N':
				order = int(arg_list[1])
				url = 'http://music.163.com/song/media/outer/url?id='+str(self.playlist[order]);
				self.play(url)
				
		return res
			
	def search(self, song_name):
		data = self.netease.search(song_name)
		cnt = len(data['result']['songs'])
		songs = data['result']['songs']
		song_list = []
		for i in range(0,cnt):
			song={}
			song['name'] = songs[i]['name']
			song['artist']=songs[i]['artists'][0]['name']
			song['id']=songs[i]['id']
			song_list.append(song)
		return song_list
	def play(self,arg):
		os.system('mplayer '+ arg)
	def start(self):
		return "hello"
