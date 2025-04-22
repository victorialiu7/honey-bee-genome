#!C:/Users/victo/anaconda3/envs/py36/python.exe

'''
FRAMEWORK PROVIDED BY LECTURE SLIDES

This program is to process the file uploaded by the user through a network and saves the processed data 
to an Oracle database. 
'''

import cgi
import cx_Oracle

def main(): #NEW
    form = cgi.FieldStorage() #cgi script line 
    theStr = form.getfirst('File Path', '')
    contents = processInput(theStr)
    print (contents)

def processInput(theFile):
    '''
    This function reads the bee gene data from a raw data file and extract the gi number values 
    and the gene sequences. Then, the relative frequencies of the nucleotide are calcualted for 
    each gene. A new Oracle database table is created using Python and is populated with the 
    data created.
    '''

    #connects to database and creates cursor
    con = cx_Oracle.connect('user_pass')
    cur = con.cursor()

    #drops the table if created
    cur.execute('drop table beeGenes')
    #creates beeGenes
    cur.execute('''create table beeGenes (
        gi varchar2(10),
        sequence clob,
        freq_A number,
        freq_C number,
        freq_G number,
        freq_T number,
        freq_GC number
    )''')

    #bindarraysize copied from lecture slides
    cur.bindarraysize = 50
    #max number of nucelotides in sequence from input_size.py
    cur.setinputsizes(10, 14440, float, float, float, float, float)

    #read raw data from file 
    infile = open(theFile, 'r')
    myStr = ""
    finalStr = ""
    start = False
    
    #form a string with the raw data and insert specific string where sequence starts 
    for aline in infile:
        if aline.startswith('>'):
            myStr = myStr + aline 
            start = True
        elif start:
            myStr = myStr + '_**gene_seq_starts_here**_' + aline 
            start = False
        else:
            myStr = myStr + aline 

    #form a continuous string
    strL = myStr.replace("\n", "")

    #change the string into a list, one gene per list item
    aList = strL.split(">")

    #keep list istems that contain the substring, Apis mellifera 
    for anItem in aList:
        if '_**gene_seq_starts_here**_' in anItem:
            finalStr = finalStr + anItem

    end = 0
    totalLength = len(finalStr)
    #count number of genes
    repetitions = finalStr.count('_**gene_seq_starts_here**_')

    #extract the target substrings, the gi number and the gene sequence 
    for i in range(repetitions):
        start = finalStr.find('gi|', end) + 3
        end = finalStr.find("|", start)
        gi = finalStr[start: end]
        start = finalStr.find('_**gene_seq_starts_here**_', end) + 26
        end = finalStr.find('gi|', start)
        #if end cannot be found, it is the last gene 
        if end == -1:
            end = totalLength
        seq = finalStr[start: end]

        #determine frequency of each nucleotide
        seqLength = len(seq)
        freq_A = seq.count('A')/float(seqLength)
        freq_C = seq.count('C')/float(seqLength)
        freq_G = seq.count('G')/float(seqLength)
        freq_T = seq.count('T')/float(seqLength)
        freq_GC = freq_C + freq_G

        cur.execute('''insert into beeGenes (gi, sequence, freq_A, freq_C, freq_G, freq_T, freq_GC) values (:v1, :v2, :v3, :v4, :v5, :v6, :v7)
        ''', (gi, seq, freq_A, freq_C, freq_G, freq_T, freq_GC))
    

    con.commit()
    infile.close()
    cur.close() 
    con.close()

    return makePage('C:\\Users\\victo\\Downloads\\stsci_4060\\Final_Liu_Victoria\\Completed_Submission_Template.html', "Thank you for uploading.")

def fileToStr(fileName):
    '''Return a string containing the contents of the named files.'''
    fin = open(fileName)
    contents = fin.read()
    fin.close()
    return contents

def makePage(templateFileName, substitutions):
    pageTemplate = fileToStr(templateFileName)
    return pageTemplate % substitutions

try:
    print("Content-type: text/html\n\n")
    main()
except:
    cgi.print_exception() 





