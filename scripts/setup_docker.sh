#!/bin/bash

# Dockerのインストール
sudo yum install -y docker
sudo service docker start

# dockerをsudoなしで使えるようにする
sudo groupadd docker
sudo usermod -aG docker $USER
