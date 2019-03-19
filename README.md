# Print At HPI

[![Docker Build Status](https://img.shields.io/docker/build/niccokunzmann/printathpi.svg)](https://hub.docker.com/r/niccokunzmann/printathpi/builds/)

Print your documents at the Hasso-Platter-Institute in Potsdam. [**Try it out**][server]
This service provides a web interface to print documents.

The minimal viable product works as follows:

1. The user opens a web interface
2. The user selects a PDF file, HPI username and password
3. The user submits (HTTP POST) the file to the server
4. The server sends this file via email using the user's email address to `Mobile Print HPI <mobileprint@hpi.uni-potsdam.de>`

Hosting:
- https
- docker + automated build, deployment every night, bei Nicco zu Hause

For supported file formats, please see the [Conversions Section][conversions]

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

The server should be reachable at port 8001 under http://localhost:8001/

Setup Conversions
-----------------
[conversions]: #setup-conversions

Different types of files can be converted.
These are the installation instructions for those.

- SVG  
  - `sudo apt-get install librsvg2-bin`  
      Read more about this here: https://superuser.com/a/381128/164164
  - or `sudo apt-get install inkscape`  
      Read more about this here: https://superuser.com/a/506696/164164
- JPG, JPEG, PNG  
  `sudo apt-get install ghostscript imagemagick`  
  Read more about this here: http://dev-random.net/convert-multiple-jpg-or-png-to-pdf-in-linux/
- bib, bmp, csv, dbf, dif, doc, doc6, doc95, docbook, docx, docx7, emf, eps, fodg, fodp, fods, fodt, gif, html, jpg, latex, mediawiki, met, odd, odg, odp, ods, odt, ooxml, otg, otp, ots, ott, pbm, pct, pdb, pdf, pgm, png, pot, potm, ppm, pps, ppt, pptx, psw, pwp, pxl, ras, rtf, sda, sdc, sdc3, sdc4, sdd, sdd3, sdd4, sdw, sdw3, sdw4, slk, stc, std, sti, stw, svg, svm, swf, sxc, sxd, sxd3, sxd5, sxi, sxw, text, tiff, txt, uop, uos, uot, vor, vor3, vor4, vor5, wmf, wps, xhtml, xls, xls5, xls95, xlsx, xlt, xlt5, xlt95, xpm  
  `sudo apt-get install unoconv libreoffice`  
  Read more about this here: http://linuxsleuthing.blogspot.de/2012/01/unoconv-is-number-one.html

The converter functions are in the [convert.py][convert] file.
It is quite simple to write those: They take a file format like `"svg"` and the bytes of a
file as an input and return the bytes of the pdf file.

Docker
------

The [server][server] is hosted via Docker.
It is deployed daily at night.
You can develop the docker image.
Please be aware that the documentation comes first, so features
of the server MUST be documented here.

After you install Docker.
Use this command to build the image:

```
docker build --tag niccokunzmann/printathpi .
```

And run the image using this command:

```
docker run --rm -p8001:8001 niccokunzmann/printathpi
```

Now, you can visit http://localhost:8001/.

API
===

The API of this print service allows you to print documents for HPI students directly from
your website.

Form
----

You can submit multiple files as the `files[]` attribute of a form.
For this you can add the following text to your HTML document.

    <form enctype='multipart/form-data' method='POST' action='https://printathpi.quelltext.eu/print'> 
      <input type='file' name='files[]' multiple="multiple" />
      <button type='submit'>Submit</button>
    </form>
    
When the user presses the submit button, the document will be printed.

JavaScript
----------

You can embed a js file to include the print functionlity into your website:

    <script type="text/javascript" async="" src="https://printathpi.quelltext.eu/printathpi.js"></script>

Then, you can use the `printAtHPI()` function:

    printAtHPI({"filename.PDF": "... pdf content ..."}, username, password, onPrint, onError);

- `{"filename.PDF": "... pdf content ..."}`  
  Is a javascript object mapping file names to content.
- `username` and `password`  
  must be strings to authenticate or `null` to open the browser dialog.
- `onPrint`  
  is called with an event if the print is successful (Status 200).
  ```
  function onPrint(e) {
    alert(e.target.responseText);
  }
  ```
- `onError`  
  is called when the print did not succeed with an event.
  ```
  function onError(e) {
    if (e.target.status == 401) {
      alert("Wrong username or password.");
    } else {
      alert("Could not print.");
    }
  }
  ```

cUrl
----

You can use the command line utility curl to print files without installing any driver.
This counts for all files which can be converted.

```
curl -X POST                                          \
     -F 'files[]=@example_files/logo.svg'             \
     -u 'Johanna.Doe@student.hpi.de:JohannasPassword' \
     https://printathpi.quelltext.eu/print
```




[py]: https://www.python.org/
[server]: https://printathpi.quelltext.eu
[convert]: https://github.com/niccokunzmann/printathpi/blob/master/printathpi/convert.py


