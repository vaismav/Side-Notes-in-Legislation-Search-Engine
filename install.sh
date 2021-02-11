#!/bin/bash

while true; do
    read -p "Do you wish to install the dependencies in virtual evironment?(Y/n) " yn
    case $yn in
        [Yy]* ) python3 -m venv venv; source venv/bin/activate; break;;
        [Nn]* )  break;;
        * ) echo "Please answer yes or no.";;
    esac
done

#installing fasttext
git clone https://github.com/facebookresearch/fastText.git
cd fastText
pip install . 
cd ../

#deleting fastext installtion files

rm -rf fastText

#install requirements
echo "Installing Py dependencies.."
pip3 install -r requirements.txt

#building the client
echo "Building Client..."
cd client
npm install
npm run build
cd ../

while true; do
    read -p "Do you want to lunch the fast-limited install INSTEAD OF the long install of all features?(Y/n) " yn
    case $yn in
        [Yy]* ) python3 install.py -f; break;;
        [Nn]* ) python3 install.py -a; break;;
        * ) echo "Please answer yes or no.";;
    esac
done

#lunching the server
echo "Starting server"
export FLASK_APP=server.py
flask run
