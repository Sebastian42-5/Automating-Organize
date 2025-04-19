import os
import shutil



def download_organizer(files):
    for file in files:
        
        filename, extension = os.path.splitext(file) 

        extension_folder_for_downloads = sorting_downloads_path + '/' + extension

        current_file_dir = downloads_path + '/' + file

        assigned_extension_dir = sorting_downloads_path + '/' + extension + '/' + file


        if os.path.exists(extension_folder_for_downloads):

            shutil.move(current_file_dir, assigned_extension_dir)

        else:
            os.makedirs(extension_folder_for_downloads)

            shutil.move(current_file_dir, assigned_extension_dir)
    print('The current files in Downloads have been organized.')


# path = input('Enter path: ')

sorting_downloads_path = 'C:/Users/sebas/Documents/sorted_downloads'

downloads_path = 'C:/Users/sebas/Downloads'

files = os.listdir(downloads_path)


if not files:
    print('There are no files to organize.')

else:
    download_organizer(files)


    

# think of a way to create a new folder that would organize all your files from your downloads

# basically, when you download something, you run the function and it will automatically sort the file into the right folder. 

# I made ittt




# for later: think of a way to run this program automatically when there is a new download


