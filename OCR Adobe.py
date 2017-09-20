from win32com.client import Dispatch
from win32com.client.dynamic import ERRORS_BAD_CONTEXT

import winerror
import os
from bs4 import BeautifulSoup as bs
import xml.etree.cElementTree as ET

ROOT_INPUT_PATH = None
ROOT_OUTPUT_PATH = None
INPUT_FILE_EXTENSION = ".pdf"
OUTPUT_FILE_EXTENSION = ".xml"

global ERRORS_BAD_CONTEXT
ERRORS_BAD_CONTEXT.append(winerror.E_NOTIMPL)

def acrobat_extract_text(f_path, f_path_out, f_basename, f_ext):
    avDoc = Dispatch("AcroExch.AVDoc") # Connect to Adobe Acrobat

    # Open the input file (as a pdf)
    ret = avDoc.Open(f_path, f_path)
    assert(ret) # FIXME: Documentation says "-1 if the file was opened successfully, 0 otherwise", but this is a bool in practise?

    pdDoc = avDoc.GetPDDoc()

    dst = os.path.join(f_path_out, ''.join((f_basename, f_ext)))

    # Adobe documentation says "For that reason, you must rely on the documentation to know what functionality is available through the JSObject interface. For details, see the JavaScript for Acrobat API Reference"
    jsObject = pdDoc.GetJSObject()

    # Here you can save as many other types by using, for instance: "com.adobe.acrobat.xml"
    jsObject.SaveAs(dst, "com.adobe.acrobat.spreadsheet")

    pdDoc.Close()
    avDoc.Close(True) # We want this to close Acrobat, as otherwise Acrobat is going to refuse processing any further files after a certain threshold of open files are reached (for example 50 PDFs)
    del pdDoc

mydir = "H:/Projects/OCR/"
fbase = "II_StateAdvisoryForumState_AL_2016"
fname = "H:/Projects/OCR/II_StateAdvisoryForumState_AL_2016.pdf"

acrobat_extract_text(fname,mydir,fbase,OUTPUT_FILE_EXTENSION)

tree = ET.parse(os.path.join(mydir, ''.join((fbase, ".xml"))))

tree.getroot()

xmlstr = ET.tostring(tree.getroot(), encoding='utf8',method='xml')

print(xmlstr)
pretty = bs(xmlstr)
prettyxml = bs(str(pretty),"lxml-xml")

print(prettyxml.prettify())

with open("XML Output.txt","w") as textfile:
    textfile.write(str(prettyxml.prettify().encode("utf-8")))

