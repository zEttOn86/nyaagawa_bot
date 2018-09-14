# coding: utf-8
import os
import settings
import pya3rt
import datetime
from plugins.const_variables import dict
from slackbot.bot import respond_to     # @botname: で反応するデコーダ
from slackbot.bot import listen_to      # チャネル内発言で反応するデコーダ
from slackbot.bot import default_reply  # 該当する応答がない場合に反応するデコーダ

# @respond_to('string')     bot宛のメッセージ
#                           stringは正規表現が可能 「r'string'」
# @listen_to('string')      チャンネル内のbot宛以外の投稿
#                           @botname: では反応しないことに注意
#                           他の人へのメンションでは反応する
#                           正規表現可能
# @default_reply()          DEFAULT_REPLY と同じ働き
#                           正規表現を指定すると、他のデコーダにヒットせず、
#                           正規表現にマッチするときに反応
#                           ・・・なのだが、正規表現を指定するとエラーになる？

# message.reply('string')   @発言者名: string でメッセージを送信
# message.send('string')    string を送信
# message.react('icon_emoji')  発言者のメッセージにリアクション(スタンプ)する
#                               文字列中に':'はいらない

@default_reply()
def send_message(message):
    """
    メンションでのデフォルトの動作
    https://qiita.com/takahirono7/items/197375db24a03cbcd591#%E3%81%93%E3%81%AE%E8%A8%98%E4%BA%8B%E3%81%A7%E3%82%84%E3%82%8B%E3%81%93%E3%81%A8
    """
    apikey = os.environ['TALK_API_KEY']
    client = pya3rt.TalkClient(apikey)
    reply_message = client.talk(message.body['text'])
    # 以下の形式でjsonが返ってくるので、replyの部分をとりだす
    # {'status': 0, 'message': 'ok', 'results': [{'perplexity': 1.2802554542585969, 'reply': '私にはよくわからないです'}]}
    #print(reply_message)
    message.reply(reply_message['results'][0]['reply'] + 'www' )

@listen_to('疲れた')
@listen_to('つかれた')
def listen_func(message):
    #message.send('誰かがつかれたと投稿したようだ')      # ただの投稿
    message.react('muscle')
    message.reply('働けwwww')                         # メンション

@listen_to('辛い')
@listen_to('つらい')
@listen_to('turai')
def listen_func(message):
    #message.send('誰かがつかれたと投稿したようだ')      # ただの投稿
    message.react('+1')
    message.send('誰かが `{}` と投稿したようだ:thinking_face:'.format(message.body['text']))
    message.reply('つらくないwwww')   # メンション


start = 0
_datetime = datetime.datetime(2000, 2, 1, 12, 15, 30) # year, month, day, hour, minute, second
margin_td3d = datetime.timedelta(days=3)
margin_td8d = datetime.timedelta(days=8)

def time_check_func():
    global _datetime, start
    _datetime_now = datetime.datetime.now()

    if _datetime_now-_datetime < margin_td3d:
        return False

    elif _datetime_now-_datetime > margin_td8d:
        temp = _datetime_now-_datetime
        for i in range(int(temp.days/8+0.5)-1):
            start +=1
            if(start == 4):
                start = 0
        _datetime = _datetime_now
        return True

    else:
        _datetime = _datetime_now
        return True


@respond_to('個別打ち合わせ')
def mention_func(message):
    global start
    if not time_check_func():
        message.send('スパン速すぎwwww')
        return

    message.send('今日の個別打ち合わせは') # メンション

    dict_counter = start
    for i in range(4):
        message.send(dict[dict_counter])
        dict_counter += 1
        if(dict_counter==4):
            dict_counter = 0

    start += 1
    if(start == 4):
        start = 0

    message.send('です')


@respond_to(r'^set\s+\S.*')
def set_default_func(message):
    text = message.body['text']     # メッセージを取り出す
    temp, word = text.split(None, 1)    # 設定する言葉を取り出す。tempには'set'が入る
    global start     # 外で定義した変数の値を変えられるようにする
    word = int(word)
    if word >3 or word<0:
        message.send('番号は0-3を選んでください')
        return

    start = word     # デフォルトの返事を上書きする
    message.send('個別の順番を `{}` からに変更しました．'.format(dict[start]))

    dict_counter = start
    for i in range(4):
        message.send(dict[dict_counter])
        dict_counter += 1
        if(dict_counter==4):
            dict_counter = 0

    message.send('からです')

@respond_to('reset')
def mention_func(message):
    global start
    start = 0
    message.send('個別打ち合わせの順番をリセットしました')
