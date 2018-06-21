FROM ubuntu:14.04
MAINTAINER padro@cs.upc.edu

# Install dependencies
RUN locale-gen en_US.UTF-8 && \
    apt-get update -q && \
    apt-get install -y build-essential automake autoconf libtool wget \
                       libicu52 libboost-regex1.54.0 \
                       libboost-system1.54.0 libboost-program-options1.54.0 \
                       libboost-thread1.54.0 libicu-dev libboost-regex-dev \
                       libboost-system-dev libboost-program-options-dev \
                       libboost-thread-dev zlib1g-dev python3-dev make \
                       subversion swig g++ libboost-all-dev

# Install Freeling and compile Python3 API
WORKDIR /tmp
RUN wget --progress=dot:giga https://github.com/TALP-UPC/FreeLing/releases/download/4.0/FreeLing-4.0.tar.gz && \
    tar xvzf FreeLing-4.0.tar.gz && \
    rm -rf FreeLing-4.0.tar.gz && \
    cd /tmp/FreeLing-4.0 && \
    autoreconf --install && \
    ./configure && \
    make && \
    make install
RUN cd /tmp && svn export https://github.com/TALP-UPC/FreeLing.git/trunk/APIs --trust-server-cert && cd APIs/python && make
RUN mkdir -p /root/.local/lib/python3.4/site-packages/ && cd /tmp/APIs/python && cp -r * /root/.local/lib/python3.4/site-packages/

# Install pyfreeling
RUN apt-get install -y python3-pip libxml2-dev libxslt1-dev && pip3 install lxml && pip3 install pyfreeling && \
    sed -i -e "s/(input)/(input.encode('utf8'))/g" /usr/local/lib/python3.4/dist-packages/pyfreeling/__init__.py && \
    sed -i -e "s/OutputLevel=tagged/OutputLevel=morfo/g" /usr/local/share/freeling/config/es.cfg

# Install flask 
RUN cd /tmp && pip3 install -U nltk && pip3 install flask
RUN mkdir /root/app

EXPOSE 50005 5000

WORKDIR /root/app
#CMD echo 'Hello world' | analyze -f en.cfg | grep -c 'world world NN 1'
