# Side-Notes-in-Legislation-Search-Engine

* [General info](#general-info)
* [Screenshots](#screenshots)
* [Technologies](#technologies)
* [Requirments](#Requirments)
* [How to build](#how-to-build)
* [How to run](#how-to-run)
* [How it works](#how-it-works)
* [Authors](#Authors)




## General info
This project is part of "Digital Humanities for CS" course.
It is a search engine of sections by side notes in laws in Israel, built to help lawyers to write laws.

## Screenshots

![main web page](https://github.com/vaismav/Side-Notes-in-Legislation-Search-Engine/blob/main/screenshot.jpeg)

## Technologies
* Server - Python (3.7) flask
* Client - React
* Words Trainning Model - [fastText]( https://fasttext.cc/docs/en/unsupervised-tutorial.html )

## Requirments
* python3 (or above)
* pip (sudo apt-get install python3-pip)
* npm

## How to build
* On terminal run:

```bash
git clone https://github.com/vaismav/Side-Notes-in-Legislation-Search-Engine.git
cd Side-Notes-in-Legislation-Search-Engine
./install.sh
```

You will have to choose at the beginning if to run the installation in venv.
(if you choose so, venv dir will create automatically and all dependencies will be install there)
And at the end. wheter you want the fast-and-limited installation or to install all features:
* Fast and Limited  : quickly deploy the neccesary files to support minimal search in the given laws xmls.
* All features      : Take times, creates a trained model of fastText and support search queries of terms which aren't found in the side-note collections     

In the end of the installation process the server will be launch automatically on default PORT

## How to run
* After installation you can run the server explictly with
```bash
export FLASK_APP=server.py
flask run
```
* Or you can use the start script
```bash
./start
```

## How it works
* All xml(law) files extracted from /data/LawRepoWiki.zip to /data/xmls.
* A JSON fill of all sections created.
* FastText model ( https://fasttext.cc/docs/en/unsupervised-tutorial.html ) run on all the side notes in the JSON.
* A flask application created from 'server.py', and serve the client files as static files from client/build directory.
* The user ask for a side note x, the server search for a side notes that are closest to x in in the trained model data and offers them to te user.
* The user pick a side note y and get a list of sections witch y is their side note.
* If the user wishs to see more results, there is a BIG GREEN BUTTON in the bottom of the results list to feth more results

## Authors
* Yarin Kagal       -   [Git](https://github.com/yarink3) | [LinkedIn](https://www.linkedin.com/in/yarin-kagal-358248173/)
* Avishai Vaisman   -   [Git](https://github.com/vaismav) | [LinkedIn](https://www.linkedin.com/in/avishai-vaisman)
* Contact us for help, consulting, offer us a job, or send us donations ;)

<!-- ### Requirements
To run this project, Python3, pip3 & pip are requierd -->