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


