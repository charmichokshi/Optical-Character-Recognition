# Optical-Character-Recognition
Detecting boxes and extract them one by one accurately for all PDFs of invoice to extract text within it like consignee and shipper name &amp; address.

Following is the algorithm:
- Convert PDF to PNG
- Apply morphological operations. I have defined two kernels. 1) Kernel to detect horizontal lines. 2) Kernel to detect vertical lines.
- Add the output of this two images which will detect all the boxes
- Crop all boxes which have height and width in a specific range and apply OCR on them to detect text

Naming convention:
- input: should have the input PDFs
- outputPNG: it will store PNG with respect to every PDF file
- Cropped: contains cropped images after applying morphological operations and text file generated after applying OCR
