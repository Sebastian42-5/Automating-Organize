import os

filename = input('Enter the name of teh file you want to create: ')


if not filename.endswith('.py'):
    filename = filename + '.py'


try:
    created_file = open(filename, 'w')

    created_file.write('#start coding here\n')

except Exception as e:
    print('An error occured: ')


