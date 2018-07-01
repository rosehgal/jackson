# J<sub>ack</sub>SON
<p align="center">
<img src="./jackson.png" height="300px"/>
</p>  

Have you ever used JSON as your config? Have you keep secrets in config as plain text, that you dont want to? Then this is the right tool for you.  
**J<sub>ack</sub>SON** is the simple and flexible file extension of JSON file types written in `python` (in less than 50 lines of code), this extension allows the users to keep their secrets in environment variables and pass the reference to those environment variables into the JSON file(jackson). The secrets in the environment variables will be read securely in to the in memory dict.

The problem that it solves:  
* Retrive secrest from env variables.
* Retrive secrets from remote/servers(HSMs).

### How to J<sub>ack</sub>SON
J<sub>ack</sub>SON is exported as python package. You can install it via `pip`.  
`pip install --user `
```bash
export foo=10
export bar=100
```
Example J<sub>ack</sub>SON config file.  
```json
{
    "_comment1": "Value from foo env variable",
    "key1": "env.foo",
    "_comment2": "Value from bar env variable",
    "key2": "env.bar",
    "_comment3": "Value from python module",
    "key3": "!a.b",
    "_comment4": "key/value pair similar to json",
    "key4": "value4"
}
```
Inside the code.
```python3
import jackson
import json    # For converting JackSON --> JSON
d = json.load(jackson.File.open("./config.jackson"))
print(d)
```
And this is how it looks.
```bash
{
    'key3': 'reached',
    'key2': '100',
    'key1': '10',
    'key4': 'value4',
    '_comment4': 'key/value pair similar to json',
    '_comment3': 'Value from python module',
    '_comment2': 'Value from bar env variable',
    '_comment1': 'Value from foo env variable'
}
```
