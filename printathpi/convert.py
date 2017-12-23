import os
from tempfile import NamedTemporaryFile
import subprocess

def pdf2pdf(file_format, content):
    """Convert a pdf to a pdf file."""
    return content

def svg2pdf(file_format, content):
    """Convert an svg file to a pdf file.
    
    This uses rsvg-convert.
    """
    with NamedTemporaryFile() as input_file:
        input_file.write(content)
        input_file.flush()
        cp = subprocess.run(["rsvg-convert", "-f", "pdf", input_file.name],
                            stdout=subprocess.PIPE, check=True)
        return cp.stdout

def png2pdf(file_format, content):
    """Convert a png or jpeg image"""
    with NamedTemporaryFile(suffix="." + file_format) as input_file:
        input_file.write(content)
        input_file.flush()
        with NamedTemporaryFile("rb", suffix=".pdf") as output_file:
            print("png2pdf", input_file.name, output_file.name)
            cp = subprocess.run(["convert", input_file.name, output_file.name], check=True)
            return output_file.read()

jpg2pdf = png2pdf

conversions = {"pdf":  pdf2pdf,
               "svg":  svg2pdf,
               "jpg":  jpg2pdf,
               "jpeg": jpg2pdf,
               "png":  png2pdf,
               }

def convert(filename, content):
    """Convert the file content to pdf.
    
    Files which cannot be converted will not be converted.
    The Uniflow system sends a message if files cannot be printed,
    so the user will know.
    """
    file_format = os.path.splitext(filename)[1][1:].lower()
    convert = conversions.get(file_format, pdf2pdf)
    print("convert {} with {}".format(filename, convert.__name__))
    return convert(file_format, content)
    

