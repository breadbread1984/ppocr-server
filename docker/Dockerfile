FROM nvidia/cuda:13.0.0-cudnn-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Shanghai
ENV PATH=/root/.local/bin:$PATH

RUN apt update

RUN apt install -y curl

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

WORKDIR /app

COPY . .

RUN rm -rf .venv

RUN uv sunc

RUN uv pip install paddlepaddle-gpu==3.2.2 -i https://www.paddlepaddle.org.cn/packages/stable/cu130/

