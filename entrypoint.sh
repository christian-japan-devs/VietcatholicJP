#!/bin/sh
# 環境変数のDEBUGの値がTrueの時はrunserverを、Falseの時はgunicornを実行します
# シェルスクリプトでは`[`と`$DEBUG`、`1`と`]`の間にスペースを一つ空けておかないと[]内の式を認識できないので注意
if [ $DEBUG = 'True' ]
then
    python3 manage.py makemigrations --noinput
    python3 manage.py migrate --noinput
    python3 manage.py collectstatic --noinput
    #python3 manage.py runserver localhost:8000
    gunicorn vietcatholicjp.wsgi:application --bind 0.0.0.0:8000
else
    python3.8 manage.py makemigrations --noinput
    python3.8 manage.py migrate --noinput
    python3.8 manage.py collectstatic --noinput
    # gunicornを起動させる時はプロジェクト名を指定します
    # 今回はdjangopjにします
    gunicorn vietcatholicjp.wsgi:application --bind 0.0.0.0:8000
fi