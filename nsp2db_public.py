from __future__ import print_function
import sys
import os
import argparse
import shutil
import getpass
import mysql.connector
import tkinter as tk
from tkinter import filedialog

# print header
print('  ______________________________________  ')
print(' /                                      \ ')
print('< ============Add NSP to DB============= >')
print(' \______________________________________/ ')
print('')

db=open('db.ini','r')
data=db.readlines()
db.close()

dbhost=data[0].split()[2]
dbuser=data[1].split()[2]

if len(data[2].split())==3:
    dbpass=data[2].split()[2]
else:
    # get database password
    dbpass=getpass.getpass('Database password: ')


try:
# mysql connection
    nspdb = mysql.connector.connect(
        host ="localhost",
        user="root",
        passwd=dbpass)
    print('Connection succeeded')
except:
    print('Invalid password, please restart the program')
    sys.exit()

cursor = nspdb.cursor()

cursor.execute('use nsps')

# convert filepath to filename
def getName(filepath):
    filename=os.path.basename(filepath)
    return filename.replace('.nsp','')
    
def getInfo(filename):
    
    # update
    if '[UPD]' in filename:
        print('Type: Update')
        split=filename.split(' [UPD]')
        # game title
        title=split[0]
        # id and version
        idver=split[1]
        
        title_id=idver.split('][')[0].replace('[','')
        version_num=idver.split('][')[1].replace(']','')
        
        print('\n','>filename: {0}'.format(filename),'\n',
            '>title: ',title,'\n',
            '>title_id: ',title_id,'\n',
            '>version_number: ',version_num)
        
        # ask for permission
        perm=input('Insert data? Y/N: ')
        
        if perm=='Y':
            # add upd to db
            add_update=('INSERT INTO `update` (game_title, title_id, version_num)'
                        'VALUES ("{0}", "{1}", "{2}")'.format(title,title_id,version_num))
            cursor.execute(add_update)
            print('Update NSP info successfully added to DB!')
            nspdb.commit()
            cursor.execute('SELECT * FROM `update` ORDER BY game_title')
            data=cursor.fetchall()
            display(data)
        else:
            print('Aborted')
    
    # dlc
    elif '[DLC]' in filename:
        print('Type: DLC')
        split=filename.split(' [DLC]')
        # game title
        title=split[0]
        # id and version
        idver=split[1]
        
        title_id=idver.split('][')[0].replace('[','')
        version_num=idver.split('][')[1].replace(']','')
        
        print('\n','>filename: {0}'.format(filename),'\n',
            '>title: ',title,'\n',
            '>title_id: ',title_id,'\n',
            '>version_number: ',version_num)
        
        # ask for permission
        perm=input('Enter info? Y/N: ')
        
        if perm=='Y':
            # add dlc to db
            add_update=('INSERT INTO dlc (game_title, title_id, version_num)'
                        'VALUES ("{0}", "{1}", "{2}")'.format(title,title_id,version_num))
            cursor.execute(add_update)
            print('DLC NSP info successfully added to DB!')
            nspdb.commit()
            cursor.execute('SELECT * FROM dlc ORDER BY game_title')
            data=cursor.fetchall()
            display(data)
        else:
            print('Aborted')
    
    # base
    else:
        print('Type: Base')
        split=filename.split(' [')
        # game title
        title=split[0]
        # id and version
        idver=split[1]
        
        title_id=idver.split('][')[0]
        version_num=idver.split('][')[1].replace(']','')
        
        print('\n','>filename: {0}'.format(filename),'\n',
            '>title: ',title,'\n',
            '>title_id: ',title_id,'\n',
            '>version_number: ',version_num)
        
        # ask for permission
        perm=input('Insert data? Y/N: ')
        
        if perm=='Y':
            # add base to db
            add_update=('INSERT INTO base (game_title, title_id, version_num)'
                        'VALUES ("{0}", "{1}", "{2}")'.format(title,title_id,version_num))
            cursor.execute(add_update)
            print('Base NSP info successfully added to DB!')
            nspdb.commit()
            cursor.execute('SELECT * FROM base ORDER BY game_title')
            data=cursor.fetchall()
            display(data)
        else:
            print('Aborted')    
            
def display(data):
    if data==[]:
        print("\nNo files found!")
    else:
        maxlen_title=max(map(lambda x: len(x[1]), data))
        maxlen_ver=max(map(lambda x: len(x[2]), data))
        for i in range(len(data)):
            print('-'*(26+maxlen_title+maxlen_ver))
            g=data[i]
            print('|',g[0],
                  '|',g[1],
                  '{0}|'.format(' '*(maxlen_title-len(g[1]))),
                  g[2],
                  '{0}|'.format(' '*(maxlen_ver-len(g[2]))))
        print('-'*(26+maxlen_title+maxlen_ver))
        print('\n\n')  
        
def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-n','--name',action='store_true',help='Use a file name instead of choosing a file')
    args = parser.parse_args()
    
    # tk setup
    root=tk.Tk()
    root.withdraw()    
    
    mode=input(
        'Select search or import:\nInput S for search\nInput I for import\n>')
    print('\n')
    if mode=='S':
        print('Mode: Search\n\nSelect type:\nInput 0 for base\nInput 1 for update\nInput 2 for DLC')
        ftype=input('>')
        print('\n')
        if ftype=='0':
            fname=input('Enter game title:')
            cursor.execute(
                'SELECT * FROM base WHERE game_title like "%{0}%" ORDER BY version_num'.format(fname))
        elif ftype=='1':
            fname=input('Enter game title:')
            cursor.execute(
                'SELECT * FROM `update` WHERE game_title like "%{0}%" ORDER BY version_num'.format(fname))            
        elif ftype=='2':
            fname=input('Enter game title:')
            cursor.execute(
                'SELECT * FROM dlc WHERE game_title like "%{0}%" ORDER BY version_num'.format(fname))   
        data=cursor.fetchall()
        display(data)        
        
    elif mode=='I':
        # passing filename on to info getter
        if args.name:
            name=input('NSP filename: ')
            getInfo(name)
        else:
            filepaths=filedialog.askopenfilenames()
            print('\nSelected {0} file(s).\n'.format(len(filepaths)))
            for f in filepaths:
                print('Processing file {0}/{1}'.
                      format(filepaths.index(f)+1,len(filepaths)))
                getInfo(getName(f))
            print('\nEnd of files.\n')
    else:
        print('Invalid input\n')
        main()
        
    input('Press Enter to exit')

if __name__=='__main__':
    main()