def songs_list(input_path, output_path="sorted_songs.txt"): 
    with open(input_path, "r", encoding="utf-8") as input_file:
        songs = input_file.readlines()


    songs.sort(key=str.lower)

    
    with open(output_path, "w", encoding="utf-8") as output_file:
        for song in songs:
            output_file.write(song)
            print(f"Song: {song.strip()}")


songs_list("songs.txt")