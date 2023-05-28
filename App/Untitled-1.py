"prueba"

n =10.23989438985
o =-43.09343095
def redondear_4_hacia_arriba(num):
    parte_decimal = str(num).split('.')[1]
    parte_entera =str(num).split('.')[0]
    cuatro_decimales = parte_decimal[0:4]
    num=float(parte_entera+'.'+cuatro_decimales)
    if num>0:
        num=num+0.0001
    return num

e = redondear_4_hacia_arriba(n)
f=redondear_4_hacia_arriba(o)
print(e)
print(f)

string= 'aaaa'

string+='bbbbbbb'
print(string)

i=''

if float(i)<0:
    print('h')