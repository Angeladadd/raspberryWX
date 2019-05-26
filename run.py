#coding=utf-8
# from WxNeteaseMusic import WxNeteaseMusic
import itchat
from neteasemusic import music

# wnm = WxNeteaseMusic()
server = music()
@itchat.msg_register(itchat.content.TEXT)
def mp3_player(msg):
    # text = msg['Text']
    # res = wnm.msg_handler(text)
    # res = u'[疑问]'
    # res = u'您好，我现在有事不在，一会儿再和您联系'
    text = msg['Text']
    res = server.msg_handler(text)
    return res

itchat.auto_login(enableCmdQR = 2)
itchat.run(debug=False)
