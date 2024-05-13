import tekore as tk
import random
import time

client_id = '39a984fe634c49b3b48924061760391e'
client_secret = #Insert clint Secret Here
redirect_uri = 'https://example.com/callback'
user_id = 'jsandish23'

conf = tk.config_from_file('tekore.cfg', return_refresh=True)
user_token = tk.refresh_user_token(*conf[:2], conf[3])

spotify = tk.Spotify(user_token)

def main():
    # Print selected user's playlists
    print("Your Playlists:")
    playlists = spotify.playlists(user_id, limit=20, offset=0)
    for i in range(len(playlists.items)):
        print(i, playlists.items[i].name)

    # Select playlist
    playlist_choice = int(input("What Playlist? "))
    chosen_playlist = spotify.playlist(playlists.items[playlist_choice].id, fields=None, market=None, as_tracks=False)

    # Print songs from chosen playlist
    for i in range(len(chosen_playlist.tracks.items)):
        print(i, chosen_playlist.tracks.items[i].track.name)

    # Ask if user wants random start placement
    user_random_response = input("Start Song at Random Place? Y / N: ")
    if user_random_response == 'Y' or user_random_response == 'y':
        random_start = True
    else:
        random_start = False

    # song_choice = int(input("Select Which Song: "))
    while True:
        song_amount = 1

        # Pick random song
        random_track_ind = random.randint(0, len(chosen_playlist.tracks.items) - 1)

        # Assign name to track and condense
        chosen_song = [chosen_playlist.tracks.items[random_track_ind].track.id]
        song_name = chosen_playlist.tracks.items[random_track_ind].track.name
        song_name_l = song_name.lower()
        if song_name_l.find("(") != -1:
            song_name_l = song_name_l[0:song_name.find("(") - 1]

        # Find random starting position
        if random_start:
            song_length = chosen_playlist.tracks.items[random_track_ind].track.duration_ms
            start_position = random.randint(0, song_length - 16000)
        else:
            start_position = 0
        
        # Playback, and user guesses and varification
        while True:
            spotify.playback_start_tracks(chosen_song, offset=None, position_ms=start_position, device_id=None)
            time.sleep(song_amount)
            spotify.playback_pause(device_id=None)
            guess = input("Guess the Song: ").lower()
            if guess == "":
                return
            elif guess == song_name_l or song_name_l.find(guess) != -1:
                print("Correct! The song was", song_name)
                break
            else:
                print("Incorrect :( guess again")
                song_amount = song_amount * 2
                continue

main()
