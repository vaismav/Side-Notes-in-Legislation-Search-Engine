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

#lunching the server
echo "Starting server"
export FLASK_APP=server.py
flask run
