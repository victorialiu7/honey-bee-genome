import cx_Oracle

con = cx_Oracle.connect('VICTORIA/Begin1025!')
cur = con.cursor()
cur.execute('''SELECT sequence
FROM beeGenes 
WHERE gi = 147907436
''')

data = cur.fetchall()

if data:
    sequence = data[0][0].read()
    print(sequence)
