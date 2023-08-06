# Keytime
### install keytime
Linux/MacOS: ```pip3 install keytime``` or ```python3 -m install keytime```

Windows: ```pip install keytime``` or ```py -m pip install keytime```

### run keytime
```
$ python3
>>> from keytime.keytime import run
>>> run()
```

keytime will now read your keyboard input. By pressing 'Escape', keytime will stop reading your input and display
collected data as a table. Keytime also writes a ```.csv```-file named 'output.csv'.