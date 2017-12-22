# Print At HPI

[![Docker Build Status](https://img.shields.io/docker/build/niccokunzmann/printathpi.svg)](https://hub.docker.com/r/niccokunzmann/printathpi/builds/)

Print your documents at the Hasso-Platter-Institute in Potsdam. [**Try it out**][server]
This service providas a web interface to print documents.

The minimal viable product works as follows:

1. The user opens a web interface
2. The user selects a PDF file, HPI username and password
3. The user submits (HTTP POST) the file to the server
4. The server sends this file via email using the user's email address to `Mobile Print HPI <mobileprint@hpi.uni-potsdam.de>`

Hosting:
- https
- docker + automated build, deployment every night, bei Nicco zu Hause

Extensions:

- [X] JPEG, PNG, SVG
- [ ] TXT, DOCX, DOC, HTML, ...
- [ ] simple curl interface (POST + BASIC) for API usage
- [X] multiple files upload

Contribution
------------

If you think, this is a good idea, please feel free to contribute.
Please open an issue if the pull request is not just a small fixing of a bug.

Setup
-----

These commands are executed inside the repository directory.

1. Install [Python 3][py] and pip
   `sudo apt-get install python3 python3-pip`.
2. Install virtualenv  
   `python3 -m pip install virtualenv`
3. Create the virtual environment  
   `virtualenv -p python3 ENV`
4. Activate the virtual environment `ENV`  
   `source ENV/bin/activate`
5. Install the packages  
   `pip install -r requirements.txt`
6. Now, you can execute the server.  
   `python3 -m printathpi.app`

In case you want to run the server after setup,
you need to activate the virtual environment and start the server.

```
source ENV/bin/activate
python3 -m printathpi.app
```

The server should be rachable at port 8001 under http://localhost:8001/

Setup Conversions
-----------------

Different types of files can be converted.
These are the installation instructions for those.

- SVG  
  `sudo apt-get install librsvg2-bin`  
  Read more about this here: https://superuser.com/a/381128/164164
- JPG, JPEG, PNG  
  `sudo apt-get install ghostscript imagemagick`
  Read more about this here: http://dev-random.net/convert-multiple-jpg-or-png-to-pdf-in-linux/

The converter functions are in the convert.py file.
It is quite easy to write those: They take an input .

Docker
------

You can install docker.
Use this commands to build the image:

```
docker build --tag niccokunzmann/printathpi .
```

And run the image using this command:

```
docker run --rm -p8001:8001 niccokunzmann/printathpi
```

Now, you can visit http://localhost:8001/.

[py]: https://www.python.org/
[server]: https://printathpi.quelltext.eu

