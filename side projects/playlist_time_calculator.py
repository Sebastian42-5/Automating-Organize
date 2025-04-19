import datetime

def playlist_time_calculator():

    song_count = int(input('Enter the number of songs: '))

    total_seconds = 0

    for i in range(song_count):
        song = input(f'Enter the length of song {i + 1} with no column: ')

        song_in_seconds = int(song[0]) * 60 + int(song[1:])

        total_seconds += song_in_seconds

    total_time = str(datetime.timedelta(seconds = total_seconds))



    print(f'Here is the length of your playlist: {total_time}') 

   

playlist_time_calculator()

    
   




