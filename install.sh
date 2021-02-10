#!/bin/bash

while true; do
    read -p "Are you currently running a virtual environment?(Y/n)" yn
    case $yn in
        [Yy]* )  break;;
        [Nn]* ) python3 -m venv venv; source venv/bin/activate; break;;
        * ) echo "Please answer yes or no.";;
    esac
done

#installing fasttext
git clone https://github.com/facebookresearch/fastText.git

cd fastText

pip install . 

#install requirements
pip3 install -r requirements.txt

#building the client

#lunching the server
