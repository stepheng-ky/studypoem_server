# -*- coding:utf-8 -*-
#
#   author: iflytek
#
#  本demo测试时运行的环境为：Windows + Python3.7
#  本demo测试成功运行时所安装的第三方库及其版本如下：
#   cffi==1.12.3
#   gevent==1.4.0
#   greenlet==0.4.15
#   pycparser==2.19
#   six==1.12.0
#   websocket==0.2.1
#   websocket-client==0.56.0
#   合成小语种需要传输小语种文本、使用小语种发音人vcn、tte=unicode以及修改文本编码方式
#  错误码链接：https://www.xfyun.cn/document/error-code （code返回错误码时必看）
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# 单次调用长度需小于8000字节（约2000汉字）
import random
import websocket
import datetime
import hashlib
import base64
import hmac
import json
from urllib.parse import urlencode
import ssl
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import _thread as thread
import os

STATUS_FIRST_FRAME = 0  # 第一帧的标识
STATUS_CONTINUE_FRAME = 1  # 中间帧标识
STATUS_LAST_FRAME = 2  # 最后一帧的标识


class Ws_Param(object):
    # 初始化
    def __init__(self, APPID, APIKey, APISecret, Text, Voice, Speed):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.Text = Text
        self.Voice = Voice
        self.Speed = Speed

        # 公共参数(common)
        self.CommonArgs = {"app_id": self.APPID}
        # 业务参数(business)，更多个性化参数可在官网查看
        self.BusinessArgs = {"aue": "lame", "sfl": 1, "auf": "audio/L16;rate=16000",
                             "vcn": self.Voice, "tte": "utf8", "bgs": 1, "speed": self.Speed}
        self.Data = {"status": 2, "text": str(base64.b64encode(self.Text.encode('utf-8')), "UTF8")}
        # 使用小语种须使用以下方式，此处的unicode指的是 utf16小端的编码方式，即"UTF-16LE"”
        # self.Data = {"status": 2, "text": str(base64.b64encode(self.Text.encode('utf-16')), "UTF8")}

    # 生成url
    def create_url(self):
        url = 'wss://tts-api.xfyun.cn/v2/tts'
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + "ws-api.xfyun.cn" + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + "/v2/tts " + "HTTP/1.1"
        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            self.APIKey, "hmac-sha256", "host date request-line", signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": "ws-api.xfyun.cn"
        }
        # 拼接鉴权参数，生成url
        url = url + '?' + urlencode(v)
        # print("date: ",date)
        # print("v: ",v)
        # 此处打印出建立连接时候的url,参考本demo的时候可取消上方打印的注释，比对相同参数时生成的url与自己代码生成的url是否一致
        # print('websocket url :', url)
        return url


# 收到websocket错误的处理
def on_error(ws, error):
    # print("### error:", error)
    pass

# 收到websocket关闭的处理
def on_close(ws, info, info2):
    print("### closed ###" + info + info2)

def tts(APPID,APISecret,APIKey,text,Voice,Speed,mp3_filename):
    print(f'开始生成{mp3_filename}')
    wsParam = Ws_Param(APPID=APPID, APISecret=APISecret,
                       APIKey=APIKey,
                       Text=text,
                       Voice=Voice,
                       Speed=Speed)

    def on_open(ws):
        def run(*args):
            d = {"common": wsParam.CommonArgs,
                 "business": wsParam.BusinessArgs,
                 "data": wsParam.Data,
                 }
            d = json.dumps(d)
            ws.send(d)
            if os.path.exists(mp3_filename):
                os.remove(mp3_filename)

        thread.start_new_thread(run, ())

    def on_message(ws, message):
        print(f'调用 on_message ')
        try:
            message = json.loads(message)
            code = message["code"]
            sid = message["sid"]
            audio = message["data"]["audio"]
            audio = base64.b64decode(audio)
            status = message["data"]["status"]
            # print(message)
            if status == 2:
                print("完成。")
                ws.close()
            if code != 0:
                errMsg = message["message"]
                # print("sid:%s call error:%s code is:%s" % (sid, errMsg, code))
            else:
                with open(mp3_filename, 'ab') as f:
                    f.write(audio)
        except Exception as e:
            print("receive msg,but parse exception:", e)

    wsUrl = wsParam.create_url()
    ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.on_open = on_open
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

if __name__ == "__main__":
    # 配置信息
    APPID = '7398a43d'
    APISecret = 'Y2NjMTJiMGNlODgwZDNhZjVhMTEzNTdl'
    APIKey = '151fa83f605efae92902b64883caa91f'
    Speed = 40
    chunk_size = 2000
    # Voice = "x_lele"
    # Voice = "x4_lingxiaolu_en"
    # Voice = "x4_lingxiaoxuan_en"
    # Voice = "x4_lingfeihao_eclives"
    # Voice = "x4_mengmengneutral"
    # Voice = "x4_lingxiaoyun_talk_emo" # 朗读不ok，聊天ok 聆小芸-多情感 御姐味
    # Voice = "x4_lingbosong_bad_talk" # 朗读不ok 待定 聆伯松-反派老人 豪迈男
    # Voice = "x3_xiaodu" # 朗读不ok 搞笑ok 小杜 成都话 女
    # Voice = "x2_xiaokun" # 朗读不ok 搞笑ok 讯飞小坤 河南话 男

    # Voice = "x4_lingxiaowan_boy"  # ok 35 男 聆小琬-小男孩
    # Voice = "x4_lingxiaoyao_em"  # ok 35 女 聆小瑶-情感
    # Voice = "x4_lingfeizhe_emo" # ok 40 男 聆飞哲-情感
    # Voice = "x2_wanshu" #  ok 男 讯飞万叔 有一点广播风
    Voices = ["x4_lingxiaowan_boy", "x4_lingxiaoyao_em", "x4_lingfeizhe_emo", "x2_wanshu"]
    Voice = random.choice(Voices)  # 随机一个音色

    file_name_filter = 'mp3list.20240704.txt'
    arr_filter = []
    with open(file_name_filter, 'r') as file:
        lines = file.readlines()
        for line in lines:
            arr_filter.append(int(line.strip('\\\n')))
    # for i in range(1000,9035): # max = 9035
    # arr_fix = [179, 216, 428, 479, 1455, 1651, 1770, 1957, 2145, 2272, 2655, 3772, 4028, 4161, 4729, 4980, 5139, 6076, 6496, 6969, 6992, 7450, 8386, 8567, 8811]
    arr_fix = [179]
    for i in arr_fix: # fix
        # i = 5
        if i not in arr_filter:
            poem_file_name = f'./poems_file_fmt/{i}.txt'
            # mp3_filename = f"./mp3/{i}-{Voice}-{Speed}.mp3"
            mp3_filename = f"./mp3/{i}.mp3"
            # if not os.path.exists(mp3_filename):
            file = open(poem_file_name, encoding='utf-8')
            text = file.read()
            file.close()
            print(f"------>开始tts:{poem_file_name} --> {mp3_filename}")
            text_list = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
            mp3_tmp_f_list = []
            for j,text_tmp in enumerate(text_list):
                mp3_tmp = f"./mp3/{i}-{j}.mp3"
                tts(APPID,APISecret,APIKey,text_tmp,Voice,Speed,mp3_tmp)
                with open(mp3_tmp,'rb') as f:
                    mp3_tmp_f = f.read()
                with open(mp3_filename,'ab') as f:
                    f.write(mp3_tmp_f)

        else:
            print(f'== {i} 已存在，跳过')