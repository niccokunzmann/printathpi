import os
from tempfile import NamedTemporaryFile
import subprocess
import re

def pdf2pdf(file_format, content):
    """Convert a pdf to a pdf file."""
    return content
    
def png2pdf(file_format, content):
    """Convert a png or jpeg image"""
    with NamedTemporaryFile(suffix="." + file_format) as input_file:
        input_file.write(content)
        input_file.flush()
        with NamedTemporaryFile("rb", suffix=".pdf") as output_file:
            print("png2pdf", input_file.name, output_file.name)
            subprocess.check_call(["convert", input_file.name, output_file.name])
            return output_file.read()

jpg2pdf = png2pdf


def unoconv2pdf(file_format, content):
    """Convert a file to an pdf using unoconv.
    
    You can use 
    
        unoconv --show
    
    on the command line.
    """
    with NamedTemporaryFile(suffix="." + file_format) as input_file:
        input_file.write(content)
        input_file.flush()
        return subprocess.check_output(["unoconv", "-f", "pdf", "--stdout", input_file.name])
    

def get_unoconv_conversions():
    """get unoconv and all supported formats"""
    try:
        process = subprocess.Popen(["unoconv", "--show"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    except FileNotFoundError:
        # FileNotFoundError: [Errno 2] No such file or directory: 'unoconv'
        return {}
    if process.wait() != 0:
        return {}
    documentation = process.stdout.read().decode()
    format_list = re.findall(r"\s+([a-z0-9]+)\s+-\s", documentation)
    conversions = {}
    for format in format_list:
        conversions[format] = unoconv2pdf
    return conversions

conversions = get_unoconv_conversions()
conversions.update({
    "pdf":  pdf2pdf,
    "jpg":  jpg2pdf,
    "jpeg": lambda *args: conversions["jpg"](*args),
    "png":  png2pdf,
})

if subprocess.call(["which", "inkscape"]) == 0:
    def inscapesvg2pdf(file_format, content):
        """Convert an svg file to a pdf file.
        
        This uses inkscape.
        """
        with NamedTemporaryFile() as input_file:
            input_file.write(content)
            input_file.flush()
            with NamedTemporaryFile() as output_file:
                subprocess.check_call(["inkscape", "-z", "-f", input_file.name, "-A", output_file.name])
                return output_file.read()
    svg2pdf = conversions["svg"] = inscapesvg2pdf
elif subprocess.call(["which", "rsvg-convert"]) == 0:
    def rsvg2pdf(file_format, content):
        """Convert an svg file to a pdf file.
        
        This uses rsvg-convert.
        """
        with NamedTemporaryFile() as input_file:
            input_file.write(content)
            input_file.flush()
            return subprocess.check_output(["rsvg-convert", "-f", "pdf", input_file.name])
    svg2pdf = conversions["svg"] = rsvg2pdf

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
    
if __name__ == "__main__":
    print("Conversions: {}".format(", ".join(list(sorted(conversions.keys())))))

