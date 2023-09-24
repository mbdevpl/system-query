ARG CUDA_VERSION="11.7.1"

FROM nvidia/cuda:${CUDA_VERSION}-devel-ubuntu22.04

SHELL ["/bin/bash", "-c"]

# set timezone

ARG TIMEZONE="Europe/Warsaw"

RUN set -Eeuxo pipefail && \
  apt-get update && \
  DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y \
    tzdata && \
  echo "${TIMEZONE}" > /etc/timezone && \
  cp "/usr/share/zoneinfo/${TIMEZONE}" /etc/localtime && \
  apt-get -qy autoremove && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

# add a non-root user

ARG USER_ID=1000
ARG GROUP_ID=1000
ARG AUX_GROUP_IDS=""

RUN set -Eeuxo pipefail && \
  (addgroup --gid "${GROUP_ID}" user || echo "group ${GROUP_ID} already exists, so not adding it") && \
  adduser --disabled-password --gecos "User" --uid "${USER_ID}" --gid "${GROUP_ID}" user && \
  echo ${AUX_GROUP_IDS} | xargs -n1 echo | xargs -I% addgroup --gid % group% && \
  echo ${AUX_GROUP_IDS} | xargs -n1 echo | xargs -I% usermod --append --groups group% user

# install dependencies

RUN set -Eeuxo pipefail && \
  apt-get update && \
  apt-get install --no-install-recommends -y \
    git \
    python3-dev \
    python3-pip \
    python3-venv \
    sudo && \
  apt-get -qy autoremove && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

WORKDIR /home/user/system-query

COPY --chown=${USER_ID}:${GROUP_ID} requirements*.txt ./

RUN set -Eeuxo pipefail && \
  pip3 install --no-cache-dir -r requirements_ci.txt

# prepare system-query for testing

USER user

VOLUME ["/home/user/system-query"]
