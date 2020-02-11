# nlp-proj1
Project 1: The Golden Globes

Group Members: Jiapeng Liu, Matthew Walsh, Ka Wong

GitHub repository: https://github.com/liujjpp/nlp-proj1

## Directions for setup:

### Use virtualenv for handling dependencies

### Requirements
* Python 3
* Pip 3

### Installation
```bash
$ pip3 install virtualenv
```

```bash
$ virtualenv -p python3 venv
```

```bash
$ source venv/bin/activate
```

```bash
$ pip install -r requirements.txt
```

```bash
$ python3 -m spacy download en_core_web_sm
```

### Get Required Files (json) for autograder from https://github.com/milara/gg-project-master
* gg2013answers.json
* gg2015answers.json

### Get Required Files (json) for api
* [gg2013.json](https://canvas.northwestern.edu/courses/105385/files/8069826/download)
* [gg2015.json](https://canvas.northwestern.edu/courses/105385/files/8069845/download)
* [gg2020.json](https://canvas.northwestern.edu/courses/105385/files/8019442/download)

### Run
For grading:

```bash
$ python autograder.py <year>
```

To output human-readable format results, run:

```bash
$ python gg_api.py
```

Then input year, for example:

```bash
Which year: 2013
```

Sometimes IMDb queries can cause errors. Just run it again if one of the following exceptions occurs:

```bash
imdb._exceptions.IMDbDataAccessError: {'errcode': 54, 'errmsg': 'Connection reset by peer', 'url': 'https://www.imdb.com/find?q=xxx&s=nm', 'proxy': '', 'exception type': 'IOError', 'original exception': ConnectionResetError(54, 'Connection reset by peer')}
```

```bash
imdb._exceptions.IMDbDataAccessError: {'errcode': None, 'errmsg': 'None', 'url': 'https://www.imdb.com/find?q=xxx&s=nm', 'proxy': '', 'exception type': 'IOError', 'original exception': URLError(timeout('_ssl.c:1039: The handshake operation timed out'))}
```