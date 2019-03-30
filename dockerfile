FROM centos
LABEL maintainer=hujingguangsa@gmail.com
ARG Download_Url=https://www.python.org/ftp/python/3.7.3/Python-3.7.3.tgz
ARG setup_tools_url=https://files.pythonhosted.org/packages/c2/f7/c7b501b783e5a74cf1768bc174ee4fb0a8a6ee5af6afa92274ff964703e0/setuptools-40.8.0.zip
ARG pip_url=https://files.pythonhosted.org/packages/36/fa/51ca4d57392e2f69397cd6e5af23da2a8d37884a605f9e3f2d3bfdc48397/pip-19.0.3.tar.gz

ARG Py_Lib="tornado==v5.0"

WORKDIR /opt

RUN yum install epel-release -y && yum clean all && yum makecache &>/dev/null && \
    yum install wget gcc openssl-devel openssl make libffi-devel  -y &>/dev/null && \
    wget ${Download_Url} && \
    tar -zxf Python-3.7.3.tgz && cd Python-3.7.3 && ./configure --prefix=/usr/local/python3.7 && \
    make && make install && cd / && rm -rf /opt/* && yum remove  gcc make -y


RUN  yum install unzip -y &>/dev/null && wget ${setup_tools_url} && \
     unzip setuptools-40.8.0.zip && cd setuptools-40.8.0 && \
     /usr/local/python3.7/bin/python3 setup.py install && \
     yum remove unzip -y && rm -rf ./*

RUN wget ${pip_url} && tar -xzf pip-19.0.3.tar.gz && cd pip-19.0.3 && \
    /usr/local/python3.7/bin/python3 setup.py install &&  rm -rf ./* 

RUN /usr/local/python3.7/bin/pip install tornado==v5.0

RUN mv /usr/bin/python /usr/bin/python.bak && ln -s /usr/local/python3.7/bin/python3 /usr/bin/python && \
    sed -i 's/python/python2.6/g'  /usr/bin/yum

ADD ./alert.py ./alert.py

RUN chmod +x ./alert.py

CMD ['./alert.py']

    

