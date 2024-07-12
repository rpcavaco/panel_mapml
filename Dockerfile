FROM python:3.11

WORKDIR /home

COPY ./cfg/requirements.txt /home/requirements.txt
RUN python3 -m pip install --no-cache-dir --upgrade pip
RUN python3 -m pip install --no-cache-dir --upgrade -r /home/requirements.txt

CMD ["panel", "serve", "/home/app/app.py", "--admin", "--address", "0.0.0.0", "--port", "8090",  "--allow-websocket-origin", "*", "--num-procs", "2", "--num-threads", "0", "--static-dirs", "assets=/home/app/assets", "--index", "app"]

RUN mkdir /.cache
RUN chmod 777 /.cache