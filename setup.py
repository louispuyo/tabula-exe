from os import path
import os

def main():
    
    if os.getenv('MODE') == 'LOCAL':
        if path.exists('.gitignore'):
            current_path = os.curdir
            with open(f'{current_path}'+'gitignore', 'a') as file:
                file.write('\ntests.py')
        else:
            print("[-] [PATH ERROR] -> .gitignore Not such file directory")

    else:
        print('Not found')
# path.exists('career.guru99.txt')
# path.exists('myDirectory')

if __name__== "__main__":
   main()