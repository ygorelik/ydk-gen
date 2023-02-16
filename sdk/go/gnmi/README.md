## YDK Go gNMI Service Installation

### gNMI Requirements

In order to enable YDK support for gNMI protocol, which is optional, the following third party software must be installed prior to gNMI YDK component installation.

#### Install protobuf and protoc

```
    wget https://github.com/google/protobuf/releases/download/v3.5.0/protobuf-cpp-3.5.0.zip
    unzip protobuf-cpp-3.5.0.zip
    cd protobuf-3.5.0
    ./configure
    make
    sudo make install
    sudo ldconfig
```

#### Install gRPC

```
    git clone -b v1.9.1 https://github.com/grpc/grpc
    cd grpc
    git submodule update --init
    make
    sudo make install
    sudo ldconfig
    cd -
```

### gNMI package installation

For gNMI Go package installation, which is optional, perform these steps.

```
$ cd /your-path-to-ydk-gen
$ python3 generate.py -i --service profiles/services/gnmi-0.4.0.json --go
```

#### Runtime environment

There is an open issue with gRPC on Centos/Fedora, which requires an extra step before running any YDK gNMI application. 
See this issue on [GRPC GitHub](https://github.com/grpc/grpc/issues/10942#issuecomment-312565041) for details. 
As a workaround, the YDK based application runtime environment must include setting of `LD_LIBRARY_PATH` variable:

```
    export LD_LIBRARY_PATH=/usr/local/lib:/usr/local/lib64:/usr/lib64:$LD_LIBRARY_PATH
```
