# Artifacts Python Client

## Introduction

I've created a python client for playing the mmo.   A minimum of 3.10 is required as we use builtin types for vars in this project.

## How to use

* `python3 -m venv venv; source venv/bin/activate`
* Re-name `credentials.temp.py` to `credentials.py` and add your bearer token in there
* Set your `PYTHONPATH` to the directory of the client in a `.env` folder (or you can create a wheel)
* `pip3 install -r requirements.txt`

You can now start using the modules 

```python
from python_artifacts_mmo_client.character_client import CharacterClient
from python_artifacts_mmo_client.game_master_client import GMClient

character_client = CharacterClient()
gm_client = GMClient()
```

Please feel free to view the methods in the classes to understand what they do, they are all doc stringed
and have reasonable names that make it easy to understand.

## Future work
I will be working on a terminal script that will play the game in the termina, it'll be text based first and over time do ASCII art. 

I will also work on trying to automate doing operations such as monster battling, material farming etc




