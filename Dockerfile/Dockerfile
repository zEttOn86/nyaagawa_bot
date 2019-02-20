FROM nvidia/cuda:9.2-cudnn7-devel
# userの追加
RUN groupadd -g 1001 developer && \
    useradd -g developer -u 1001 -G sudo -m -s /bin/bash penguin && \
    echo "penguin:piyopiyo" | chpasswd && \
    echo "penguin ALL=(ALL) ALL" >> /etc/sudoers

USER penguin
WORKDIR /home/penguin/

# https://towardsdatascience.com/docker-for-data-science-9c0ce73e8263
RUN wget https://repo.continuum.io/archive/Anaconda3-4.2.0-Linux-x86_64.sh && \
    bash Anaconda3-4.2.0-Linux-x86_64.sh -b && \
    rm Anaconda3-4.2.0-Linux-x86_64.sh

# Set PATH to conda
ENV PATH /home/penguin/anaconda3/bin:$PATH

# Update pip and anaconda packages
RUN conda update conda && \
    conda update --all && \
    pip install --upgrade pip && \
    pip install --no-cache-dir \
        slackbot \
        pya3rt \
        python-dotenv
