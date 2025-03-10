
'''This program determines the maximum number of nucleotides of all the genes in the data file.
Most of the code is copied over from process_link.py.'''

#intialize maximum number of nucelotides 
max_num = 0

#reads file 
infile = open(r'C:\Users\victo\Downloads\stsci 4060\Final_Liu_Victoria\honeybee_gene_sequences.txt', 'r')
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
repetitions = finalStr.count('_**gene_seq_starts_here**_')

#extract the target substrings, the gi number and the gene sequence 
for i in range(repetitions):
        start = finalStr.find('_**gene_seq_starts_here**_', end) + 26
        end = finalStr.find('gi|', start)
        if end == -1:
            end = totalLength
        seq = finalStr[start: end]
        #choose the longest gene sequence out of all genes
        max_num = max(max_num, len(seq))  

print(max_num) #output is 14440