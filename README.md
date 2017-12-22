# print At HPI

Print your documents at the Hasso-Platter-Institute in Potsdam.

This service providas a web interface to print documents.

The minimal viable prduct works as follows:

1. The user opens a web interface
2. The user selects a PDF file, HPI username and password
3. The user submits (HTTP POST) the file to the server
4. The server sends this file via email using the user's email address to `Mobile Print HPI <mobileprint@hpi.uni-potsdam.de>`

Hosting:
- https
- docker + automated build

Possible extensions:

- TXT, DOCX, DOC, SVG, HTML, JPEG, PNG, ...
- simple curl interface (POST + BASIC)
- multiple files upload

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


[py]: https://www.python.org/
