# CoffeeHouse API Wrapper for Python

This is a very simple API Wrapper for the CoffeeHouse API. Using
This Library only supports the V1IVA2.0 API which is based from
this [Documentation](https://gist.github.com/Netkas/e8977b26f482ca40911a949df7dd286f)

<p align="center">
  <img src="https://i.imgur.com/DjuRyhZ.jpg" alt="CoffeeHouse Python Example">
</p>


## Installation
```sh
pip install coffeehouse
```

or
```sh
python setup.py build
python setup.py install
```


## Lydia Example

```python
from coffeehouse.lydia import LydiaAI
from coffeehouse.api import API

# Create the CoffeeHouse API instance
coffeehouse_api = API("<API KEY>")

# Create Lydia instance
lydia = LydiaAI(coffeehouse_api)

# Create a new chat session (Like a conversation)
session = lydia.create_session()
print("Session ID: {0}".format(session.id))
print("Session Available: {0}".format(str(session.available)))
print("Session Language: {0}".format(str(session.language)))
print("Session Expires: {0}".format(str(session.expires)))

# Talk to the bot!
while True:
    output = session.think_thought(input("Input: "))
    print("Output: {0}".format(output))
```
