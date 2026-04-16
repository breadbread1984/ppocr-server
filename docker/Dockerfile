FROM nvidia/cuda:12.8.0-cudnn-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Shanghai

RUN apt update && apt install -y software-properties-common

RUN add-apt-repository ppa:deadsnakes/ppa -y

RUN apt install python3.12 python3.12-venv python3.12-dev wget -y

RUN python3.12 -m ensurepip --upgrade

RUN python3 -m pip install uv -i https://pypi.tuna.tsinghua.edu.cn/simple

WORKDIR /app

COPY . .

RUN rm -rf .venv

RUN python3 -m uv sync --index-url https://mirrors.aliyun.com/pypi/simple/

RUN wget https://paddle-whl.bj.bcebos.com/stable/cu128/paddlepaddle-gpu/paddlepaddle-3.2.0-cp312-cp312-linux_x86_64.whl

RUN python3 -m uv pip install paddlepaddle-3.2.0-cp312-cp312-linux_x86_64.whl

