# coding: utf-8
import os
import settings

# botアカウントのトークンを指定
API_TOKEN = os.environ['SLACK_API_KEY']

# このbot宛のメッセージで、どの応答にも当てはまらない場合の応答文字列
DEFAULT_REPLY = "何言ってんだこいつ"

# プラグインスクリプトを置いてあるサブディレクトリ名のリスト
PLUGINS = ['plugins']
