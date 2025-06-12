from html2image import Html2Image
from PIL import Image

try:
   hti.screenshot(html_file=home.html)

finally:
   image1 = Image.open(r'C:\users\administrator\pictures\test.png')
   im1 = image1.convert('RGB')
   im1.save(r'C:\users\administrator\documents\newpdf.pdf')