# -*- coding: utf-8 -*-

from linepy import *
from akad.ttypes import Message
from datetime import datetime
from time import sleep
from bs4 import BeautifulSoup
from humanfriendly import format_timespan, format_size, format_number, format_length
import time, random, sys, json, codecs, threading, glob, re, string, os, requests, subprocess, six, ast, pytz, urllib, urllib.parse
from gtts import gTTS
from googletrans import Translator
#
botStart = time.time()

Kia = LINE()
#Kia = LINE('Token')
#Kia = LINE("Email","Paswot")
Kia.log("Auth Token : " + str(Kia.authToken))
channelToken = Kia.getChannelResult()
Kia.log("Channel Token : " + str(channelToken))

readOpen = codecs.open("read.json","r","utf-8")
settingsOpen = codecs.open("temp.json","r","utf-8")

KiaMID = Kia.profile.mid
KiaProfile = Kia.getProfile()
KiaSettings = Kia.getSettings()
oepoll = OEPoll(Kia)

read = json.load(readOpen)
settings = json.load(settingsOpen)

#
settings = {
    "autoAdd": False,
    "autoJoin": False,
    "autoLeave": False,
    "autoRead": False,
    "detectMention": False,
    "lang":"JP",
    "changeGroupPicture":[],
    "Sambutan": True,
    "Sider":{},
    "checkSticker": False,
    "userAgent": [
        "Mozilla/5.0 (X11; U; Linux i586; de; rv:5.0) Gecko/20100101 Firefox/5.0",
        "Mozilla/5.0 (X11; U; Linux amd64; rv:5.0) Gecko/20100101 Firefox/5.0 (Debian)",
        "Mozilla/5.0 (X11; U; Linux amd64; en-US; rv:5.0) Gecko/20110619 Firefox/5.0",
        "Mozilla/5.0 (X11; Linux) Gecko Firefox/5.0",
        "Mozilla/5.0 (X11; Linux x86_64; rv:5.0) Gecko/20100101 Firefox/5.0 FirePHP/0.5",
        "Mozilla/5.0 (X11; Linux x86_64; rv:5.0) Gecko/20100101 Firefox/5.0 Firefox/5.0",
        "Mozilla/5.0 (X11; Linux x86_64) Gecko Firefox/5.0",
        "Mozilla/5.0 (X11; Linux ppc; rv:5.0) Gecko/20100101 Firefox/5.0",
        "Mozilla/5.0 (X11; Linux AMD64) Gecko Firefox/5.0",
        "Mozilla/5.0 (X11; FreeBSD amd64; rv:5.0) Gecko/20100101 Firefox/5.0",
        "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:5.0) Gecko/20100101 Firefox/5.0",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:5.0) Gecko/20110619 Firefox/5.0",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:5.0) Gecko/20100101 Firefox/5.0",
        "Mozilla/5.0 (Windows NT 6.1; rv:6.0) Gecko/20100101 Firefox/5.0",
        "Mozilla/5.0 (Windows NT 6.1.1; rv:5.0) Gecko/20100101 Firefox/5.0",
        "Mozilla/5.0 (Windows NT 5.2; WOW64; rv:5.0) Gecko/20100101 Firefox/5.0",
        "Mozilla/5.0 (Windows NT 5.1; U; rv:5.0) Gecko/20100101 Firefox/5.0",
        "Mozilla/5.0 (Windows NT 5.1; rv:2.0.1) Gecko/20100101 Firefox/5.0",
        "Mozilla/5.0 (Windows NT 5.0; WOW64; rv:5.0) Gecko/20100101 Firefox/5.0",
        "Mozilla/5.0 (Windows NT 5.0; rv:5.0) Gecko/20100101 Firefox/5.0"
    ],
    "mimic": {
        "copy": False,
        "status": False,
        "target": {}
    }
}

read = {
    "readPoint": {},
    "readMember": {},
    "readTime": {},
    "ROM": {}
}

myProfile = {
	"displayName": "",
	"statusMessage": "",
	"pictureStatus": ""
}

cctv = {
    "cyduk":{},
    "point":{},
    "MENTION":{},
    "sidermem":{}
}

myProfile["displayName"] = KiaProfile.displayName
myProfile["statusMessage"] = KiaProfile.statusMessage
myProfile["pictureStatus"] = KiaProfile.pictureStatus
#
def restartBot():
    print ("[ INFO ] BOT RESETTED")
    time.sleep(3)
    python = sys.executable
    os.execl(python, python, *sys.argv)
    
def logError(text):
    Kia.log("[ ERROR ] " + str(text))
    time_ = datetime.now()
    with open("errorLog.txt","a") as error:
        error.write("\n[%s] %s" % (str(time), text))
        
def sendMention(to, mid, firstmessage, lastmessage):
    try:
        arrData = ""
        text = "%s " %(str(firstmessage))
        arr = []
        mention = "@x "
        slen = str(len(text))
        elen = str(len(text) + len(mention) - 1)
        arrData = {'S':slen, 'E':elen, 'M':mid}
        arr.append(arrData)
        text += mention + str(lastmessage)
        Kia.sendMessage(to, text, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)
    except Exception as error:
        logError(error)
        Kia.sendMessage(to, "[ INFO ] Error :\n" + str(error))

def sendMessage(to, Message, contentMetadata={}, contentType=0):
    mes = Message()
    mes.to, mes._from = to, profile.mid
    mes.text = text
    mes.contentType, mes.contentMetadata = contentType, contentMetadata
    if to not in messageReq:
        messageReq[to] = -1
    messageReq[to] += 1

def sendMessageWithMention(to, mid):
    try:
        aa = '{"S":"0","E":"3","M":'+json.dumps(mid)+'}'
        text_ = '@x '
        Kia.sendMessage(to, text_, contentMetadata={'MENTION':'{"MENTIONEES":['+aa+']}'}, contentType=0)
    except Exception as error:
        logError(error)

        
def mentionMembers(to, mid):
    try:
        arrData = ""
        textx = "╔══[Mention {} User]\n╠ ".format(str(len(mid)))
        arr = []
        no = 1
        for i in mid:
            mention = "@x\n"
            slen = str(len(textx))
            elen = str(len(textx) + len(mention) - 1)
            arrData = {'S':slen, 'E':elen, 'M':i}
            arr.append(arrData)
            textx += mention
            if no < len(mid):
                no += 1
                textx += "╠ "
            else:
                try:
                    textx += "╚══[ {} ]".format(str(Kia.getGroup(to).name))
                except:
                    pass
        Kia.sendMessage(to, textx, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)
    except Exception as error:
        logError(error)
        Kia.sendMessage(to, "[ INFO ] Error :\n" + str(error))

