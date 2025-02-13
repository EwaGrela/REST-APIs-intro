# How to create the virtual environments

For each demo you will need a Python 3 virtual environment that contains the Python packages that the demos depend on. This requires Python virtual environment support (`venv`). You will also need the Python package manager `pip` to install those packages (other Python package managers are available).

The packages required are listed in the requirements files, which by convention are named '\<prefix\>requirements.txt'. They are stored in the REST_APIS directory this repository.

In Ubuntu you can satisfy these dependencies using the operating system's package manager `apt` as follows (other operating systems and OS package managers are available):


```
$ sudo apt-get install python3-dev
$ sudo apt-get install python3-pip
```

Once venv and pip are installed, `cd` to the root of the repository and run the following commands:


```
# for flask
$ python3 -m venv flask_venv
$ source flask_venv/bin/activate
$ python3 -m pip install -r REST_APIs/flask_requirements.txt
```



```
# for fast API
$ python3 -m venv fast_venv
$ source fast_venv/bin/activate
$ python3 -m pip install -r REST_APIs/fast_requirements.txt
```


Running these commands loads the correct Python virtual environment for the respective demos into the current terminal, so you can start the server without needing to load them. 

To unload the virtual environment `cd` to the root of the repository and type:

```
$ deactivate
```

To reload it later `cd` to the root of the repository and type:

```
# flask
$ source flask_venv/bin/activate
```

```
# fast API
$ source fast_venv/bin/activate
```
