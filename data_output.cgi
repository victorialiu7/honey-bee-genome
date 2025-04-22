#!C:/Users/victo/anaconda3/envs/py36/python.exe

'''
FRAMEWORK PROVIDED BY LECTURE SLIDES

This program is extracts the data from the Oracle database and display them on a webpage
upon user's request.
'''

import cgi
import cx_Oracle
import scipy as sp

def main(): #NEW
    contents = processInput()
    print(contents)

#This function extras data from an Oracle table.
def processInput(): 
    con = cx_Oracle.connect('user_pass')
    cur = con.cursor()
    nucelotidesList = ['A', 'C', 'G', 'T']
    #creates four lists in a list 
    fList = [[] for t in range(4)]
    #iterates through each nucelotide 
    for i in range(4):
        myDict = {'nucelotide': nucelotidesList[i]}
        #extracts gi and frequency of nucelotide's maximum frequency 
        cur.execute('''select gi, freq_%(nucelotide)s 
        from beeGenes, 
        (select max(freq_%(nucelotide)s) as max%(nucelotide)s from beeGenes) 
        where freq_%(nucelotide)s = max%(nucelotide)s''' % myDict)

        obj = cur.fetchall()

        #add the maximum freq of each nucelotide to fList as an element
        for x in obj: 
            fList[i].append(x)

    myList = []
    for t in range(4):
        #for multiple gi numbers with the same max freq
        gi_numbers = '<br>'.join(str(x[0]) for x in fList[t])  
        #extract the max freq of each nucelotide 
        max_freq = str(fList[t][0][1])
        myList.append(gi_numbers)
        myList.append(max_freq)

    cur.close()
    con.close()
    return makePage(r"C:\Users\victo\Downloads\stsci_4060\Final_Liu_Victoria\See_Results_Template.html", myList)

def fileToStr(fileName):
    '''Return a string containing the contents of the name file.'''
    fin = open(fileName)
    contents = fin.read()
    fin.close()
    return contents

def makePage(templateFileName, substitutions):
    pageTemplate = fileToStr(templateFileName)
    #substituting all the strings with the elements of the tuple (originally list)
    return pageTemplate % tuple(substitutions)  

try: 
    print('Content-type: text/html\n\n')
    main()
except:
    cgi.print_exception()

        

    