FROM ubuntu:25.04 AS base

SHELL ["/bin/bash", "-c"]

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Zurich
ENV PIPX_BIN_DIR=/usr/local/bin

COPY requirements.txt /tmp/requirements.txt

RUN apt update && apt install -y \
        locales \
        python3 \
        python3-dev \
        python3-pip \
        python3-full \
        python3-venv && \
    dpkg-reconfigure locales &&\
    locale-gen "en_US.UTF-8" && \
    useradd -ms /bin/bash python && \
    python3 -m venv /opt/venv && \
    source /opt/venv/bin/activate && \
    pip3 install --no-cache-dir -r /tmp/requirements.txt

FROM base AS devcontainer

RUN apt install -y \
        git \
        vim

FROM base AS prod

USER python
WORKDIR /home/python

RUN rm -rf /var/lib/apt/lists/* && \
    rm -rf /root/.cache/pip*

COPY environment.py environment.py
COPY gui.py gui.py
COPY meteo_a.py meteo_a.py
COPY schneeflocke.png schneeflocke.png
COPY simulator.py simulator.py
COPY projectile.py projectile.py