def backupData():
    try:
        backup = settings
        f = codecs.open('temp.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        backup = read
        f = codecs.open('read.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        return True
    except Exception as error:
        logError(error)
        return False

def helpmessage():
    helpMessage = "▬▬▬▬ஜ۩۞۩ஜ▬▬▬▬" + "\n" + \
                  "╔══[ ʜᴇʟᴇᴘ ]" + "\n" + \
                  "║☯➸  Help" + "\n" + \
                  "║☯➸  Translate" + "\n" + \
                  "║☯➸  TextToSpeech" + "\n" + \
                  "╠══[ sᴛᴀᴛᴜs ᴄᴏᴍᴍᴀɴᴅ ]" + "\n" + \
                  "║☯➸  Restart" + "\n" + \
                  "║☯➸  Runtime" + "\n" + \
                  "║☯➸  Speed" + "\n" + \
                  "║☯➸  Status" + "\n" + \
                  "║☯➸  About" + "\n" + \
                  "║☯➸  nuke" + "\n" + \
                  "╠══[ sᴇᴛ ᴄᴏᴍᴇɴᴅ ]" + "\n" + \
                  "║☯➸  AutoAdd「On/Off」" + "\n" + \
                  "║☯➸  AutoJoin「On/Off」" + "\n" + \
                  "║☯➸  AutoLeave「On/Off」" + "\n" + \
                  "║☯➸  AutoRead「On/Off」" + "\n" + \
                  "║☯➸  CheckSticker「On/Off」" + "\n" + \
                  "║☯➸  Welcome「On/Off」" + "\n" + \
                  "║☯➸  Detectmention「On/Off」" + "\n" + \
                  "╠══[ sᴇʟғ ʙᴏᴏᴛ ]" + "\n" + \
                  "║☯➸  Me" + "\n" + \
                  "║☯➸  MyMid" + "\n" + \
                  "║☯➸  MyName" + "\n" + \
                  "║☯➸  MyBio" + "\n" + \
                  "║☯➸  MyPicture" + "\n" + \
                  "║☯➸  MyVideoProfile" + "\n" + \
                  "║☯➸  MyCover" + "\n" + \
                  "║☯➸  Contact「@」" + "\n" + \
                  "║☯➸  Mid「@」" + "\n" + \
                  "║☯➸  Name「@」" + "\n" + \
                  "║☯➸  Bio「@」" + "\n" + \
                  "║☯➸  Picture「@」" + "\n" + \
                  "║☯➸  VideoProfile「@」" + "\n" + \
                  "║☯➸  Cover「@」" + "\n" + \
                  "║☯➸  CloneProfile「@」" + "\n" + \
                  "║☯➸  RestoreProfile" + "\n" + \
                  "║☯➸  gantipp" + "\n" + \
                  "╠══[ sᴇᴛ ɢʀᴏᴜᴘ ]" + "\n" + \
                  "║☯➸  GroupCreator" + "\n" + \
                  "║☯➸  GroupId" + "\n" + \
                  "║☯➸  GroupName" + "\n" + \
                  "║☯➸  GroupPicture" + "\n" + \
                  "║☯➸  GroupTicket「On/Off」" + "\n" + \
                  "║☯➸  GroupTicket" + "\n" + \
                  "║☯➸  GroupList" + "\n" + \
                  "║☯➸  GroupMemberList" + "\n" + \
                  "║☯➸  GroupInfo" + "\n" + \
                  "║☯➸  Invitegroupcall 「Jumlah」" + "\n" + \
                  "║☯➸  Mimic「On/Off」" + "\n" + \
                  "║☯➸  MimicList" + "\n" + \
                  "║☯➸  MimicAdd「Mention」" + "\n" + \
                  "║☯➸  MimicDel「Mention」" + "\n" + \
                  "║☯➸  Tagall-Tag-Sepi" + "\n" + \
                  "║☯➸  Lurking「On/Off/Reset」" + "\n" + \
                  "║☯➸  Lurking" + "\n" + \
                  "╠══[ ᴍᴇᴅɪʏᴀ ]" + "\n" + \
                  "║☯➸  Kalender" + "\n" + \
                  "║☯➸  CheckDate「Date」" + "\n" + \
                  "║☯➸  InstagramInfo「UserName」" + "\n" + \
                  "║☯➸  InstagramPost「UserName」" + "\n" + \
                  "║☯➸  SearchYoutube「Search」" + "\n" + \
                  "║☯➸  SearchImage「Search」" + "\n" + \
                  "║☯➸  ScreenshootWebsite「LinkURL」" + "\n" + \
                  "╚══[     вoтaĸ вoт      ]" + "\n" + \
                  "▬▬▬▬ஜ۩۞۩ஜ▬▬▬▬"
    return helpMessage
    
def helptexttospeech():
    helpTextToSpeech =   "╔══[ тeхт тo ѕpeecн ]" + "\n" + \
                         "║☯➸  af : Afrikaans" + "\n" + \
                         "║☯➸  sq : Albanian" + "\n" + \
                         "║☯➸  ar : Arabic" + "\n" + \
                         "║☯➸  hy : Armenian" + "\n" + \
                         "║☯➸  bn : Bengali" + "\n" + \
                         "║☯➸  ca : Catalan" + "\n" + \
                         "║☯➸  zh : Chinese" + "\n" + \
                         "║☯➸  zh-cn : Chinese (Mandarin/China)" + "\n" + \
                         "║☯➸  zh-tw : Chinese (Mandarin/Taiwan)" + "\n" + \
                         "║☯➸  zh-yue : Chinese (Cantonese)" + "\n" + \
                         "║☯➸  hr : Croatian" + "\n" + \
                         "║☯➸  cs : Czech" + "\n" + \
                         "║☯➸  da : Danish" + "\n" + \
                         "║☯➸  nl : Dutch" + "\n" + \
                         "║☯➸  en : English" + "\n" + \
                         "║☯➸  en-au : English (Australia)" + "\n" + \
                         "║☯➸  en-uk : English (United Kingdom)" + "\n" + \
                         "║☯➸  en-us : English (United States)" + "\n" + \
                         "║☯➸  eo : Esperanto" + "\n" + \
                         "║☯➸  fi : Finnish" + "\n" + \
                         "║☯➸  fr : French" + "\n" + \
                         "║☯➸  de : German" + "\n" + \
                         "║☯➸  el : Greek" + "\n" + \
                         "║☯➸  hi : Hindi" + "\n" + \
                         "║☯➸  hu : Hungarian" + "\n" + \
                         "║☯➸  is : Icelandic" + "\n" + \
                         "║☯➸  id : Indonesian" + "\n" + \
                         "║☯➸  it : Italian" + "\n" + \
                         "║☯➸  ja : Japanese" + "\n" + \
                         "║☯➸  km : Khmer (Cambodian)" + "\n" + \
                         "║☯➸  ko : Korean" + "\n" + \
                         "║☯➸  la : Latin" + "\n" + \
                         "║☯➸  lv : Latvian" + "\n" + \
                         "║☯➸  mk : Macedonian" + "\n" + \
                         "║☯➸  no : Norwegian" + "\n" + \
                         "║☯➸  pl : Polish" + "\n" + \
                         "║☯➸  pt : Portuguese" + "\n" + \
                         "║☯➸  ro : Romanian" + "\n" + \
                         "║☯➸  ru : Russian" + "\n" + \
                         "║☯➸  sr : Serbian" + "\n" + \
                         "║☯➸  si : Sinhala" + "\n" + \
                         "║☯➸  sk : Slovak" + "\n" + \
                         "║☯➸  es : Spanish" + "\n" + \
                         "║☯➸  es-es : Spanish (Spain)" + "\n" + \
                         "║☯➸  es-us : Spanish (United States)" + "\n" + \
                         "║☯➸  sw : Swahili" + "\n" + \
                         "║☯➸  sv : Swedish" + "\n" + \
                         "║☯➸  ta : Tamil" + "\n" + \
                         "║☯➸  th : Thai" + "\n" + \
                         "║☯➸  tr : Turkish" + "\n" + \
                         "║☯➸  uk : Ukrainian" + "\n" + \
                         "║☯➸  vi : Vietnamese" + "\n" + \
                         "║☯➸  cy : Welsh" + "\n" + \
                         "╚══[ ĸepo aн ]" + "\n" + "\n\n" + \
                          "conтoн : ѕay-ιd ĸaмυ jeleĸ"
    return helpTextToSpeech
    
def helptranslate():
    helpTranslate =    "╔══[ тranѕlaтe ]" + "\n" + \
                       "║☯➸  af : afrikaans" + "\n" + \
                       "║☯➸  sq : albanian" + "\n" + \
                       "║☯➸  am : amharic" + "\n" + \
                       "║☯➸  ar : arabic" + "\n" + \
                       "║☯➸  hy : armenian" + "\n" + \
                       "║☯➸  az : azerbaijani" + "\n" + \
                       "║☯➸  eu : basque" + "\n" + \
                       "║☯➸  be : belarusian" + "\n" + \
                       "║☯➸  bn : bengali" + "\n" + \
                       "║☯➸  bs : bosnian" + "\n" + \
                       "║☯➸  bg : bulgarian" + "\n" + \
                       "║☯➸  ca : catalan" + "\n" + \
                       "║☯➸  ceb : cebuano" + "\n" + \
                       "║☯➸  ny : chichewa" + "\n" + \
                       "║☯➸  zh-cn : chinese (simplified)" + "\n" + \
                       "║☯➸  zh-tw : chinese (traditional)" + "\n" + \
                       "║☯➸  co : corsican" + "\n" + \
                       "║☯➸  hr : croatian" + "\n" + \
                       "║☯➸  cs : czech" + "\n" + \
                       "║☯➸  da : danish" + "\n" + \
                       "║☯➸  nl : dutch" + "\n" + \
                       "║☯➸  en : english" + "\n" + \
                       "║☯➸  eo : esperanto" + "\n" + \
                       "║☯➸  et : estonian" + "\n" + \
                       "║☯➸  tl : filipino" + "\n" + \
                       "║☯➸  fi : finnish" + "\n" + \
                       "║☯➸  fr : french" + "\n" + \
                       "║☯➸  fy : frisian" + "\n" + \
                       "║☯➸  gl : galician" + "\n" + \
                       "║☯➸  ka : georgian" + "\n" + \
                       "║☯➸  de : german" + "\n" + \
                       "║☯➸  el : greek" + "\n" + \
                       "║☯➸  gu : gujarati" + "\n" + \
                       "║☯➸  ht : haitian creole" + "\n" + \
                       "║☯➸  ha : hausa" + "\n" + \
                       "║☯➸  haw : hawaiian" + "\n" + \
                       "║☯➸  iw : hebrew" + "\n" + \
                       "║☯➸  hi : hindi" + "\n" + \
                       "║☯➸  hmn : hmong" + "\n" + \
                       "║☯➸  hu : hungarian" + "\n" + \
                       "║☯➸  is : icelandic" + "\n" + \
                       "║☯➸  ig : igbo" + "\n" + \
                       "║☯➸  id : indonesian" + "\n" + \
                       "║☯➸  ga : irish" + "\n" + \
                       "║☯➸  it : italian" + "\n" + \
                       "║☯➸  ja : japanese" + "\n" + \
                       "║☯➸  jw : javanese" + "\n" + \
                       "║☯➸  kn : kannada" + "\n" + \
                       "║☯➸  kk : kazakh" + "\n" + \
                       "║☯➸  km : khmer" + "\n" + \
                       "║☯➸  ko : korean" + "\n" + \
                       "║☯➸  ku : kurdish (kurmanji)" + "\n" + \
                       "║☯➸  ky : kyrgyz" + "\n" + \
                       "║☯➸  lo : lao" + "\n" + \
                       "║☯➸  la : latin" + "\n" + \
                       "║☯➸  lv : latvian" + "\n" + \
                       "║☯➸  lt : lithuanian" + "\n" + \
                       "║☯➸  lb : luxembourgish" + "\n" + \
                       "║☯➸  mk : macedonian" + "\n" + \
                       "║☯➸  mg : malagasy" + "\n" + \
                       "║☯➸  ms : malay" + "\n" + \
                       "║☯➸  ml : malayalam" + "\n" + \
                       "║☯➸  mt : maltese" + "\n" + \
                       "║☯➸  mi : maori" + "\n" + \
                       "║☯➸  mr : marathi" + "\n" + \
                       "║☯➸  mn : mongolian" + "\n" + \
                       "║☯➸  my : myanmar (burmese)" + "\n" + \
                       "║☯➸  ne : nepali" + "\n" + \
                       "║☯➸  no : norwegian" + "\n" + \
                       "║☯➸  ps : pashto" + "\n" + \
                       "║☯➸  fa : persian" + "\n" + \
                       "║☯➸  pl : polish" + "\n" + \
                       "║☯➸  pt : portuguese" + "\n" + \
                       "║☯➸  pa : punjabi" + "\n" + \
                       "║☯➸  ro : romanian" + "\n" + \
                       "║☯➸  ru : russian" + "\n" + \
                       "║☯➸  sm : samoan" + "\n" + \
                       "║☯➸  gd : scots gaelic" + "\n" + \
                       "║☯➸  sr : serbian" + "\n" + \
                       "║☯➸  st : sesotho" + "\n" + \
                       "║☯➸  sn : shona" + "\n" + \
                       "║☯➸  sd : sindhi" + "\n" + \
                       "║☯➸  si : sinhala" + "\n" + \
                       "║☯➸  sk : slovak" + "\n" + \
                       "║☯➸  sl : slovenian" + "\n" + \
                       "║☯➸  so : somali" + "\n" + \
                       "║☯➸  es : spanish" + "\n" + \
                       "║☯➸  su : sundanese" + "\n" + \
                       "║☯➸  sw : swahili" + "\n" + \
                       "║☯➸  sv : swedish" + "\n" + \
                       "║☯➸  tg : tajik" + "\n" + \
                       "║☯➸  ta : tamil" + "\n" + \
                       "║☯➸  te : telugu" + "\n" + \
                       "║☯➸  th : thai" + "\n" + \
                       "║☯➸  tr : turkish" + "\n" + \
                       "║☯➸  uk : ukrainian" + "\n" + \
                       "║☯➸  ur : urdu" + "\n" + \
                       "║☯➸  uz : uzbek" + "\n" + \
                       "║☯➸  vi : vietnamese" + "\n" + \
                       "║☯➸  cy : welsh" + "\n" + \
                       "║☯➸  xh : xhosa" + "\n" + \
                       "║☯➸  yi : yiddish" + "\n" + \
                       "║☯➸  yo : yoruba" + "\n" + \
                       "║☯➸  zu : zulu" + "\n" + \
                       "║☯➸ fil : Filipino" + "\n" + \
                       "║☯➸ he : Hebrew" + "\n" + \
                       "╚══[ dιн ĸepo ]" + "\n" + "\n\n" + \
                         "conтoн : ѕay-ιd ĸaмυ jeleĸ"
    return helpTranslate
#
def KiaBot(op):
    try:
        if op.type == 0:
            print ("[ 0 ] END OF OPERATION")
            return
        if op.type == 5:
            print ("[ 5 ] NOTIFIED ADD CONTACT")
            if settings["autoAdd"] == True:
                Kia.sendMessage(op.param1, "нaι ĸawan {} тerιмaĸaѕιн тelaн мenaмвaнĸan ѕaya ѕeвagaι тeмan".format(str(Kia.getContact(op.param1).displayName)))
        if op.type == 13:
            print ("[ 13 ] NOTIFIED INVITE GROUP")
            group = Kia.getGroup(op.param1)
            if settings["autoJoin"] == True:
                Kia.acceptGroupInvitation(op.param1)
        if op.type == 24:
            print ("[ 24 ] NOTIFIED LEAVE ROOM")
            if settings["autoLeave"] == True:
                Kia.leaveRoom(op.param1)
        if op.type == 25:
            print ("[ 25 ] SEND MESSAGE")
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != Kia.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
            if msg.contentType == 0:
                if text is None:
                    return
                    
#
                if text.lower() == 'help':
                    helpMessage = helpmessage()
                    Kia.sendMessage(to, str(helpMessage))
                    Kia.sendContact(to, "u80abbfcbdc60a0a266c807a0dad66b1b")
                elif text.lower() == 'texttospeech':
                    helpTextToSpeech = helptexttospeech()
                    Kia.sendMessage(to, str(helpTextToSpeech))
                elif text.lower() == 'translate':
                    helpTranslate = helptranslate()
                    Kia.sendMessage(to, str(helpTranslate))
#
                elif text.lower() == 'speed':
                    start = time.time()
                    Kia.sendMessage(to, "█L▒o▒a▒d▒i▒n▒g▒")
                    elapsed_time = time.time() - start
                    Kia.sendMessage(to,format(str(elapsed_time)))
                elif text.lower() == 'restart':
                    Kia.sendMessage(to, "█L▒o▒a▒d▒i▒n▒g▒")
                    Kia.sendMessage(to, "Done Restarting")
                    restartBot()
                elif text.lower() == 'runtime':
                    timeNow = time.time()
                    runtime = timeNow - botStart
                    runtime = format_timespan(runtime)
                    Kia.sendMessage(to, "вoy geѕoт ѕelaмa {}".format(str(runtime)))
                elif text.lower() == 'about':
                    try:
                        arr = []
                        owner = "u80abbfcbdc60a0a266c807a0dad66b1b"
                        creator = Kia.getContact(owner)
                        contact = Kia.getContact(KiaMID)
                        grouplist = Kia.getGroupIdsJoined()
                        contactlist = Kia.getAllContactIds()
                        blockedlist = Kia.getBlockedContactIds()
                        ret_ = "╔══[ About Self ]"
                        ret_ += "\n║☯➸  Line : {}".format(contact.displayName)
                        ret_ += "\n║☯➸  Group : {}".format(str(len(grouplist)))
                        ret_ += "\n║☯➸  Friend : {}".format(str(len(contactlist)))
                        ret_ += "\n║☯➸  Blocked : {}".format(str(len(blockedlist)))
                        ret_ += "\n╠══[ About Selfbot ]"
                        ret_ += "\n║☯➸  Version : BOTAK BOT"
                        ret_ += "\n║☯➸  Creator : {}".format(creator.displayName)
                        ret_ += "\n╚══[ BOTAK BOOT ]"
                        Kia.sendMessage(to, str(ret_))
                    except Exception as e:
                        Kia.sendMessage(msg.to, str(e))
#
                elif text.lower() == 'status':
                    try:
                        ret_ = "╔══[ STATUS ]"
                        if settings["autoAdd"] == True: ret_ += "\n╠⎆ Auto Add ✅"
                        else: ret_ += "\n║☯➸  Auto Add ❌"
                        if settings["autoJoin"] == True: ret_ += "\n╠⎆ Auto Join ✅"
                        else: ret_ += "\n║☯➸  Auto Join ❌"
                        if settings["autoLeave"] == True: ret_ += "\n╠⎆ Auto Leave ✅"
                        else: ret_ += "\n║☯➸  Auto Leave ❌"
                        if settings["autoRead"] == True: ret_ += "\n╠⎆ Auto Read ✅"
                        else: ret_ += "\n║☯➸  Auto Read ❌"
                        if settings["checkSticker"] == True: ret_ += "\n╠⎆ Check Sticker ✅"
                        else: ret_ += "\n║☯➸  Check Sticker ❌"
                        if settings["detectMention"] == True: ret_ += "\n╠⎆ Detect Mention ✅"
                        else: ret_ += "\n║☯➸  Detect Mention ❌"
                        ret_ += "\n╚══[ STATUS ]"
                        Kia.sendMessage(to, str(ret_))
                    except Exception as e:
                        Kia.sendMessage(msg.to, str(e))
                elif text.lower() == 'autoadd on':
                    settings["autoAdd"] = True
                    Kia.sendMessage(to, "☯➸ aυтo add on")
                elif text.lower() == 'autoadd off':
                    settings["autoAdd"] = False
                    Kia.sendMessage(to, "☯➸ aυтo add oғғ")
                elif text.lower() == 'autojoin on':
                    settings["autoJoin"] = True
                    Kia.sendMessage(to, "☯➸ aυтo joιn on")
                elif text.lower() == 'autojoin off':
                    settings["autoJoin"] = False
                    Kia.sendMessage(to, "☯➸ aυтo joιn oғғ")
                elif text.lower() == 'autoleave on':
                    settings["autoLeave"] = True
                    Kia.sendMessage(to, "☯➸ aυтo leave on")
                elif text.lower() == 'autoleave off':
                    settings["autoLeave"] = False
                    Kia.sendMessage(to, "☯➸ aυтo leave oғғ")
                elif text.lower() == 'autoread on':
                    settings["autoRead"] = True
                    Kia.sendMessage(to, "☯➸ aυтo read on")
                elif text.lower() == 'autoread off':
                    settings["autoRead"] = False
                    Kia.sendMessage(to, "☯➸ aυтo read oғғ")
                elif text.lower() == 'checksticker on':
                    settings["checkSticker"] = True
                    Kia.sendMessage(to, "☯➸ cнecĸ deтaιlѕ ѕeтιcĸer on")
                elif text.lower() == 'checksticker off':
                    settings["checkSticker"] = False
                    Kia.sendMessage(to, "☯➸ cнecĸ deтaιlѕ ѕeтιcĸer oғғ")
                elif text.lower() == 'detectmention on':
                    settings["detectMention"] = True
                    Kia.sendMessage(to, "☯➸ deтecт мenтιon on")
                elif text.lower() == 'detectmention off':
                    settings["detectMention"] = False
                    Kia.sendMessage(to, "☯➸ deтecт мenтιon oғғ")
#
                elif text.lower() == 'me':
                    sendMessageWithMention(to, KiaMID)
                    Kia.sendContact(to, KiaMID)
                elif text.lower() == 'mymid':
                    Kia.sendMessage(msg.to,"[MID]\n" +  KiaMID)
                elif text.lower() == 'myname':
                    me = Kia.getContact(KiaMID)
                    Galank.sendMessage(msg.to,"[DisplayName]\n" + me.displayName)
                elif text.lower() == 'mybio':
                    me = Kia.getContact(KiaMID)
                    Kia.sendMessage(msg.to,"[StatusMessage]\n" + me.statusMessage)
                elif text.lower() == 'mypicture':
                    me = Kia.getContact(KiaMID)
                    Kia.sendImageWithURL(msg.to,"http://dl.profile.line-cdn.net/" + me.pictureStatus)
                elif text.lower() == 'myvideoprofile':
                    me = Kia.getContact(KiaMID)
                    Kia.sendVideoWithURL(msg.to,"http://dl.profile.line-cdn.net/" + me.pictureStatus + "/vp")
                elif text.lower() == 'mycover':
                    me = Kia.getContact(KiaMID)
                    cover = Kia.getProfileCoverURL(KiaMID)    
                    Kia.sendImageWithURL(msg.to, cover)
                elif msg.text.lower().startswith("contact "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            contact = Kia.getContact(ls)
                            mi_d = contact.mid
                            Kia.sendContact(msg.to, mi_d)
                elif msg.text.lower().startswith("mid "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        ret_ = "[ Mid User ]"
                        for ls in lists:
                            ret_ += "\n{}" + ls
                        Kia.sendMessage(msg.to, str(ret_))
                elif msg.text.lower().startswith("name "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            contact = Kia.getContact(ls)
                            Kia.sendMessage(msg.to, "[ Display Name ]\n" + contact.displayName)
                elif msg.text.lower().startswith("bio "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            contact = Kia.getContact(ls)
                            Kia.sendMessage(msg.to, "[ Status Message ]\n{}" + contact.statusMessage)
                elif msg.text.lower().startswith("picture "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            path = "http://dl.profile.line.naver.jp/" + Kia.getContact(ls).pictureStatus
                            Kia.sendImageWithURL(msg.to, str(path))
                elif msg.text.lower().startswith("videoprofile "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            path = "http://dl.profile.Kia.naver.jp/" + Kia.getContact(ls).pictureStatus + "/vp"
                            Kia.sendImageWithURL(msg.to, str(path))
                elif msg.text.lower().startswith("cover "):
                    if Kia != None:
                        if 'MENTION' in msg.contentMetadata.keys()!= None:
                            names = re.findall(r'@(\w+)', text)
                            mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                            mentionees = mention['MENTIONEES']
                            lists = []
                            for mention in mentionees:
                                if mention["M"] not in lists:
                                    lists.append(mention["M"])
                            for ls in lists:
                                path = Kia.getProfileCoverURL(ls)
                                Kia.sendImageWithURL(msg.to, str(path))
                elif msg.text.lower().startswith("cloneprofile "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        for mention in mentionees:
                            contact = mention["M"]
                            break
                        try:
                            Kia.cloneContactProfile(contact)
                            Kia.sendMessage(msg.to, "ᴮᴱᴿᴴᴬˢᴵᴸ ᶜᴸᴼᴺᴱ ᴹᴱᴹᴮᴱᴿ ᵀᵁᴺᴳᴳᵁ ᴮᴱᴮᴱᴿᴬᴾᴬ ˢᴬᴬᵀ ˢᴬᴹᴾᴬᴵ ᴾᴿᴼᶠᴵᴸ ᴮᴱᴿᵁᴮᴬᴴ")
                        except:
                            Kia.sendMessage(msg.to, "ᴳᴬᴳᴬᴸ ᶜᴸᴼᴺᴱ ᴹᴱᴹᴮᴱᴿ")
                elif text.lower() == 'restoreprofile':
                    try:
                        KiaProfile.displayName = str(myProfile["displayName"])
                        KiaProfile.statusMessage = str(myProfile["statusMessage"])
                        KiaProfile.pictureStatus = str(myProfile["pictureStatus"])
                        Kia.updateProfileAttribute(8, KiaProfile.pictureStatus)
                        Kia.updateProfile(KiaProfile)
                        Kia.sendMessage(msg.to, "ᴮᴱᴿᴴᴬˢᴵᴸ ᴿᴱˢᵀᴼᴿᴱ ᴾᴿᴼᶠᴵᴸᴱ ᵀᵁᴺᴳᴳᵁ ᴮᴱᴮᴱᴿᴬᴾᴬ ˢᴬᴬᵀˢᴬᴹᴾᴬᴵᴾᴿᴼᶠᴵᴸ ᴮᴱᴿᵁᴮᴬᴴ")
                    except:
                        Kia.sendMessage(msg.to, "ᴳᴬᴳᴬᴸ ᴿᴱˢᵀᴼᴿᴱ ᴾᴿᴼᶠᴵᴸᴱ")
#
                elif msg.text.lower().startswith("mimicadd "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            settings["mimic"]["target"][target] = True
                            Kia.sendMessage(msg.to,"ᵀᴬᴿᴳᴱᵀ ᴰᴵᵀᴬᴹᴮᴬᴴᴷᴬᴺ")
                            break
                        except:
                            Kia.sendMessage(msg.to,"ᴬᴰᴰᴱᴰ ᵀᴬᴿᴳᴱᵀ ᶠᴬᴵᴸ")
                            break
                elif msg.text.lower().startswith("mimicdel "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            del settings["mimic"]["target"][target]
                            Kia.sendMessage(msg.to,"ᵀᴬᴿᴳᴱᵀ ᴰᴵ ᴴᴬᴾᵁˢᴷᴬᴺ")
                            break
                        except:
                            Kia.sendMessage(msg.to,"ᴰᴱᴸᴱᴬᴰ ᵀᴬᴿᴳᴱᵀ ᶠᴬᴵᴸ")
                            break
                elif text.lower() == 'mimiclist':
                    if settings["mimic"]["target"] == {}:
                        Kia.sendMessage(msg.to,"ᵀᴵᴰᴬᴷ ᴬᴰᴬ ᵀᴬᴿᴳᴱᵀ")
                    else:
                        mc = "╔══[ Mimic List ]"
                        for mi_d in settings["mimic"]["target"]:
                            mc += "\n╠ "+Kia.getContact(mi_d).displayName
                        Kia.sendMessage(msg.to,mc + "\n╚══[ Finish ]")
                    
                elif "mimic" in msg.text.lower():
                    sep = text.split(" ")
                    mic = text.replace(sep[0] + " ","")
                    if mic == "on":
                        if settings["mimic"]["status"] == False:
                            settings["mimic"]["status"] = True
                            Kia.sendMessage(msg.to,"ᴿᴱᴬᴾᴸᵞ ᴹᴬˢˢᴬᴺᴳᴱ ᴼᴺ")
                    elif mic == "off":
                        if settings["mimic"]["status"] == True:
                            settings["mimic"]["status"] = False
                            Kia.sendMessage(msg.to,"ᴿᴱᴬᴾᴸᵞ ᴹᴬˢˢᴬᴺᴳᴱ ᴼᶠᶠ")
#
                elif text.lower() == 'groupcreator':
                    group = Kia.getGroup(to)
                    GS = group.creator.mid
                    Kia.sendContact(to, GS)
                elif text.lower() == 'groupid':
                    gid = Kia.getGroup(to)
                    Kia.sendMessage(to, "[ID Group : ]\n" + gid.id)
                elif text.lower() == 'grouppicture':
                    group = Kia.getGroup(to)
                    path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
                    Kia.sendImageWithURL(to, path)
                elif text.lower() == 'groupname':
                    gid = Kia.getGroup(to)
                    Kia.sendMessage(to, "[Nama Group : ]\n" + gid.name)
                elif text.lower() == 'groupticket':
                    if msg.toType == 2:
                        group = Kia.getGroup(to)
                        if group.preventedJoinByTicket == False:
                            ticket = Kia.reissueGroupTicket(to)
                            Kia.sendMessage(to, "[ Group Ticket ]\nhttps://line.me/R/ti/g/{}".format(str(ticket)))
                        else:
                            Kia.sendMessage(to, "Grup qr tidak terbuka silahkan buka terlebih dahulu dengan perintah {}openqr".format(str(settings["keyCommand"])))
                elif text.lower() == 'groupticket on':
                    if msg.toType == 2:
                        group = Kia.getGroup(to)
                        if group.preventedJoinByTicket == False:
                            Kia.sendMessage(to, "☯➸ ᴳᴿᴼᵁᴾ ᵟᴿ ˢᵁᴰᴬᴴ ᵀᴱᴿᴮᵁᴷᴬ")
                        else:
                            group.preventedJoinByTicket = False
                            Kia.updateGroup(group)
                            Kia.sendMessage(to, "☯➸ ᴮᴱᴿᴴᴬˢᴵᴸ ᴹᴱᴹᴮᵁᴷᴬ ᵟᴿ ᴳᴿᴼᵁᴾ")
                elif text.lower() == 'groupticket off':
                    if msg.toType == 2:
                        group = Kia.getGroup(to)
                        if group.preventedJoinByTicket == True:
                            Kia.sendMessage(to, "☯➸ ᴳᴿᴼᵁᴾ ᵟᴿ ˢᵁᴰᴬᴴ ᵀᴱᴿᵀᵁᵀᵁᴾ")
                        else:
                            group.preventedJoinByTicket = True
                            Kia.updateGroup(group)
                            Kia.sendMessage(to, "☯➸ ᴮᴱᴿᴴᴬˢᴵᴸ ᴹᴱᴺᵁᵀᴵᴾ ᵟᴿ ᴳᴿᴼᵁᴾ")
                elif text.lower() == 'groupinfo':
                    group = Kia.getGroup(to)
                    try:
                        gCreator = group.creator.displayName
                    except:
                        gCreator = "Tidak ditemukan"
                    if group.invitee is None:
                        gPending = "0"
                    else:
                        gPending = str(len(group.invitee))
                    if group.preventedJoinByTicket == True:
                        gQr = "Tertutup"
                        gTicket = "Tidak ada"
                    else:
                        gQr = "Terbuka"
                        gTicket = "https://line.me/R/ti/g/{}".format(str(Kia.reissueGroupTicket(group.id)))
                    path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
                    ret_ = "╔══[ ᴵᴺᶠᴼ ᴳᴿᴼᵁᴾ ]"
                    ret_ += "\n║☯➸  Nama Group : {}".format(str(group.name))
                    ret_ += "\n║☯➸  ID Group : {}".format(group.id)
                    ret_ += "\n║☯➸  Pembuat : {}".format(str(gCreator))
                    ret_ += "\n║☯➸  Jumlah Member : {}".format(str(len(group.members)))
                    ret_ += "\n║☯➸  Jumlah Pending : {}".format(gPending)
                    ret_ += "\n║☯➸  Group Qr : {}".format(gQr)
                    ret_ += "\n║☯➸  Group Ticket : {}".format(gTicket)
                    ret_ += "\n╚══[ ᶠᴵᴺᴵˢ ]"
                    Kia.sendMessage(to, str(ret_))
                    Kia.sendImageWithURL(to, path)
                elif text.lower() == 'groupmemberlist':
                    if msg.toType == 2:
                        group = Kia.getGroup(to)
                        ret_ = "╔══[ Member List ]"
                        no = 0 + 1
                        for mem in group.members:
                            ret_ += "\n║☯➸ {}. {}".format(str(no), str(mem.displayName))
                            no += 1
                        ret_ += "\n╚══[ Total {} ]".format(str(len(group.members)))
                        Kia.sendMessage(to, str(ret_))
                elif text.lower() == 'grouplist':
                        groups = Kia.groups
                        ret_ = "╔══[ Group List ]"
                        no = 0 + 1
                        for gid in groups:
                            group = Kia.getGroup(gid)
                            ret_ += "\n║☯➸ {}. {} | {}".format(str(no), str(group.name), str(len(group.members)))
                            no += 1
                        ret_ += "\n╚══[ Total {} Groups ]".format(str(len(groups)))
                        Kia.sendMessage(to, str(ret_))
                elif text.lower() == 'ceksider':
                                try:
                                    del cctv['point'][receiver]
                                    del cctv['sidermem'][receiver]
                                    del cctv['cyduk'][receiver]
                                except:
                                    pass
                                cctv['point'][receiver] = msg.id
                                cctv['sidermem'][receiver] = ""
                                cctv['cyduk'][receiver]=True
                elif text.lower() == 'offread':
                                if msg.to in cctv['point']:
                                    cctv['cyduk'][receiver]=False
                                    Kia.sendText(receiver, cctv['sidermem'][msg.to])

                elif text.lower() == 'welcome on':
                   if settings["Sambutan"] == True:
                       if settings["lang"] == "JP":
                           Kia.sendMessage(msg.to,"☯➸ ˢᵁᴰᴬᴴ ᴼᴺ (´▽`)")
                   else:
                       settings["Sambutan"] = True
                       if settings["lang"] == "JP":
                           Kia.sendMessage(msg.to,"☯➸ ˢᴬᴹᴮᵁᵀᴬᴺ ᴰᴵ ᴬᴷᵀᴵᶠᴷᴬᴺ (*´∀`*)")

                elif text.lower() == 'welcome off':
                   if settings["Sambutan"] == False:
                       if settings["lang"] == "JP":
                          Kia.sendMessage(msg.to,"☯➸ ˢᵁᴰᴬᴴ ᴼᶠᶠ(p′︵‵。)")
                   else: 
                       settings["Sambutan"] = False
                       if settings["lang"] == "JP":
                           Kia.sendMessage(msg.to,"☯➸ ˢᴬᴹᴮᵁᵀᴬᴺ ᴰᴵ ᴹᴬᵀᴵᴷᴬᴺ (＾∇＾)")

#          
                elif msg.text in ["Tagall","Sepi","Tag"]:
                            if msg.toType == 0:
                                sendMention(to, to, "", "")
                            elif msg.toType == 2:
                                group = Kia.getGroup(to)
                                contact = [mem.mid for mem in group.members]
                                ct1, ct2, ct3, ct4, ct5, ct6, ct7, ct8, ct9, ct10, ct11, jml = [], [], [], [], [], [], [], [], [], [], [], len(contact)
                                if jml <= 20:
                                    mentionMembers(to, contact)
                                elif jml > 20 and jml <= 40: 
                                    for a in range(0, 20):
                                        ct1 += [contact[a]]
                                    for b in range(20, jml):
                                        ct2 += [contact[b]]
                                    mentionMembers(to, ct1)
                                    mentionMembers(to, ct2)
                                elif jml > 40 and jml <= 60:
                                    for a in range(0, 20):
                                        ct1 += [contact[a]]
                                    for b in range(20, 40):
                                        ct2 += [contact[b]]
                                    for c in range(40, jml):
                                        ct3 += [contact[c]]
                                    mentionMembers(to, ct1)
                                    mentionMembers(to, ct2)
                                    mentionMembers(to, ct3)
                                elif jml > 60 and jml <= 80:
                                    for a in range(0, 20):
                                        ct1 += [contact[a]]
                                    for b in range(20, 40):
                                        ct2 += [contact[b]]
                                    for c in range(40, 60):
                                        ct3 += [contact[c]]
                                    for d in range(60, jml):
                                        ct4 += [contact[d]]
                                    mentionMembers(to, ct1)
                                    mentionMembers(to, ct2)
                                    mentionMembers(to, ct3)
                                    mentionMembers(to, ct4)
                                elif jml > 80 and jml <= 100:
                                    for a in range(0, 20):
                                        ct1 += [contact[a]]
                                    for b in range(20, 40):
                                        ct2 += [contact[b]]
                                    for c in range(40, 60):
                                        ct3 += [contact[c]]
                                    for d in range(60, 80):
                                        ct4 += [contact[d]]
                                    for e in range(80, jml):
                                        ct5 += [contact[e]]
                                    mentionMembers(to, ct1)
                                    mentionMembers(to, ct2)
                                    mentionMembers(to, ct3)
                                    mentionMembers(to, ct4)
                                    mentionMembers(to, ct5)
                                elif jml > 100 and jml <= 120:
                                    for a in range(0, 20):
                                        ct1 += [contact[a]]
                                    for b in range(20, 40):
                                        ct2 += [contact[b]]
                                    for c in range(40, 60):
                                        ct3 += [contact[c]]
                                    for d in range(60, 80):
                                        ct4 += [contact[d]]
                                    for e in range(80, 100):
                                        ct5 += [contact[e]]
                                    for f in range(100, jml):
                                        ct6 += [contact[f]]
                                    mentionMembers(to, ct1)
                                    mentionMembers(to, ct2)
                                    mentionMembers(to, ct3)
                                    mentionMembers(to, ct4)
                                    mentionMembers(to, ct5)
                                    mentionMembers(to, ct6) 
                                elif jml > 120 and jml <= 140:
                                    for a in range(0, 20):
                                        ct1 += [contact[a]]
                                    for b in range(20, 40):
                                        ct2 += [contact[b]]
                                    for c in range(40, 60):
                                        ct3 += [contact[c]]
                                    for d in range(60, 80):
                                        ct4 += [contact[d]]
                                    for e in range(80, 100):
                                        ct5 += [contact[e]]
                                    for f in range(100, 120):
                                        ct6 += [contact[f]]
                                    for g in range(120, jml):
                                        ct7 += [contact[g]]
                                    mentionMembers(to, ct1)
                                    mentionMembers(to, ct2)
                                    mentionMembers(to, ct3)
                                    mentionMembers(to, ct4)
                                    mentionMembers(to, ct5)
                                    mentionMembers(to, ct6) 
                                    mentionMembers(to, ct7) 
                                elif jml > 140 and jml <= 160:
                                    for a in range(0, 20):
                                        ct1 += [contact[a]]
                                    for b in range(20, 40):
                                        ct2 += [contact[b]]
                                    for c in range(40, 60):
                                        ct3 += [contact[c]]
                                    for d in range(60, 80):
                                        ct4 += [contact[d]]
                                    for e in range(80, 100):
                                        ct5 += [contact[e]]
                                    for f in range(100, 120):
                                        ct6 += [contact[f]]
                                    for g in range(120, 140):
                                        ct7 += [contact[g]]
                                    for h in range(140, jml):
                                        ct8 += [contact[h]]
                                    mentionMembers(to, ct1)
                                    mentionMembers(to, ct2)
                                    mentionMembers(to, ct3)
                                    mentionMembers(to, ct4)
                                    mentionMembers(to, ct5)
                                    mentionMembers(to, ct6) 
                                    mentionMembers(to, ct7) 
                                    mentionMembers(to, ct8) 
                                elif jml > 160 and jml <= 180:
                                    for a in range(0, 20):
                                        ct1 += [contact[a]]
                                    for b in range(20, 40):
                                        ct2 += [contact[b]]
                                    for c in range(40, 60):
                                        ct3 += [contact[c]]
                                    for d in range(60, 80):
                                        ct4 += [contact[d]]
                                    for e in range(80, 100):
                                        ct5 += [contact[e]]
                                    for f in range(100, 120):
                                        ct6 += [contact[f]]
                                    for g in range(120, 140):
                                        ct7 += [contact[g]]
                                    for h in range(140, 160):
                                        ct8 += [contact[h]]
                                    for i in range(160, jml):
                                        ct9 += [contact[i]]
                                    mentionMembers(to, ct1)
                                    mentionMembers(to, ct2)
                                    mentionMembers(to, ct3)
                                    mentionMembers(to, ct4)
                                    mentionMembers(to, ct5)
                                    mentionMembers(to, ct6) 
                                    mentionMembers(to, ct7) 
                                    mentionMembers(to, ct8)
                                    mentionMembers(to, ct9) 
                                elif jml > 180 and jml <= 200:
                                    for a in range(0, 20):
                                        ct1 += [contact[a]]
                                    for b in range(20, 40):
                                        ct2 += [contact[b]]
                                    for c in range(40, 60):
                                        ct3 += [contact[c]]
                                    for d in range(60, 80):
                                        ct4 += [contact[d]]
                                    for e in range(80, 100):
                                        ct5 += [contact[e]]
                                    for f in range(100, 120):
                                        ct6 += [contact[f]]
                                    for g in range(120, 140):
                                        ct7 += [contact[g]]
                                    for h in range(140, 160):
                                        ct8 += [contact[h]]
                                    for i in range(160, 180):
                                        ct9 += [contact[i]]
                                    for j in range(180, jml):
                                        ct9 += [contact[j]]
                                    mentionMembers(to, ct1)
                                    mentionMembers(to, ct2)
                                    mentionMembers(to, ct3)
                                    mentionMembers(to, ct4)
                                    mentionMembers(to, ct5)
                                    mentionMembers(to, ct6) 
                                    mentionMembers(to, ct7) 
                                    mentionMembers(to, ct8)
                                    mentionMembers(to, ct9) 
                                    mentionMembers(to, ct10) 
                                elif jml > 200 and jml <= 220:
                                    for a in range(0, 20):
                                        ct1 += [contact[a]]
                                    for b in range(20, 40):
                                        ct2 += [contact[b]]
                                    for c in range(40, 60):
                                        ct3 += [contact[c]]
                                    for d in range(60, 80):
                                        ct4 += [contact[d]]
                                    for e in range(80, 100):
                                        ct5 += [contact[e]]
                                    for f in range(100, 120):
                                        ct6 += [contact[f]]
                                    for g in range(120, 140):
                                        ct7 += [contact[g]]
                                    for h in range(140, 160):
                                        ct8 += [contact[h]]
                                    for i in range(160, 180):
                                        ct9 += [contact[i]]
                                    for j in range(180, 200):
                                        ct9 += [contact[j]]
                                    for k in range(200, jml):
                                        ct9 += [contact[k]]
                                    mentionMembers(to, ct1)
                                    mentionMembers(to, ct2)
                                    mentionMembers(to, ct3)
                                    mentionMembers(to, ct4)
                                    mentionMembers(to, ct5)
                                    mentionMembers(to, ct6) 
                                    mentionMembers(to, ct7) 
                                    mentionMembers(to, ct8)
                                    mentionMembers(to, ct9) 
                                    mentionMembers(to, ct10)
                                    mentionMembers(to, ct11) 
#
                elif text.lower() == 'gantipp':
                            settings["changePicture"] = True
                            Kia.sendMessage(to, "☯➸ ѕιlaнĸan ĸιrιм gaмвarnya")
                elif text.lower() == 'changegrouppicture':
                            if msg.toType == 2:
                                if to not in settings["changeGroupPicture"]:
                                    settings["changeGroupPicture"].append(to)
                            Kia.sendMessage(to, "☯➸ ѕιlaнĸan ĸιrιм gaмвarnya")


#

                elif text.lower() == 'lurking on':
                    tz = pytz.timezone("Asia/Jakarta")
                    timeNow = datetime.now(tz=tz)
                    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                    hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
                    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                    hr = timeNow.strftime("%A")
                    bln = timeNow.strftime("%m")
                    for i in range(len(day)):
                        if hr == day[i]: hasil = hari[i]
                    for k in range(0, len(bulan)):
                        if bln == str(k): bln = bulan[k-1]
                    readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                    if msg.to in read['readPoint']:
                            try:
                                del read['readPoint'][msg.to]
                                del read['readMember'][msg.to]
                                del read['readTime'][msg.to]
                            except:
                                pass
                            read['readPoint'][msg.to] = msg.id
                            read['readMember'][msg.to] = ""
                            read['readTime'][msg.to] = datetime.now().strftime('%H:%M:%S')
                            read['ROM'][msg.to] = {}
                            with open('read.json', 'w') as fp:
                                json.dump(read, fp, sort_keys=True, indent=4)
                                Kia.sendMessage(msg.to,"lυrĸιng already on")
                    else:
                        try:
                            del read['readPoint'][msg.to]
                            del read['readMember'][msg.to]
                            del read['readTime'][msg.to]
                        except:
                            pass
                        read['readPoint'][msg.to] = msg.id
                        read['readMember'][msg.to] = ""
                        read['readTime'][msg.to] = datetime.now().strftime('%H:%M:%S')
                        read['ROM'][msg.to] = {}
                        with open('read.json', 'w') as fp:
                            json.dump(read, fp, sort_keys=True, indent=4)
                            Kia.sendMessage(msg.to, "Set reading point:\n" + readTime)
                            
                elif text.lower() == 'lurking off':
                    tz = pytz.timezone("Asia/Jakarta")
                    timeNow = datetime.now(tz=tz)
                    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                    hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
                    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                    hr = timeNow.strftime("%A")
                    bln = timeNow.strftime("%m")
                    for i in range(len(day)):
                        if hr == day[i]: hasil = hari[i]
                    for k in range(0, len(bulan)):
                        if bln == str(k): bln = bulan[k-1]
                    readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                    if msg.to not in read['readPoint']:
                        Kia.sendMessage(msg.to,"lυrĸιng already oғғ")
                    else:
                        try:
                            del read['readPoint'][msg.to]
                            del read['readMember'][msg.to]
                            del read['readTime'][msg.to]
                        except:
                              pass
                        Kia.sendMessage(msg.to, "Delete reading point:\n" + readTime)
    
                elif text.lower() == 'lurking reset':
                    tz = pytz.timezone("Asia/Jakarta")
                    timeNow = datetime.now(tz=tz)
                    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                    hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
                    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                    hr = timeNow.strftime("%A")
                    bln = timeNow.strftime("%m")
                    for i in range(len(day)):
                        if hr == day[i]: hasil = hari[i]
                    for k in range(0, len(bulan)):
                        if bln == str(k): bln = bulan[k-1]
                    readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                    if msg.to in read["readPoint"]:
                        try:
                            del read["readPoint"][msg.to]
                            del read["readMember"][msg.to]
                            del read["readTime"][msg.to]
                        except:
                            pass
                        Kia.sendMessage(msg.to, "Reset reading point:\n" + readTime)
                    else:
                        Kia.sendMessage(msg.to, "lυrĸιng вelυм aĸтιғ jagan dι reѕeт")
                        
                elif text.lower() == 'lurking':
                    tz = pytz.timezone("Asia/Jakarta")
                    timeNow = datetime.now(tz=tz)
                    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                    hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
                    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                    hr = timeNow.strftime("%A")
                    bln = timeNow.strftime("%m")
                    for i in range(len(day)):
                        if hr == day[i]: hasil = hari[i]
                    for k in range(0, len(bulan)):
                        if bln == str(k): bln = bulan[k-1]
                    readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                    if receiver in read['readPoint']:
                        if read["ROM"][receiver].items() == []:
                            Kia.sendMessage(receiver,"[ Reader ]:\nNone")
                        else:
                            chiya = []
                            for rom in read["ROM"][receiver].items():
                                chiya.append(rom[1])
                            cmem = Kia.getContacts(chiya) 
                            zx = ""
                            zxc = ""
                            zx2 = []
                            xpesan = '[ Reader ]:\n'
                        for x in range(len(cmem)):
                            xname = str(cmem[x].displayName)
                            pesan = ''
                            pesan2 = pesan+"@c\n"
                            xlen = str(len(zxc)+len(xpesan))
                            xlen2 = str(len(zxc)+len(pesan2)+len(xpesan)-1)
                            zx = {'S':xlen, 'E':xlen2, 'M':cmem[x].mid}
                            zx2.append(zx)
                            zxc += pesan2
                        text = xpesan+ zxc + "\n[ Lurking time ]: \n" + readTime
                        try:
                            Kia.sendMessage(receiver, text, contentMetadata={'MENTION':str('{"MENTIONEES":'+json.dumps(zx2).replace(' ','')+'}')}, contentType=0)
                        except Exception as error:
                            print (error)
                        pass
                    else:
                        Kia.sendMessage(receiver,"lυrĸιng нaѕ noт вeen ѕeт.")

                elif text.lower() == 'sider on':
                    try:
                        del cctv['point'][msg.to]
                        del cctv['sidermem'][msg.to]
                        del cctv['cyduk'][msg.to]
                    except:
                        pass
                    cctv['point'][msg.to] = msg.id
                    cctv['sidermem'][msg.to] = ""
                    cctv['cyduk'][msg.to]=True 
                    settings["Sider"] = True
                    Kia.sendMessage(msg.to,"ceĸ ѕιder on")

                elif text.lower() == 'sider off':
                    if msg.to in cctv['point']:
                       cctv['cyduk'][msg.to]=False
                       settings["Sider"] = False
                       Kia.sendMessage(msg.to,"ceĸ ѕιder oғғ")
                    else:
                        Kia.sendMessage(msg.to,"ceĸ ѕιder oғғ")

#
                elif msg.text.lower().startswith("say-af "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'af'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    Kia.sendAudio(msg.to,"hasil.mp3")
        
                elif msg.text.lower().startswith("say-sq "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'sq'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    Kia.sendAudio(msg.to,"hasil.mp3")
                    
                elif msg.text.lower().startswith("say-ar "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'ar'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    Kia.sendAudio(msg.to,"hasil.mp3")
                    
                elif msg.text.lower().startswith("say-hy "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'hy'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    Kia.sendAudio(msg.to,"hasil.mp3")
                    
                elif msg.text.lower().startswith("say-bn "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'bn'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    Kia.sendAudio(msg.to,"hasil.mp3")
                    
                elif msg.text.lower().startswith("say-ca "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'ca'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    Kia.sendAudio(msg.to,"hasil.mp3")
                    
                elif msg.text.lower().startswith("say-zh "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'zh'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    Kia.sendAudio(msg.to,"hasil.mp3")
                    
                elif msg.text.lower().startswith("say-zh-cn "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'zh-cn'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    Kia.sendAudio(msg.to,"hasil.mp3")
                    
                elif msg.text.lower().startswith("say-zh-tw "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'zh-tw'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    Kia.sendAudio(msg.to,"hasil.mp3")
                    
                elif msg.text.lower().startswith("say-zh-yue "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'zh-yue'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    Kia.sendAudio(msg.to,"hasil.mp3")
                    
                elif msg.text.lower().startswith("say-hr "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'hr'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    Kia.sendAudio(msg.to,"hasil.mp3")
                    
                elif msg.text.lower().startswith("say-cs "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'cs'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    Kia.sendAudio(msg.to,"hasil.mp3")
                    
                elif msg.text.lower().startswith("say-da "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'da'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    Kia.sendAudio(msg.to,"hasil.mp3")
                    
                elif msg.text.lower().startswith("say-nl "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'nl'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    Kia.sendAudio(msg.to,"hasil.mp3")
                    
                elif msg.text.lower().startswith("say-en "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'en'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    Kia.sendAudio(msg.to,"hasil.mp3")
                    
                elif msg.text.lower().startswith("say-en-au "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'en-au'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    Kia.sendAudio(msg.to,"hasil.mp3")
                    
                elif msg.text.lower().startswith("say-en-uk "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'en-uk'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    Kia.sendAudio(msg.to,"hasil.mp3")
                    
                elif msg.text.lower().startswith("say-en-us "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'en-us'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    Kia.sendAudio(msg.to,"hasil.mp3")
                    
                elif msg.text.lower().startswith("say-eo "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'eo'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    Kia.sendAudio(msg.to,"hasil.mp3")
                    
                elif msg.text.lower().startswith("say-fi "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'fi'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    Kia.sendAudio(msg.to,"hasil.mp3")
                    
                elif msg.text.lower().startswith("say-fr "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'fr'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    Kia.sendAudio(msg.to,"hasil.mp3")
                    
                elif msg.text.lower().startswith("say-de "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'de'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    Kia.sendAudio(msg.to,"hasil.mp3")
                    
                elif msg.text.lower().startswith("say-el "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'el'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    Kia.sendAudio(msg.to,"hasil.mp3")
                    
                elif msg.text.lower().startswith("say-hi "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'hi'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    Kia.sendAudio(msg.to,"hasil.mp3")
                    
                elif msg.text.lower().startswith("say-hu "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'hu'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    Kia.sendAudio(msg.to,"hasil.mp3")
                    
                elif msg.text.lower().startswith("say-is "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'is'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    Kia.sendAudio(msg.to,"hasil.mp3")
                    
                elif msg.text.lower().startswith("say-id "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'id'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    Kia.sendAudio(msg.to,"hasil.mp3")
                    
                elif msg.text.lower().startswith("say-it "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'it'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    Kia.sendAudio(msg.to,"hasil.mp3")
                    
                elif msg.text.lower().startswith("say-ja "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'ja'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    Kia.sendAudio(msg.to,"hasil.mp3")
                    
                elif msg.text.lower().startswith("say-km "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'km'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    Kia.sendAudio(msg.to,"hasil.mp3")
                    
                elif msg.text.lower().startswith("say-ko "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'ko'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    Kia.sendAudio(msg.to,"hasil.mp3")
                    
                elif msg.text.lower().startswith("say-la "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'la'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    Kia.sendAudio(msg.to,"hasil.mp3")
                    
                elif msg.text.lower().startswith("say-lv "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'lv'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    Kia.sendAudio(msg.to,"hasil.mp3")
                    
                elif msg.text.lower().startswith("say-mk "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'mk'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    Kia.sendAudio(msg.to,"hasil.mp3")
                    
                elif msg.text.lower().startswith("say-no "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'no'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    Kia.sendAudio(msg.to,"hasil.mp3")
                    
                elif msg.text.lower().startswith("say-pl "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'pl'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    Kia.sendAudio(msg.to,"hasil.mp3")
                    
                elif msg.text.lower().startswith("say-pt "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'pt'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    Kia.sendAudio(msg.to,"hasil.mp3")
                    
                elif msg.text.lower().startswith("say-do "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'ro'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    Kia.sendAudio(msg.to,"hasil.mp3")
                    
                elif msg.text.lower().startswith("say-ru "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'ru'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    Kia.sendAudio(msg.to,"hasil.mp3")
                    
                elif msg.text.lower().startswith("say-sr "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'sr'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    Kia.sendAudio(msg.to,"hasil.mp3")
                    
                elif msg.text.lower().startswith("say-si "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'si'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    Kia.sendAudio(msg.to,"hasil.mp3")
                    
                elif msg.text.lower().startswith("say-sk "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'sk'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    Kia.sendAudio(msg.to,"hasil.mp3")
                    
                elif msg.text.lower().startswith("say-es "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'es'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    Kia.sendAudio(msg.to,"hasil.mp3")
                    
                elif msg.text.lower().startswith("say-es-es "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'es-es'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    Kia.sendAudio(msg.to,"hasil.mp3")
                    
                elif msg.text.lower().startswith("say-es-us "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'es-us'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    Kia.sendAudio(msg.to,"hasil.mp3")
                    
                elif msg.text.lower().startswith("say-sw "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'sw'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    Kia.sendAudio(msg.to,"hasil.mp3")
                    
                elif msg.text.lower().startswith("say-sv "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'sv'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    Kia.sendAudio(msg.to,"hasil.mp3")
                    
                elif msg.text.lower().startswith("say-ta "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'ta'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    Kia.sendAudio(msg.to,"hasil.mp3")
                    
                elif msg.text.lower().startswith("say-th "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'th'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    Kia.sendAudio(msg.to,"hasil.mp3")
                    
                elif msg.text.lower().startswith("say-tr "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'tr'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    Kia.sendAudio(msg.to,"hasil.mp3")
                    
                elif msg.text.lower().startswith("say-uk "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'uk'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    Kia.sendAudio(msg.to,"hasil.mp3")
                    
                elif msg.text.lower().startswith("say-vi "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'vi'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    Kia.sendAudio(msg.to,"hasil.mp3")
                    
                elif msg.text.lower().startswith("say-cy "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'cy'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    Kia.sendAudio(msg.to,"hasil.mp3")
#
                elif msg.text.lower().startswith("tr-af "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='af')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-sq "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='sq')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-am "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='am')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-ar "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='ar')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-hy "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='hy')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-az "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='az')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-eu "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='eu')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-be "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='be')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-bn "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='bn')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-bs "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='bs')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-bg "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='bg')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-ca "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='ca')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-ceb "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='ceb')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-ny "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='ny')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-zh-cn "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='zh-cn')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-zh-tw "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='zh-tw')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-co "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='co')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-hr "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='hr')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-cs "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='cs')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-da "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='da')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-nl "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='nl')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-en "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='en')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-et "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='et')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-fi "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='fi')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-fr "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='fr')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-fy "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='fy')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-gl "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='gl')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-ka "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='ka')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-de "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='de')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-el "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='el')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-gu "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='gu')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-ht "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='ht')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-ha "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='ha')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-haw "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='haw')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-iw "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='iw')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-hi "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='hi')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-hmn "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='hmn')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-hu "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='hu')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-is "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='is')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-ig "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='ig')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-id "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='id')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-ga "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='ga')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-it "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='it')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-ja "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='ja')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-jw "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='jw')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-kn "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='kn')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-kk "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='kk')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-km "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='km')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-ko "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='ko')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-ku "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='ku')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-ky "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='ky')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-lo "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='lo')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-la "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='la')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-lv "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='lv')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-lt "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='lt')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-lb "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='lb')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-mk "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='mk')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-mg "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='mg')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-ms "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='ms')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-ml "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='ml')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-mt "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='mt')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-mi "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='mi')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-mr "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='mr')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-mn "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='mn')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-my "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='my')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-ne "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='ne')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-no "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='no')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-ps "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='ps')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-fa "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='fa')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-pl "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='pl')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-pt "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='pt')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-pa "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='pa')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-ro "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='ro')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-ru "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='ru')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-sm "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='sm')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-gd "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='gd')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-sr "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='sr')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-st "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='st')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-sn "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='sn')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-sd "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='sd')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-si "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='si')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-sk "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='sk')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-sl "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='sl')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-so "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='so')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-es "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='es')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-su "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='su')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-sw "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='sw')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-sv "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='sv')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-tg "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='tg')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-ta "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='ta')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-te "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='te')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-th "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='th')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-tr "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='tr')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-uk "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='uk')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-ur "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='ur')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-uz "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='uz')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-vi "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='vi')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-cy "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='cy')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-xh "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='xh')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-yi "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='yi')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-yo "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='yo')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-zu "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='zu')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-fil "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='fil')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-he "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='he')
                    A = hasil.text
                    Kia.sendMessage(msg.to, A)
# 
                elif "spamtag @" in msg.text.lower():
                   _name = msg.text.replace("spamtag @","")
                   _nametarget = _name.rstrip(' ')
                   gs = Kia.getGroup(msg.to)
                   for g in gs.members:
                       if _nametarget == g.displayName:
                        xname = g.displayName
                        xlen = str(len(xname)+1)
                        msg.contentType = 0
                        msg.text = "@"+xname+" "
                        msg.contentMetadata ={'MENTION':'{"MENTIONEES":[{"S":"0","E":'+json.dumps(xlen)+',"M":'+json.dumps(g.mid)+'}]}','EMTVER':'4'}
                        Kia.sendMetion(msg)
                        Kia.sendMention(msg)
                        Kia.sendMetion(msg)
                     
                elif text.lower() == 'creator':
                    Kia.sendMessage(to, "мy creaтor:")
                    Kia.sendContact(to, "u80abbfcbdc60a0a266c807a0dad66b1b")

                elif msg.text.lower().startswith("/ "):
                   txt = text.split(" ")
                   jmlh = int(txt[2])
                   teks = text.replace(" "+str(txt[1])+" "+str(jmlh)+ " ","")
                   tulisan = jmlh * (teks+"\n")
                   if txt[1] == "on":
                        if jmlh <= 10000:
                             for x in range(jmlh):
                                   Kia.sendMessage(msg.to, teks)
                        else:
                               Kia.sendMessage(msg.to, "Out of range! ")
                   elif txt[1] == "off":
                         if jmlh <= 10000:
                               Kia.sendMessage(msg.to, tulisan)
                         else:
                               Kia.sendMessage(msg.to, "Out of range! ")

                elif "nuke" in msg.text.lower():
                  if msg.toType == 2:
#                    print  ("ok")
                    _name = msg.text.replace("nuke","")
                    gs = Kia.getGroup(msg.to)
                    targets = []
                    for g in gs.members:
                        if _name in g.displayName:
                            targets.append(g.mid)
                    if targets == []:
                        Kia.sendMessage(msg.to,"Not found.")
                    else:
                        for target in targets:
                                Kia.kickoutFromGroup(msg.to,[target])
                                print (msg.to,[g.mid])


                elif "invitegroupcall" in msg.text.lower():
                            if msg.toType == 2:
                                sep = text.split(" ")
                                strnum = text.replace(sep[0] + " ","")
                                num = int(strnum)
                                Kia.sendMessage(to, "вerнaѕιl мegυndang ĸe тelpon groυp")
                                for var in range(0,num):
                                    group = Kia.getGroup(to)
                                    members = [mem.mid for mem in group.members]
                                    Kia.acquireGroupCallRoute(to)
                                    Kia.inviteIntoGroupCall(to, contactIds=members)

                elif text.lower().startswith("music2 "):
                            try:
                                search = text.lower().replace("music2 ","")
                                r = requests.get("https://farzain.xyz/api/joox.php?apikey=your_api_key&id={}".format(urllib.parse.quote(search))) #untuk api key bisa requests ke web http://www.farzain.xyz/requests.php
                                data = r.text
                                data = json.loads(data)
                                info = data["info"]
                                audio = data["audio"]
                                hasil = " Hasil Musik \n"
                                hasil += "\nPenyanyi : {}".format(str(info["penyanyi"]))
                                hasil += "\nJudul : {}".format(str(info["judul"]))
                                hasil += "\nAlbum : {}".format(str(info["album"]))
                                hasil += "\n\nLink : \n1. Image : {}".format(str(data["gambar"]))
                                hasil += "\n\nLink : \n2. MP3 : {}".format(str(audio["mp3"]))
                                hasil += "\n\nLink : \n3. M4A : {}".format(str(audio["m4a"]))
                                Kia.sendImageWithURL(msg.to, str(data["gambar"]))
                                Kia.sendMessage(msg.to, "Downloading...")
                                Kia.sendAudioWithURL(msg.to, str(audio["mp3"]))
                                Kia.sendVideoWithURL(msg.to, str(audio["m4a"]))
                                Kia.sendMessage(msg.to, "Success Download...")
                            except Exception as error:
                            	Kia.sendMessage(msg.to, " Result Error \n" + str(error))


                elif text.lower() == 'kalender':
                    tz = pytz.timezone("Asia/Makassar")
                    timeNow = datetime.now(tz=tz)
                    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                    hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
                    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                    hr = timeNow.strftime("%A")
                    bln = timeNow.strftime("%m")
                    for i in range(len(day)):
                        if hr == day[i]: hasil = hari[i]
                    for k in range(0, len(bulan)):
                        if bln == str(k): bln = bulan[k-1]
                    readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                    Kia.sendMessage(msg.to, readTime)                 
                elif "screenshotwebsite" in msg.text.lower():
                    sep = text.split(" ")
                    query = text.replace(sep[0] + " ","")
                    with requests.session() as web:
                        r = web.get("http://rahandiapi.herokuapp.com/sswebAPI?key=betakey&link={}".format(urllib.parse.quote(query)))
                        data = r.text
                        data = json.loads(data)
                        Kia.sendImageWithURL(to, data["result"])
                elif "checkdate" in msg.text.lower():
                    sep = msg.text.split(" ")
                    tanggal = msg.text.replace(sep[0] + " ","")
                    r=requests.get('https://script.google.com/macros/exec?service=AKfycbw7gKzP-WYV2F5mc9RaR7yE3Ve1yN91Tjs91hp_jHSE02dSv9w&nama=ervan&tanggal='+tanggal)
                    data=r.text
                    data=json.loads(data)
                    ret_ = "╔══[ D A T E ]"
                    ret_ += "\n╠ Date Of Birth : {}".format(str(data["data"]["lahir"]))
                    ret_ += "\n╠ Age : {}".format(str(data["data"]["usia"]))
                    ret_ += "\n╠ Birthday : {}".format(str(data["data"]["ultah"]))
                    ret_ += "\n╠ Zodiak : {}".format(str(data["data"]["zodiak"]))
                    ret_ += "\n╚══[ Success ]"
                    Kia.sendMessage(to, str(ret_))
                elif "instagraminfo" in msg.text.lower():
                    sep = text.split(" ")
                    search = text.replace(sep[0] + " ","")
                    with requests.session() as web:
                        web.headers["User-Agent"] = random.choice(settings["userAgent"])
                        r = web.get("https://www.instagram.com/{}/?__a=1".format(search))
                        try:
                            data = json.loads(r.text)
                            ret_ = "╔══[ Profile Instagram ]"
                            ret_ += "\n╠ Nama : {}".format(str(data["user"]["full_name"]))
                            ret_ += "\n╠ Username : {}".format(str(data["user"]["username"]))
                            ret_ += "\n╠ Bio : {}".format(str(data["user"]["biography"]))
                            ret_ += "\n╠ Pengikut : {}".format(format_number(data["user"]["followed_by"]["count"]))
                            ret_ += "\n╠ Diikuti : {}".format(format_number(data["user"]["follows"]["count"]))
                            if data["user"]["is_verified"] == True:
                                ret_ += "\n╠ Verifikasi : Sudah"
                            else:
                                ret_ += "\n╠ Verifikasi : Belum"
                            if data["user"]["is_private"] == True:
                                ret_ += "\n╠ Akun Pribadi : Iya"
                            else:
                                ret_ += "\n╠ Akun Pribadi : Tidak"
                            ret_ += "\n╠ Total Post : {}".format(format_number(data["user"]["media"]["count"]))
                            ret_ += "\n╚══[ https://www.instagram.com/{} ]".format(search)
                            path = data["user"]["profile_pic_url_hd"]
                            Kia.sendImageWithURL(to, str(path))
                            Kia.sendMessage(to, str(ret_))
                        except:
                            Kia.sendMessage(to, "Pengguna tidak ditemukan")
                elif "instagrampost" in msg.text.lower():
                    separate = msg.text.split(" ")
                    user = msg.text.replace(separate[0] + " ","")
                    profile = "https://www.instagram.com/" + user
                    with requests.session() as x:
                        x.headers['user-agent'] = 'Mozilla/5.0'
                        end_cursor = ''
                        for count in range(1, 999):
                            print('PAGE: ', count)
                            r = x.get(profile, params={'max_id': end_cursor})
                        
                            data = re.search(r'window._sharedData = (\{.+?});</script>', r.text).group(1)
                            j    = json.loads(data)
                        
                            for node in j['entry_data']['ProfilePage'][0]['user']['media']['nodes']: 
                                if node['is_video']:
                                    page = 'https://www.instagram.com/p/' + node['code']
                                    r = x.get(page)
                                    url = re.search(r'"video_url": "([^"]+)"', r.text).group(1)
                                    print(url)
                                    Kia.sendVideoWithURL(msg.to,url)
                                else:
                                    print (node['display_src'])
                                    Kia.sendImageWithURL(msg.to,node['display_src'])
                            end_cursor = re.search(r'"end_cursor": "([^"]+)"', r.text).group(1)
                elif "searchimage" in msg.text.lower():
                    separate = msg.text.split(" ")
                    search = msg.text.replace(separate[0] + " ","")
                    with requests.session() as web:
                        web.headers["User-Agent"] = random.choice(settings["userAgent"])
                        r = web.get("http://rahandiapi.herokuapp.com/imageapi?key=betakey&q={}".format(urllib.parse.quote(search)))
                        data = r.text
                        data = json.loads(data)
                        if data["result"] != []:
                            items = data["result"]
                            path = random.choice(items)
                            a = items.index(path)
                            b = len(items)
                            Kia.sendImageWithURL(to, str(path))
                elif "searchyoutube" in msg.text.lower():
                    sep = text.split(" ")
                    search = text.replace(sep[0] + " ","")
                    params = {"search_query": search}
                    with requests.session() as web:
                        web.headers["User-Agent"] = random.choice(settings["userAgent"])
                        r = web.get("https://www.youtube.com/results", params = params)
                        soup = BeautifulSoup(r.content, "html5lib")
                        ret_ = "╔══[ Youtube Result ]"
                        datas = []
                        for data in soup.select(".yt-lockup-title > a[title]"):
                            if "&lists" not in data["href"]:
                                datas.append(data)
                        for data in datas:
                            ret_ += "\n╠══[ {} ]".format(str(data["title"]))
                            ret_ += "\n╠ https://www.youtube.com{}".format(str(data["href"]))
                        ret_ += "\n╚══[ Total {} ]".format(len(datas))
                        Kia.sendMessage(to, str(ret_))
                elif "searchmusic" in msg.text.lower():
                    sep = text.split(" ")
                    search = text.replace(sep[0] + " ","")
                    params = {'songname': search}
                    with requests.session() as web:
                        web.headers["User-Agent"] = random.choice(settings["userAgent"])
                        r = web.get("https://ide.fdlrcn.com/workspace/yumi-apis/joox?" + urllib.parse.urlencode(params))
                        try:
                            data = json.loads(r.text)
                            for song in data:
                                ret_ = "╔══[ Music ]"
                                ret_ += "\n╠ Nama lagu : {}".format(str(song[0]))
                                ret_ += "\n╠ Durasi : {}".format(str(song[1]))
                                ret_ += "\n╠ Link : {}".format(str(song[4]))
                                ret_ += "\n╚══[ reading Audio ]"
                                Kia.sendMessage(to, str(ret_))
                                Kia.sendAudioWithURL(to, song[3])
                        except:
                            Kia.sendMessage(to, "Musik tidak ditemukan")
                elif "searchlyric" in msg.text.lower():
                    sep = text.split(" ")
                    search = text.replace(sep[0] + " ","")
                    params = {'songname': search}
                    with requests.session() as web:
                        web.headers["User-Agent"] = random.choice(settings["userAgent"])
                        r = web.get("https://ide.fdlrcn.com/workspace/yumi-apis/joox?" + urllib.parse.urlencode(params))
                        try:
                            data = json.loads(r.text)
                            for song in data:
                                songs = song[5]
                                lyric = songs.replace('ti:','Title - ')
                                lyric = lyric.replace('ar:','Artist - ')
                                lyric = lyric.replace('al:','Album - ')
                                removeString = "[1234567890.:]"
                                for char in removeString:
                                    lyric = lyric.replace(char,'')
                                ret_ = "╔══[ Lyric ]"
                                ret_ += "\n╠ Nama lagu : {}".format(str(song[0]))
                                ret_ += "\n╠ Durasi : {}".format(str(song[1]))
                                ret_ += "\n╠ Link : {}".format(str(song[4]))
                                ret_ += "\n╚══[ Finish ]\n{}".format(str(lyric))
                                Kia.sendMessage(to, str(ret_))
                        except:
                            Kia.sendMessage(to, "Lirik tidak ditemukan")
            elif msg.contentType == 7:
                if settings["checkSticker"] == True:
                    stk_id = msg.contentMetadata['STKID']
                    stk_ver = msg.contentMetadata['STKVER']
                    pkg_id = msg.contentMetadata['STKPKGID']
                    ret_ = "╔══[ Sticker Info ]"
                    ret_ += "\n╠ STICKER ID : {}".format(stk_id)
                    ret_ += "\n╠ STICKER PACKAGES ID : {}".format(pkg_id)
                    ret_ += "\n╠ STICKER VERSION : {}".format(stk_ver)
                    ret_ += "\n╠ STICKER URL : line://shop/detail/{}".format(pkg_id)
                    ret_ += "\n╚══[ Finish ]"
                    Kia.sendMessage(to, str(ret_))

            elif msg.contentType == 1:
                    if settings["changePicture"] == True:
                        path = Kia.downloadObjectMsg(msg_id)
                        settings["changePicture"] = False
                        Kia.updateProfilePicture(path)
                        Kia.sendMessage(to, "Berhasil mengubah foto profile")
                    if msg.toType == 2:
                        if to in settings["changeGroupPicture"]:
                            path = Kia.downloadObjectMsg(msg_id)
                            settings["changeGroupPicture"].remove(to)
                            Kia.updateGroupPicture(to, path)
                            Kia.sendMessage(to, "Berhasil mengubah foto group")

      #print(e)
        if op.type == 65:
            try:
                at = op.param1
                msg_id = op.param2
                if settings["reread"] == True:
                    if msg_id in msg_dict:
                        if msg_dict[msg_id]["from"] not in bl:
                            Kia.sendMessage(at,"[Pelaku nya nih ]\n%s\n[Unsend Messages ]\n%s"%(Kia.getContact(msg_dict[msg_id]["from"]).displayName,msg_dict[msg_id]["text"]))
                            print ["Ingat Pesan"]
                        del msg_dict[msg_id]
                else:
                    pass
            except Exception as e:
                print(e)
#
        if op.type == 26:
            print ("[ 26 ] RECEIVE MESSAGE")
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != Kia.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
                if settings["autoRead"] == True:
                    Kia.sendChatChecked(to, msg_id)
                if to in read["readPoint"]:
                    if sender not in read["ROM"][to]:
                        read["ROM"][to][sender] = True
                if sender in settings["mimic"]["target"] and settings["mimic"]["status"] == True and settings["mimic"]["target"][sender] == True:
                    text = msg.text
                    if text is not None:
                        Kia.sendMessage(msg.to,text)
                if msg.contentType == 0 and sender not in KiaMID and msg.toType == 2:
                    if "MENTION" in list(msg.contentMetadata.keys())!= None:
                         if settings['detectMention'] == True:
                             contact = Kia.getContact(msg._from)
                             cName = contact.pictureStatus
                             balas = ["http://dl.profile.line-cdn.net/" + cName]
                             ret_ = random.choice(balas)
                             mention = ast.literal_eval(msg.contentMetadata["MENTION"])
                             mentionees = mention["MENTIONEES"]
                             for mention in mentionees:
                                   if mention["M"] in KiaMID:
                                          Kia.sendImageWithURL(to,ret_)
                                          break  
                if msg.contentType == 0 and sender not in KiaMID and msg.toType == 2:
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                       # names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if KiaMID in mention["M"]:
                              if settings["detectMention"] == True:
                                contact = Kia.getContact(sender)
                                Kia.sendMessage(to, " ──┅━✥ ʀᴇsᴘᴏɴ ✥━┅── \n ᴋᴇɴᴀᴘᴀ ᴋᴋ ɢᴇᴛᴀɢ - ɢᴇᴛᴀɢ ᴍᴇʟᴜʟᴜ \n ᴍɪɴᴛᴀ ᴅɪ ᴄɪᴘᴏᴋ ʏᴀ...!!!\n ──┅━✥ ======= ✥━┅──")

        if op.type == 17:
           print ("MEMBER JOIN TO GROUP")
           if settings["Sambutan"] == True:
             if op.param2 in KiaMID:
                 return
             ginfo = Kia.getGroup(op.param1)
             contact = Kia.getContact(op.param2)
             image = "http://dl.profile.line.naver.jp/" + contact.pictureStatus
             Kia.sendMessage(op.param1,"╔══[➣ⓗⓔⓛⓛⓞ " + Kia.getContact(op.param2).displayName + "  ]\n║☯➸ ᏔᎬᏞᏟᎾᎷᎬ ᎢᎾ  ☞ " + str(ginfo.name) + " ☜" +"\n║☯➸ υтaмaĸan naιĸ ĸe noтe\n║☯➸ ѕιlaнĸan мencarι тιĸυgan мυ\n║☯➸ jagan вaper n ѕeмoga вeтaн ya\n╚══[ ➣SALKEN YA.......!!!  ]")
             Kia.sendImageWithURL(op.param1,image)

        if op.type == 15:
           print ("MEMBER LEAVE TO GROUP")
           if settings["Sambutan"] == True:
             if op.param2 in KiaMID:
                 return
             ginfo = Kia.getGroup(op.param1)
             contact = Kia.getContact(op.param2)
             image = "http://dl.profile.line.naver.jp/" + contact.pictureStatus
             Kia.sendImageWithURL(op.param1,image)
             Kia.sendMessage(op.param1,"╔══[ Good Bye " + Kia.getContact(op.param2).displayName + " ]\n║☯➸  nah kan minggat dia\n║☯➸  selamat berjumpa kembali\n╚══[ Dadah........... {*_+} ]")
#
        if op.type == 55:
            print ("[ 55 ] NOTIFIED READ MESSAGE")
            try:
                if cctv['cyduk'][op.param1]==True:
                    if op.param1 in cctv['point']:
                        Name = Kia.getContact(op.param2).displayName
                        if Name in cctv['sidermem'][op.param1]:
                            pass
                        else:
                            cctv['sidermem'][op.param1] += "\nâ¢ " + Name
                            if " " in Name:
                                nick = Name.split(' ')
                                if len(nick) == 2:
                                    Kia.sendMessage(op.param1, "╔══[ ᴴᴬᴵ ᴷᴷ " + "☞ " + nick[0] + " ☜" + "]\n║☯➸ ˢᴵᴺᴵ ᴳᴬᴮᵁᴺᴳ ᶜᴬᵀ ᴬᴳᴬᴿ ᴮᴵˢᴬ ˢᴬᴸᴵᴺᴳ ᴷᴱᴺᴬᴸ\n║☯➸  ᴷᴬᴸᴼ ᴳᴵᴺᵀᴵᴾ ᴹᵁᴸᵁ ᴺᵀᴬᴿ ᴮᴵᴺᵀᴵᵀᴬᴺ ᴸᴼᴴ... \n╚══[ ᶜᴬᴺᴰᴬ ᴷᴷ ᴶᴬᴳᴬᴺ ᴰᴵ ᴬᴹᴮᴵᴸ ᴴᴬᵀᴵ ]")
                                    time.sleep(0.2)
                                    mentionMembers(op.param1,[op.param2])
                                else:
                                    Kia.sendMessage(op.param1, "╔══[Assᴀʟᴀᴍᴜᴀʟᴀɪᴋᴜᴍ " + "☞" + nick[1] + " ☜" + "]\n║☯➸  nNɢɪɴᴛɪᴘ ᴍᴇʟᴜʟᴜ \n║☯➸  ᴍᴇɴᴅɪɴɢ sɪɴɪ \n║☯➸ ᴋɪᴛᴀ ɴɢᴇʀᴜᴍᴘɪ\n╚══[ SALKEN YA....]")
                                    time.sleep(0.2)
                                    mentionMembers(op.param1,[op.param2])
                            else:
                                Kia.sendMessage(op.param1, "╔══[ Nahkan " + "☞ " + Name + " ☜" + " ]\n║☯➸  Kᴇᴛᴀᴜᴡᴀɴ ɴɢɪɴᴛɪᴘ \n║☯➸  Hᴀʜᴀʜᴀ...\n╚══[ TERCIDUK ] ")
                                time.sleep(0.2)
                                mentionMembers(op.param1,[op.param2])
                    else:
                        pass
                else:
                    pass
            except:
                pass


        if op.type == 55:
            print ("[ 55 ] NOTIFIED READ MESSAGE")
            try:
                if op.param1 in read['readPoint']:
                    if op.param2 in read['readMember'][op.param1]:
                        pass
                    else:
                        read['readMember'][op.param1] += op.param2
                    read['ROM'][op.param1][op.param2] = op.param2
                    backupData()
                else:
                   pass
            except:
                pass
    except Exception as error:
        logError(error)

#
while True:
    try:
        ops = oepoll.singleTrace(count=50)
        if ops is not None:
            for op in ops:
                KiaBot(op)
                oepoll.setRevision(op.revision)
    except Exception as e:
        logError(e)
