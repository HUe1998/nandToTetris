file=open('zzz.txt', 'w')
for i in range(16):
    file.write('Mux(a=a[{}], b=b[{}], sel=sel, out=out[{}]);\n'.format(i,i,i))
file.close()