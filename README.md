# postalCodeToCensus
Functions for handling Statistics Canada's Postal Code Conversion File.

This script provides functions for converting postal codes into census tracts, dissemination areas, or dissemination block codes or latitude/longitude pairs. The Reference Guide can be found [here](http://publications.gc.ca/collections/collection_2017/statcan/92-0153/92-153-g2011005-eng.pdf). The conversion files can be accessed easily by UBC members from the UBC Abacus Dataverse site [here](http://dvn.library.ubc.ca/dvn/dv/ABACUSLD/faces/study/StudyPage.xhtml;jsessionid=c0a175128c18aade128b0c0cb225?studyId=4054&tab=files). Make sure the conversion file is in the same directory you are using to run this script.

This code is written to be compliant with the 2011 Reference Guide and datafile. For Vancouver, make sure to download "pccf59_may11_fccp59.zip". 

To run (make sure you have Python 3 installed):

`python postalCodeToCensus.py`

Then enter 'DA' to convert to dissemination area, 'DBC' to convert to dissemination block code or 'LATLON' to convert to latitude/longitude pair. 

Then enter the full file path for your .CSV file containing postal codes to be converted. The file should have the following format:

| postalCode |
|---|
|V6T1Z1|
|...|

For processing large numbers of postal codes, you should optimize the code.
