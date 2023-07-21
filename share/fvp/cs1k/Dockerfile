FROM docker.io/library/ubuntu:focal
ARG version

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

RUN if [ -z $version ]; then echo "FVP version not set!" && exit 1; fi
RUN set -e ;\
    apt update -q=2 ;\
    apt full-upgrade -q=2 --yes ;\
    apt install --yes ca-certificates ;\
    apt install -q=2 --yes --no-install-recommends ${PKG_DEPS} ;\
    # Install the FVP model
    curl --connect-timeout 5 --retry 5 --retry-delay 1 -fsSLo /tmp/fvp.tgz \
    "https://developer.arm.com/-/media/Arm%20Developer%20Community/Downloads/OSS/FVP/Corstone-1000-23/Linux/FVP_Corstone_1000_11.19_21_Linux64.tgz" ;\
    tar xf /tmp/fvp.tgz -C /tmp ;\
    /tmp/FVP_Corstone_1000.sh \
      --i-agree-to-the-contained-eula \
      --destination /opt/model/FVP_Corstone_1000 \
      --no-interactive ;\
    # Cleanup
    apt clean ;\
    rm -rf /var/lib/apt/lists/* /tmp/*
