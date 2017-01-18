# Download Instructions
1. Go TO https://github.com/bio-boris/parse_pdf
2. Click Download and Download the Zip
3. Save as, open and extract the folder to C:/

# Install Python
* https://www.python.org/downloads/release/python-2713/
* Choose the Windows MSI installer , download and install

(Make sure Python is added to Path,
 the checkbox should be automatically
 checked but you can take a look and make sure)

# Install VC Python
* http://aka.ms/vcpython27

# Install LXML
Open CMD window
    cd C:\parse_pdf-master
    pip install wheel
    pip install lxml-3.6.4-cp27-cp27m-win32.whl

# Install required libraries
    pip install pypdf
    pip install pypdf2
    pip install lxml
    pip install pdfquery
    pip install reportlab

# Run the GUI.py , open with C:/Python27/python.exe

* Select PDF, watermark it
* The PDF will be generated in the same directory as the PDF you selected

