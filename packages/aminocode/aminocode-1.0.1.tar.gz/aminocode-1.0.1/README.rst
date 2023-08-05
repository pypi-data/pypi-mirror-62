PyInstaller Overview
====================
The aminocode library can be used to encode texts written in natural language in a format based on amino acids. With coding is enable the application of various bioinformatics tools in text mining.

Stand alone tools based on library are available at link <https://sourceforge.net/projects/aminocode>.

Installation
------------
To install aminocode through `pip`::

      pip install aminocode


Tested Platforms
----------------
- Python:

 - 3.7.4

- Windows (64bits):

 - 10

- Ubuntu (64bits)

 - 18.04.1 LTS

Required external libraries
---------------------------
- numpy
- unidecode
- biopython

Functions
---------------
- :code:`encodetext(text,detailing='')`

 - **text:** natural language text string to be encoded;
 - **detailing:** details in coding. 'd' for details in digits. 'p' for details on the punctuation. 'dp' or 'pd' for both;
 - **output:** encode string.

- :code:`decodetext(text,detailing='')`

 - **text:** text string encoded using the encodefile function to be decode;
 - **detailing:** details used in the text to be decoded. 'd' for details in digits. 'p' for details on the punctuation. 'dp' or 'pd' for both;
 - **output:** decode string.

- :code:`encodefile(input_file_name,output_file_name=None,detailing='',header_format='number+originaltext',verbose=False)`

 - **input_file_name:** text file name or _io.TextIOWrapper variable. It can also be used the format that is imported by the Bio.SeqIO library of Biopython, in which case the function will automatically extract the headers to do the encoding;
 - **output_file_name:** the name for the output file. If not defined, the result will only be returned as a variable;
 - **detailing:** same as in the encodetext function;
 - **header_format:** format for the headers of the generated FASTA. It can be 'number+originaltext', 'number' or 'originaltext'. 'number' is a count of the lines in the input file. Blank lines are considered in the count, but are not added to the FASTA file. 'originaltext' is the input text itself;
 - **verbose:** if True displays progress;
 - **output:** FASTA variable in Biopython format. If defined output_file_name a file will be saved.


- :code:`decodefile(input_file_name,output_file_name=None,detailing='',verbose=False)`

 - **input_file_name:** file name or variable in the format used by Biopython's Bio.SeqIO library
 - **output_file_name:** the name for the output file. If not defined, the result will only be returned as a variable;
 - **detailing:** same as in the decodetext function;
 - **verbose:** if True displays progress;
 - **output:** string list. If defined output_file_name a file will be saved.