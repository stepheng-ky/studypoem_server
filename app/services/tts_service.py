# @Time    : 2024/4/29 11:31
# @Author  : Stepheng
# @Email   : 1142262478@qq.com
# @File    : tts_service.py
# 功能描述  ：tts服务,文字转语音

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
from flask import current_app
from ..config import Config

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
        # 此处打印出建立连接时候的url,参考本demo的时候可取消上方打印的注释，比对相同参数时生成的url与自己代码生成的url是否一致
        current_app.logger.debug('websocket url :', url)
        return url

# 收到websocket错误的处理
def on_error(ws, error):
    current_app.logger.debug("### error:", error)
    pass

# 收到websocket关闭的处理
def on_close(ws, info, info2):
    current_app.logger.info("### closed ###" + info + info2)
    pass

def _tts_2000(APPID,APISecret,APIKey,text,voice,speed,mp3_filename):
    """
    text生成mp3_filename，text长度2000
    """
    current_app.logger.debug(f'开始将{text}生成{mp3_filename}...')
    wsParam = Ws_Param(APPID=APPID, APISecret=APISecret,
                       APIKey=APIKey,
                       Text=text,
                       Voice=voice,
                       Speed=speed)

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
        try:
            message = json.loads(message)
            code = message["code"]
            sid = message["sid"]
            audio = message["data"]["audio"]
            audio = base64.b64decode(audio)
            status = message["data"]["status"]
            if status == 2:
                current_app.logger.debug(f"{mp3_filename}生成完成。")
                ws.close()
            if code != 0:
                errMsg = message["message"]
                current_app.logger.warning("sid:%s call error:%s code is:%s" % (sid, errMsg, code))
            else:
                with open(mp3_filename, 'ab') as f:
                    f.write(audio)
        except Exception as e:
            current_app.logger.error("receive msg,but parse exception:", e)
            pass
    wsUrl = wsParam.create_url()
    ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.on_open = on_open
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})




def _tts(text,voice="x4_lingxiaoyao_em",speed=40,mp3_filename='tmp'):
    '''
    tts，将text按2000分割并生成多个mp3，最后将多个mp3合成一个
    '''
    if voice not in _get_voice():
        return False,f'音色【{voice}】不存在.'
    if speed not in range(0,101):
        return False,f'不支持速度：{speed}.只支持(0~100)的整数.'
    try:
        APPID = Config.XF_APPID
        APISecret = Config.XF_APISecret
        APIKey = Config.XF_APIKey
        mp3_file = f'app/mp3_tts/{mp3_filename}.mp3'
        print(f'开始生成语音{mp3_file}:\nvoice:{voice}\nspeed:{speed}')
        current_app.logger.info(f'开始生成语音{mp3_file}:\ntext:{text}\nvoice:{voice}\nspeed:{speed}')
        if os.path.exists(mp3_file):
            os.remove(mp3_file)
        chunk_size = 2000
        # 大于2000，先分割文件然后生成多个mp3，最后合成一个mp3
        if len(text) > chunk_size:
            text_list = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
            for i, text_i in enumerate(text_list):
                mp3_file_tmp = f"app/mp3_tts/{mp3_filename}-{i}.mp3"
                _tts_2000(APPID,APISecret,APIKey,text_i, voice, speed, mp3_file_tmp)
                with open(mp3_file_tmp,'rb') as f:
                    mp3_file_tmp_f = f.read()
                with open(mp3_file,'ab') as f:
                    f.write(mp3_file_tmp_f)
                    os.remove(mp3_file_tmp)
        else:
            _tts_2000(APPID, APISecret, APIKey, text, voice, speed, mp3_file)
        current_app.logger.info(f'生成语音{mp3_file}完成.\n')
        print(f'生成语音{mp3_file}完成.\n')
        return True,'ok'
    except Exception as e:
        current_app.logger.error("异常：", e)
        return False,e


def _get_voice():
    voices = {
        "xiaoyan":"讯飞小燕",
        "aisjiuxu":"讯飞许久",
        "aisxping":"讯飞小萍",
        "aisjinger":"讯飞小婧",
        "aisbabyxu":"讯飞许小宝",
        # 以下音色免费使用期限截至 20240716
        "x4_lingfeihao_upbeatads":"聆飞皓-广告-男",
        "x_lele": "讯飞乐乐-女童",
        "x4_lingxiaoyao_em": "聆小瑶-情感-女",
        "x4_lingxiaolu_en": "聆小璐-女",
        "x4_lingxiaoxuan_en": "聆小璇-温柔-女",
        "x4_lingxiaowan_boy": "聆小琬-小男孩-女",
        # 以下音色免费使用期限截至 20240719
        "x4_lingfeizhe_emo":"聆飞哲-情感-男",
        "x3_xiaodu":"小杜-成都话-女",
        "x4_lingxiaoyun_talk_emo":"聆小芸-多情感-女",
        "x2_xiaokun":"讯飞小坤-河南话-男",
        "x4_mengmengneutral":"讯飞萌萌-中立-童",
        "x4_lingbosong_bad_talk":"聆伯松-反派老人-男",
        "x2_wanshu":"讯飞万叔-男",
        "x4_lingfeihao_eclives":"聆飞皓-直播-男"
    }
    return voices

if __name__ == "__main__":
    # 配置信息
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
    voices = ["x4_lingxiaowan_boy", "x4_lingxiaoyao_em", "x4_lingfeizhe_emo", "x2_wanshu"]
    voice = random.choice(voices)  # 随机一个音色
    speed = 40
    text = "这是一句完整的测试内容，你猜我是哪儿口音？"
    mp3_filename = "test20240711193308"
    _tts(text, voice, speed, mp3_filename)
    # arr_fix = [179, 216, 428, 479, 1455, 1651, 1770, 1957, 2145, 2272, 2655, 3772, 4028, 4161, 4729, 4980, 5139, 6076, 6496, 6969, 6992, 7450, 8386, 8567, 8811]
    # # arr_fix = [179]
    # for i in arr_fix: # fix
    #     poem_file_name = f'../tts/poems_file_fmt/{i}.txt'
    #     mp3_filename = f'{i}'
    #     file = open(poem_file_name, encoding='utf-8')
    #     text = file.read()
    #     file.close()
    #     current_app.logger.info(f"------>开始tts:{poem_file_name}")
    #     _tts(text,voice,speed,mp3_filename)
