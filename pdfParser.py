import sys
from tabula import errors
from tabula.io import read_pdf, convert_into, convert_into_by_batch
import csv
from os import getenv
import os
import re
import pandas as pd
from datetime import date
# FILES

#! file
#file = getenv('file')
try:
    file = sys.argv[1] 

except:
    file = "/home/snowden/Documents/expenses-pagesti-pdf/1120-2012.pdf"


# SECTION - LIST DES LIGNES qui casse les #!Couilles
#! -> 175
# -> l entete 



# RETURN A DF object
def clean_data_csv(F):
    Data = pd.read_csv(F, delimiter=',', header=None)
    next(Data, None)  # skip the headers
    container = []
    for j,i in enumerate(Data):
        if j == 1:
            container = container
        else:
            container+=i
    return container

# TODO => make a class DataPdfParserClass that take a file path and return a clean csv 
# class DataPdfParserClass(str)

def ParseData(file=file):

    # GENERAL VARIABLES
    Trigger = 0
    path = os.path.dirname(__file__)
    filename = os.path.basename(file)
    (File, ext) = os.path.splitext(filename)

    #TOOLS FUNCTION
    def listToString(s):  
        str1 = ""  
        for ele in s:  
            str1 += ele   
        
        return str1  
    
    def PositionSwitch(Trigger):
        tag_list = [regex_Amount,regex_Tva,regex_Recuperable,regex_Deduct]
        if Trigger != 1:
            for i in tag_list:
                while Trigger == 0:
                    break
        
        return 1

    def counter(file):
        count = 0
        with open(file, 'r') as f:
            for line in f:
                count += 1
        print("Total number of lines is:", count)
        return count

    def KeepSameSize(df_col):
        if len(df_col) == 0:
            df_col = 'N'
            return df_col
        else:
            df_col = df_col
            return df_col

    def formatdate(regex_Date):
        if len(regex_Date) < 2:
            return regex_Date
        else:
            regex_Date = f"{regex_Date[0]}/{regex_Date[1]}/{regex_Date[2]}"
        return regex_Date

    def vta_null(regex_Tva):
        return len(regex_Tva) == 0

    def Isempty(Row):
        return len(Row) == 0
        
    # DATAFRAMES
    data = pd.read_csv(file)
    df = pd.DataFrame(data, index=range(counter(file)), columns=['Date','Libellés','N° Fact','Montants','Récupérable','Déductible','T.V.A.'])
    df_T = df.transpose()
    df_Libelle = []
    df_Date = []
    df_Compte = []
    df_Four = []
    df_Bill = []
    df_Deduct = []
    df_Tva = []
    df_Amount = []
    df_Recup = []
    df_Conso = []

    # REPARTITION
    for index in df.index:
        regex_Date = re.findall(r"\d+\/\d+\/\d+", str(df['Date'][index]))
        # regex_bill = re.findall(r'dddddddd')
        regex_Compte = re.findall(r"Total compte.(\d{8})", str(df['Libellés'][index]))
        regex_Four = re.findall(r'^Four:.*', str(df['Libellés'][index]))
        regex_Amount = re.findall(r'\d+.\d{2}', str(df['Montants'][index]))
        regex_Tva = re.findall(r'\d+.\d{2}', str(df['T.V.A.'][index]))
        regex_Deduct = re.findall(r'\d+.\d{2}', str(df['Déductible'][index]))
        regex_Recuperable = re.findall(r'\d+.\d{2}', str(df['Récupérable'][index]))
        regex_Libel = re.findall(r'\D', str(df['Libellés'][index]))
        regex_bill = re.findall(r'\d+.d{2}', str(df['N° Fact'][index]))
        regex_Conso = re.findall(r'\d+m3|\d+kwh|\d+mwh', str(df['Libellés'][index]))


        if len(regex_Amount) == 0:
            df_Amount += KeepSameSize(regex_Amount)

            if vta_null(regex_Tva):
                regex_Tva = regex_bill
            
        elif '0000' == listToString(regex_Amount)[:4]:
            df_Compte += regex_Amount
            df_Amount += 'N'
        
        else:
            df_Amount += KeepSameSize(regex_Amount)
        

        Trigger = PositionSwitch(Trigger) 
        
        if Trigger > 0: 
            if KeepSameSize(regex_Recuperable) != 'N':
                regex_Tva = regex_Recuperable
                # print('///////////////////////////////')
            else:
                regex_Tva = regex_Deduct
                # print('//////////////////////////////////')
            

        df_Libelle += KeepSameSize(regex_bill)
        df_Deduct += KeepSameSize(regex_Deduct)
        df_Four += KeepSameSize(regex_Four)
        df_Date += KeepSameSize(regex_Date)
        df_Compte += KeepSameSize(regex_Compte)
        df_Bill +=  KeepSameSize(regex_bill)
        df_Tva += KeepSameSize(regex_Tva)
        df_Recup += KeepSameSize(regex_Recuperable) 
        df_Conso += KeepSameSize(regex_Conso)

    # print(f"{df_Four},\n----- END FOUR-----\n\n', {df_Date},\n----- END DATE-----\n\n', {df_Compte},\n----- END COMPTE -----\n\n', {df_Amount},\n-----END AMOUNT -----\n\n', {df_Tva} \n ------- END TVA -------- \n {df_Deduct}\n-----END DEDUCT ------------\n {df_Recup}")


    df['Date'] = df_Date
    df['Libellés'] = df_Conso 
    df['N° Fact'] = df_Compte
    df['Montants'] = df_Amount
    df['Récupérable'] = df_Tva
    df['Déductible'] = df_Four
    df['T.V.A.'] = df_Bill

    df.rename({'Libellés':'consumption','N° Fact':'bill_number','Montants':'amount','Récupérable':'vta','Déductible':'supplier','T.V.A.':'account'},inplace=True)
    for line in df.values:
        print(line)
    

    return df.to_csv(file, header=False)


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
    progress=open(f"{path}/temp/progress.txt", "a+")
    file_csv=f"{path}/temp/{foldername}/{File}.csv"

    try:
        print(file)
        convert_into(file, f'{path}/temp/{foldername}/{File}.csv',output_format='csv', pages='all')
        clean_data = clean_data_csv(F=file_csv)
        ParseData(file=f'{path}/temp/{foldername}/{File}.csv')
        
        # print('TOUS VA BIEN')
                 
    except:
        with open(f"{path}/temp/progress.txt", "a") as myfile:
            myfile.write(f"{File}=2,")
        print("C EST LA MERDE!", f"{path}/temp/{foldername}/{File}.csv")
    else:
        with open(f"{path}/temp/progress.txt", "a") as myfile:
            myfile.write(f"{File}=1,")
    
# FIXME 
# uncomment below
extract()


# TRASH ZONE


    #     if not Isempty(regex_Tva): 
    #         if not Condition_bt({"a":regex_Amount, "b":regex_Tva}):
    #             temp = regex_Amount
    #             regex_Amount = regex_Tva
    #             regex_Tva = temp
    #         else:
    #             df_Amount += regex_Amount
    #             df_Tva += regex_Tva
               
    #     else:
    #         df_Amount += regex_Amount
    #         df_Tva += regex_Tva
          

    #     if regex_Amount == '000':
    #         df_Compte += regex_Amount[0]
    #     else:
    #         print(f'missed the {index} value {regex_Amount} < {regex_Tva}')
    # #     print(df.loc[i])
    

    #   # BIGGER THAN
    # def Condition_bt(tools:dict)->bool:
    #     ''' @help RESPECT the syntaxe:
    #     {"a":'<VALUE_A>', "b":<VALUE_B>}
    #     '''
    #     print(len(tools["a"]))
    #     return len([i for i in tools["a"]]) > len([i for i in tools["b"]])