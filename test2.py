import os


path = 'Z:/'
for file in os.listdir(path):
    if os.path.isdir(f'{path}/{file}'):
        for folder in os.listdir(f'{path}/{file}'):
            try:
                if 'gcp' in folder.lower() or 'gps' in folder.lower():
                    print(file)
            except:
                print('oops2')
