FROM python:3.10.11-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV TERM=xterm

# Setup the challenge
RUN apt-get update
RUN apt-get install -y socat
RUN python3 -m pip install ecdsa gmpy2

RUN mkdir chall
COPY src/* /chall
WORKDIR /chall

RUN chmod +x server.py
RUN chmod +x flag.py

RUN echo '#!/bin/bash' > /chall/wrapper.sh && \
    echo 'export CLIENT_IP="$SOCAT_PEERADDR"' >> /chall/wrapper.sh && \
    echo './server.py "$@"' >> /chall/wrapper.sh && \
    chmod +x /chall/wrapper.sh

CMD ["socat", "-d", "tcp-listen:1259,reuseaddr,fork", "exec:'/chall/wrapper.sh 0',stderr"]
EXPOSE 1259