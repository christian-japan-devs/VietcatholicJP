FROM cjones/ic21

# Install client admin & python3
RUN dnf -y install oracle-instantclient-release-el8 && \
    dnf install -y python38 && \
    dnf install -y python38-pip && \
    python3.8 -m pip install cx_Oracle && \
    rm -rf /var/cache/dnf
#COPY ./clientadmin/ /lib/oracle/21/client64/lib/network/admin/

# Install app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/vietcatholicjp

# install requirement libraries for Pillow
RUN dnf -y install gcc python3-devel libjpeg-turbo-devel libjpeg-turbo-utils zlib-devel

COPY ./requirements.txt /usr/src/vietcatholicjp/requirements.txt
RUN python3.8 -m pip install --upgrade pip
RUN python3.8 -m pip install setuptools 
RUN python3.8 -m pip install -r requirements.txt
RUN mkdir -p /var/run/gunicorn
RUN mkdir -p /var/run/gunicorn/cert

#ssl
#COPY ./cert/server.crt /var/run/gunicorn/cert/server.crt
#COPY ./cert/server.key /var/run/gunicorn/cert/server.key
#COPY ./cert/server.password /var/run/gunicorn/cert/server.password

# make migrations
COPY ./manage.py /usr/src/vietcatholicjp/manage.py
#RUN python3 /usr/src/vietcatholicjp/manage.py makemigrations
# apply migrations
#RUN python3 /usr/src/vietcatholicjp/manage.py migrate

CMD ["gunicorn", "vietcatholicjp.wsgi", "--bind=unix:/var/run/gunicorn/gunicorn.sock"]