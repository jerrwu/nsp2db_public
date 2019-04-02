from __future__ import print_function
import os
import argparse
import shutil
import getpass
import mysql.connector
import time
import tkinter as tk
from tkinter import filedialog

# print header
print('  ______________________________________  ')
print(' /                                      \ ')
print('< ============Add NSP to DB============= >')
print(' \______________________________________/ ')
print('')

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
    time.sleep(2)

cursor = nspdb.cursor()

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
            cursor.execute('use nsps')
            cursor.execute(add_update)
            print('Update NSP info successfully added to DB!')
            nspdb.commit()
            cursor.execute('SELECT * FROM `update` ORDER BY game_title')
            data=cursor.fetchall()
            for i in range(len(data)):
                print(data[i])
            time.sleep(1)
        else:
            print('Aborted')
            time.sleep(0.5)
    
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
            cursor.execute('use nsps')
            cursor.execute(add_update)
            print('DLC NSP info successfully added to DB!')
            nspdb.commit()
            cursor.execute('SELECT * FROM dlc ORDER BY game_title')
            data=cursor.fetchall()
            for i in range(len(data)):
                print(data[i])
            time.sleep(1)
        else:
            print('Aborted')
            time.sleep(0.5) 
    
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
            cursor.execute('use nsps')
            cursor.execute(add_update)
            print('Base NSP info successfully added to DB!')
            nspdb.commit()
            cursor.execute('SELECT * FROM base ORDER BY game_title')
            data=cursor.fetchall()
            for i in range(len(data)):
                print(data[i])
            time.sleep(1)
        else:
            print('Aborted')
            time.sleep(0.5)        
        
def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-n','--name',action='store_true',help='Use a file name instead of choosing a file')
    args = parser.parse_args()
    
    # tk setup
    root=tk.Tk()
    root.withdraw()    
    
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

if __name__=='__main__':
    main()