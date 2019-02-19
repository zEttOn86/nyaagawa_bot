# coding: utf-8
import os, sys, time, random
import settings
import pya3rt
import datetime
import pandas as pd
import numpy as np
from slackbot.bot import respond_to     # @botname: で反応するデコーダ
from slackbot.bot import listen_to      # チャネル内発言で反応するデコーダ
from slackbot.bot import default_reply  # 該当する応答がない場合に反応するデコーダ

"""
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
"""

"""
# Collection of Well known quotes for akinobu
"""
well_known_quotes_df = pd.read_csv('assets/well-known-quotes.csv',
                                    encoding="shift-jis",
                                    header=None)
"""
"""
apikey = os.environ['TALK_API_KEY']
client = pya3rt.TalkClient(apikey)

@default_reply()
def send_message(message):
    """
    メンションでのデフォルトの動作
    https://qiita.com/takahirono7/items/197375db24a03cbcd591#%E3%81%93%E3%81%AE%E8%A8%98%E4%BA%8B%E3%81%A7%E3%82%84%E3%82%8B%E3%81%93%E3%81%A8
    """
    reply_message = client.talk(message.body['text'])
    # 以下の形式でjsonが返ってくるので、replyの部分をとりだす
    # {'status': 0, 'message': 'ok', 'results': [{'perplexity': 1.2802554542585969, 'reply': '私にはよくわからないです'}]}
    message.reply(reply_message['results'][0]['reply'])


@listen_to('疲れた')
@listen_to('つかれた')
def listen_func(message):
    message.react('muscle')
    message.reply('がんばれーーーーー！！')   # メンション


@listen_to('辛い')
@listen_to('つらい')
@listen_to('turai')
def listen_func(message):
    message.react('+1')
    message.reply('がんばれーーーーー！！')   # メンション


@listen_to('あきのぶ')
@listen_to('清水')
@listen_to('名言')
@listen_to('語録')
@listen_to('先生')
@listen_to('教授')
@listen_to('感動')
@listen_to('愉悦')
@listen_to('歓喜')
@listen_to('満悦')
@listen_to('論文')
@listen_to('研究')
@listen_to('研究室')
@listen_to('検定')
@listen_to('分布')
@listen_to('手法')
@listen_to('提案')
def listen_func(message):
    idx = np.random.randint(0, len(well_known_quotes_df))
    message.reply(well_known_quotes_df.iloc[idx, 0])
