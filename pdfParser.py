from tabula.io import read_pdf 
from os import getenv
# FILES
file = getenv('file')


# FUNCTIONS

def pagecounter():
    document = read_pdf(f"{file}", pages='all', multiple_tables=True)
    pages_number = len(document)
    print(pages_number)
    counter = str(document).find('Libellés  N° Fact Montants Récupérable')
    print(counter)

    return pages_number

def getDimension():

    # LOCAL VARIABLES
    pages_container = []
    
    pages_number = 7
    assert pages_number != 0
    for page in range(pages_number):


        df = read_pdf(f"{file}", output_format='json', pandas_options={
                                'header': None}, multiple_tables=True, pages=page)
        pages_container.append(df)
        
    return pages_container
    

def extract():
    # LOCAL VARIABLE
    PDFcontainer = []

    for page in range(6):

        df = read_pdf(f"{file}", output_format='json', pandas_options={
                                'header': None}, multiple_tables=True, pages=page)
            
        top = df[0]['top']
        bottom = df[0]['height']+top
        left = df[0]['left']
        right = df[0]['width']+left
        print('\n DIMENSION')
        print(top, right, bottom, left)
        print('\n-------------------------------------------------------------')
        df = read_pdf(f"{file}", pandas_options={
                            'header': None}, multiple_tables=True, area=(top, left, bottom, right), pages=page)
        print(df)
        PDFcontainer.append(df)

    return PDFcontainer



# RUN
extract()