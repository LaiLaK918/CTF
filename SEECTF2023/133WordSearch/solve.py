
file = 'wordsearch1.txt'
wordsearch = open(file).read().splitlines()

pos = [[487, 953], [486, 952], [485, 951], [484, 950]]

i = pos[0][0]
j = pos[0][1]
flag = ''

while '}' not in flag:
    flag += wordsearch[i][j]
    i -= 1
    j -= 1
    
print(flag) 