FROM docker.io/library/ubuntu:focal


ENV DEBIAN_FRONTEND=noninteractive
ENV PKG_DEPS="\
    bc \
    ca-certificates \
    curl \
    libatomic1 \
    libdbus-1-3 \
    openssh-server \
    telnet \
"

ARG FVP_STDLIB_PKG

COPY $FVP_STDLIB_PKG /tmp/fvp.tgz

RUN set -e ;\
    apt update -q=2 ;\
    apt full-upgrade -q=2 --yes ;\
    apt install --yes ca-certificates ;\
    apt install -q=2 --yes --no-install-recommends ${PKG_DEPS} ;\
    # Install Morello FVP
    tar xf /tmp/fvp.tgz -C /tmp ;\
    /tmp/FVP_ARM_Std_Library.sh \
      --i-agree-to-the-contained-eula \
      --destination /opt/model/FVP/ \
      --no-interactive ;\
    # Cleanup
    apt clean ;\
    rm -rf /var/lib/apt/lists/* /tmp/*
