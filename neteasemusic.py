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
         u"S: search <name>\n" \
         u"L: 播放列表\n" \
         u"C: 清空播放列表\n" \
         u"N: 下一曲\n" \
         u"R: 正在播放\n" \
         u"P: 暂停\n"
		self.tmp_playlist = []
		self.playlist = []
		self.playing = ""
		self.playing_pointer = -1
		self.con = threading.Condition()
		t = threading.Thread(target=self.playsong)
		t.start()
	def msg_handler(self, args):
		arg_list = args.split(" ")  # 参数以空格为分割符
		res = self.help_msg
		if len(arg_list) == 1 and len(arg_list[0]) == 1:  # 如果接收长度为1
			arg = arg_list[0]
			if arg == u'H':  # 帮助信息
				res = self.help_msg
			elif arg == u'C':
				self.playlist = []
				self.playing_pointer = -1
				res = u'播放列表已清空'
			elif arg == u'L':
				res = ''
				for i in range(0,len(self.playlist)):
					if i == self.playing_pointer:
						res += "* "
					res = res +str(i)+' '+ self.playlist[i]['name'] + '\n'
				res += u'Pl <order> to play'	
			elif arg == u'R':
				res = self.playing
			elif arg == u'P':
				if self.con.acquire():
					self.con.notifyAll()
					self.con.release()
				self.playing_pointer = -1
				res = u'Pause'
			elif arg ==u'N':
				if len(self.playlist) > 0:
					if self.con.acquire():
						self.con.notifyAll()
						self.con.release()
					self.playing_pointer = self.playing_pointer+1
					self.playing_pointer = self.playing_pointer % len(self.playlist)
					self.playing = self.playlist[self.playing_pointer]['name']+ ' ' + self.playlist[self.playing_pointer]['artist']
					res = u'切换成功，正在播放: ' +self.playlist[self.playing_pointer]['name']
				else:
					res = u'当前播放列表为空'
		elif len(arg_list) == 2:
			arg = arg_list[0]
			res = u""
			if arg == u'S':
				self.tmp_playlist = []
				song_list = self.search(arg_list[1])
				for i in range(0,len(song_list)):
					if int(song_list[i]['fee']) != 0:
						res += u'[VIP] '
					res = res +str(i)+' '+ song_list[i]['name']+' '+song_list[i]['artist'] + '\n';
					self.tmp_playlist.append(song_list[i])
				res = res + 'Play <order> to play \nAdd <order> to add in playlist' 
			elif arg == u'Pl':
				if self.con.acquire():
					self.con.notifyAll()
					self.con.release()
				self.playing_pointer = int(arg_list[1])
				self.playing = self.playlist[self.playing_pointer]['name']+ ' ' + self.playlist[self.playing_pointer]['artist']
				res = u'切换成功，正在播放: ' +self.playlist[self.playing_pointer]['name']
			elif arg == u'Play':
				order = int(arg_list[1])
				if int(self.tmp_playlist[order]['fee']) != 0:
					res = u'收费歌曲不支持播放'
				else:
					if self.con.acquire():
						self.con.notifyAll()
						self.con.release()
					self.playing = self.tmp_playlist[order]['name'] + ' '+ self.tmp_playlist[order]['artist']
					if self.playing_pointer != -1:
						self.playlist.insert(self.playing_pointer, self.tmp_playlist[order])
					else:
						self.playlist.append(self.tmp_playlist[order])
						self.playing_pointer = len(self.playlist)-1
					self.playing = self.playlist[self.playing_pointer]['name']+ ' ' + self.playlist[self.playing_pointer]['artist']
					res = u'播放' + self.tmp_playlist[order]['name'] + ' '+ self.tmp_playlist[order]['artist']
				# url = 'http://music.163.com/song/media/outer/url?id='+str(self.tmp_playlist[order]['id']);
				# self.play(url)
			elif arg == u'Add':
				order = int(arg_list[1])
				if int(self.tmp_playlist[order]['fee']) != 0:
					res = u'收费歌曲不支持播放'
				else:
					self.playlist.append(self.tmp_playlist[order])
					res = u"添加成功"			
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
			song['duration'] = songs[i]['duration'] # play time
			song['fee'] = songs[i]['fee']
			song_list.append(song)
		return song_list
	def play(self,arg):
		os.system('mplayer '+ arg)
	def start(self):
		return "hello"
	def playsong(self):
		while True:
			if self.con.acquire():
				if self.playing_pointer != -1:
					song = self.playlist[self.playing_pointer]
					mp3_url = 'http://music.163.com/song/media/outer/url?id='+str(song["id"])
					try:
						subprocess.Popen(["pkill","mplayer"])
						time.sleep(1)
						subprocess.Popen(["mplayer", mp3_url])
						self.con.notifyAll()
						self.con.wait(int(song['duration'])/1000)
					except:
						pass
				else:
					try:
						subprocess.Popen(["pkill", "mplayer"])
						self.con.notifyAll()
						self.con.wait()
					except:
						pass
