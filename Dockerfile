FROM ayiinxd/ayiin:xd

RUN git clone -b AyiinUbot https://github.com/AyiinXd/AyiinUbot  /home/AyiinUbot/ \
    && chmod 777 /home/AyiinUbot \
    && mkdir /home/AyiinUbot/bin/

COPY ./config.env ./.env* /home/AyiinUbot/

WORKDIR /home/AyiinUbot

RUN pip3 install --upgrade pip

RUN pip3 install --no-cache-dir -U -r requirements.txt

CMD ["bash","start"]
