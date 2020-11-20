import pandas as pn


walkFiles = os.walk(r'D:\engram\New_Converted_Folder\N1\1h-Done\done\separate files')
filesNames = []
for root, dirs, file in walkFiles:
    filesNames = file

filesNames = [i for i in filter(lambda file: 'final' in file, filesNames)]
print(filesNames)
unknown_id = []
#
for file in filesNames:
    a = pn.read_csv(r'D:\engram\New_Converted_Folder\N1\1h-Done\done\separate files' + "\\" + file)
    a = a[a['id name'] == '??']
    b = a['id'].unique()
    print (b)
    unknown_id.append([int(i) for i in b])

print(unknown_id)
s=[]
for i in unknown_id:
    for j in i:
        s.append(j)

print (set(s))