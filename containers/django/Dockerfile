FROM cjones/ic21

# Install client admin & python3
RUN dnf -y install oracle-instantclient-release-el8 && \
    dnf install -y python38 && \
    dnf install -y python38-pip && \
    python3.8 -m pip install cx_Oracle && \
    rm -rf /var/cache/dnf
#COPY ./clientadmin/ /lib/oracle/21/client64/lib/network/admin/

# Install app
# PYTHONDONTWRITEBYTECODEとPYTHONUNBUFFEREDはオプション
# pycファイル(および__pycache__)の生成を行わないようにする
ENV PYTHONDONTWRITEBYTECODE 1
# 標準出力・標準エラーのストリームのバッファリングを行わない
ENV PYTHONUNBUFFERED 1

WORKDIR /code

# install requirement libraries for Pillow
RUN dnf -y install gcc python3-devel libjpeg-turbo-devel libjpeg-turbo-utils zlib-devel

COPY requirements.txt /code/
RUN python3.8 -m pip install --upgrade pip
RUN python3.8 -m pip install setuptools 
RUN python3.8 -m pip install -r requirements.txt

ENV PYTHONPATH /usr/src/vietcatholicjp

# entrypoint.shに実行権限を付与
RUN chmod 755 entrypoint.sh
# ソースコードをコンテナにコピー
COPY . /code/