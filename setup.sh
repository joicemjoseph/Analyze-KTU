#!/bin/bash
error() {
      printf '\E[31m'; echo "$@"; printf '\E[0m'
}
# Check if the user is root
if [ $EUID -ne 0 ]; then
    error "This script should not be run using sudo or as the root user"
    exit 1
fi
apt-get install git mysql-server mysql-client python python-pip vim
pip install --upgrade pip
pip install virtualenv virtualenvwrapper
exit 0
