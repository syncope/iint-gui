FROM debian:stretch
LABEL maintainer "Christoph Rosemann <christoph.rosemann@desy.de>"

RUN apt-get update && apt-get install -y wget gnupg gnupg2 ca-certificates evince\
    && wget http://nims.desy.de/extra/desy/DESY-Debian-key.asc \
    && wget http://nims.desy.de/extra/hasylab.debian/fsec.asc \
    && apt-key add DESY-Debian-key.asc \
    && apt-key add fsec.asc \
    && echo "deb http://nims.desy.de/extra/desy stretch desy" >> /etc/apt/sources.list.d/desy.list \
    && echo "deb-src http://nims.desy.de/extra/desy stretch desy" >> /etc/apt/sources.list.d/desy.list \
    && echo "deb [arch=amd64] http://nims.desy.de/extra/hasylab.debian stretch main non-free contrib" >> /etc/apt/sources.list.d/fsec_addon.list \
    && apt-get update \
    && apt-get install -y \
        python3-psio \
        python3-adapt \
        python3-pensant \ 
        python3-iintgui

RUN useradd -ms /bin/bash iintuser

USER iintuser
WORKDIR /home/iintuser

ENV LANG en-US

ENTRYPOINT ["/usr/bin/iint-gui"]
