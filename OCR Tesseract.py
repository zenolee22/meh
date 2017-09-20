from PIL import Image as PI
import pytesseract
from wand.image import Image
from pyocr import pyocr
from pyocr import builders
import io
import pdfminer

#image_file = "H:/Projects/OCR/transforming_into_an_analytics_driven_insurance_carrier.pdf"

image_pdf = Image(filename="H:/Projects/OCR/II_StateAdvisoryForumState_AL_2016.pdf", resolution=400)
image_jpeg = image_pdf.convert('jpeg')

req_image = []
final_text = []

for img in image_jpeg.sequence:
    img_page = Image(image=img)
    req_image.append(img_page.make_blob('jpeg'))

tool = pyocr.get_available_tools()[0]
#lang = tool.get_available_languages()[1]

for img in req_image:
    txt = tool.image_to_string(
        PI.open(io.BytesIO(img)),
#        lang=lang,
        builder=builders.TextBuilder()
    )
    final_text.append(txt)

print(final_text[1])

file = open("output.txt","w",encoding='utf-8')

for item in final_text:
    file.write(str(item))

#pytesseract.image_to_string(PIL.Image.open)
