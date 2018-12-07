# Optical-Character-Recognition
Detecting boxes and extract them one by one accurately for all PDFs of invoice to extract text within it like consignee and shipper name & address.

Algorithm:
- Convert PDF to PNG
- Apply morphological operations. I have defined two kernels. 
  1) Kernel to detect horizontal lines. 
  2) Kernel to detect vertical lines.
- Add the output of this two images which will detect all the boxes
- Crop all boxes which have height and width in a specific range and apply OCR on them to detect text

Naming convention:
- input: should have the input PDFs
- outputPNG: it will store PNG with respect to every PDF file
- Cropped: contains cropped images after applying morphological operations and text file generated after applying OCR

**Input:**
![Input](https://github.com/charmichokshi/Optical-Character-Recognition/blob/master/outputPNG/117568-MAWB014-45783043_333320171013030906-Page(1).png)

**Cropped boxes**
![a](https://github.com/charmichokshi/Optical-Character-Recognition/blob/master/Cropped/117568-MAWB014-45783043_333320171013030906-Page(1)_1.png)
![a](https://github.com/charmichokshi/Optical-Character-Recognition/blob/master/Cropped/117568-MAWB014-45783043_333320171013030906-Page(1)_2.png)

**Extracted Text**
M/S JEENA & COMPANY

JEENA HOUSE PLOT 170 OM NAGAR

OFF PIPELINE ROAD SAGAR

ANDHERI E MUMBAI 400 099

INDIA

MR. SHIRISH BAADKAR 91 22 44222111

TRANSGROUP INTERNATIONAL

140 Eastern Ave

Chelsea, MA 02150

(617) 889-5089
