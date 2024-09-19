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
I'm currently working on the Terminal client, I'll also be working on a way to regularly update data behind the scenes such as maps etc and also downloading a cache of information to reduce loading times when doing calculations on things such as resources and monsters.




