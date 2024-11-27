FROM ubuntu:jammy

MAINTAINER http://ydk.io

COPY . /root/ydk-gen

RUN echo 'Installing dependencies'

WORKDIR /root/ydk-gen

RUN /bin/bash -c './test/dependencies_ubuntu.sh && ./test/dependencies_linux_gnmi.sh'

RUN pip3 install -r requirements.txt
RUN pip3 install 3d_party/python/pyang-2.6.1.1.tar.gz

RUN python3 generate.py -i --core --cpp
RUN python3 generate.py -i --service profiles/services/gnmi-0.4.0.json --cpp

RUN python3 generate.py -i --core
RUN python3 generate.py -i --service profiles/services/gnmi-0.4.0.json
RUN pip3 install ydk-models-openconfig

RUN ./install_ydk.sh --go --core --service gnmi
RUN source .env

RUN ln -s /usr/bin/python3 /usr/bin/python
