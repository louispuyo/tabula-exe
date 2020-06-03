import sys
from tabula import errors
from tabula.io import read_pdf, convert_into, convert_into_by_batch
import csv
from os import getenv
import os

import pandas as pd
# FILES



#file = getenv('file')
file = sys.argv[1] 




def extract():
    path = os.path.dirname(__file__)
    filename = os.path.basename(file)
    foldername = os.path.basename(os.path.dirname(file))
    print(f"{path}/temp/{foldername}")
    if not os.path.exists(f'{path}/temp/{foldername}'):
        try:
            os.mkdir(f'{path}/temp/{foldername}')
        except OSError:
            print ("Creation of the directory %s failed" % foldername)
        else:
            print ("Successfully created the directory %s" % foldername)





    # Use splitext() to get filename and extension separately.
    (File, ext) = os.path.splitext(filename)
    progress=open(f"{path}/temp/{foldername}/progress.txt", "a+")
    try:
        print(file)
        convert_into(file, f'{path}/temp/{foldername}/{File}.csv',output_format='csv', pages='all')    
        #data = pd.read_csv(f'{path}/temp/{foldername}/{File}.csv', header=None)
    except:
        with open(f"{path}/temp/{foldername}/progress.txt", "a") as myfile:
            myfile.write(f"{File}=2,")
        print("C EST LA MERDE!", f"{path}/temp/{foldername}/{File}.csv")
    else:
        with open(f"{path}/temp/{foldername}/progress.txt", "a") as myfile:
            myfile.write(f"{File}=1,")
    

extract()
