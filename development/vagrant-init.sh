#!/bin/bash

# set up our environment
locale-gen en_US.UTF-8
locale-gen de_DE.UTF-8

export LANGUAGE=en_US.UTF-8
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

# update repository cache
apt-get -q -y update

# basic packages
apt-get install -q -y build-essential python python-dev python-setuptools python-pip python-mysqldb git zsh screen tmux vim

# certain module dependencies
apt-get install -q -y libjpeg62-dev zlib1g-dev libfreetype6-dev liblcms1-dev libncurses5-dev libgif4 giflib-tools libgif-dev

# mysql
export DEBIAN_FRONTEND=noninteractive
apt-get install -q -y mysql-server mysql-client
mysqladmin create c4sh

# virtualenv global setup
if ! command -v pip; then
    easy_install -U pip
fi
if [[ ! -f /usr/local/bin/virtualenv ]]; then
    easy_install virtualenv virtualenvwrapper virtualenv-clone
fi

# install our Python dependencies
pip install -r /vagrant/deployment/requirements.txt

# symlink our source code to vagrant homedir
ln -s /vagrant/c4sh /home/vagrant/

# copy misc. files
cp /vagrant/development/files/motd /etc/motd.tail

echo
echo
echo "Your c4sh development instance is ready, use 'vagrant ssh' to connect."