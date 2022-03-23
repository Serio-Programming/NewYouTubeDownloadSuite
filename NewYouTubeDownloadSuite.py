# NewYouTubeDownloadSuite
# This program allows you to download channels, playlists, and single videos from YouTube as videos or audio
# Programming began circa December 2021
# A program by Tyler Serio
# Python 3.9.5
# Pytube v. 11.0.2

# Import packages
import pytube
from pytube import YouTube
from pytube import Playlist
from pytube import Channel
import os
import time

# Create/check for directories to store downloads
try:
    os.makedirs("Downloads")
    print("Directory for Downloads created.")
except FileExistsError:
    pass
except Exception as e:
    print("Error: " + str(e))

try:
    os.makedirs("downloads/Single Videos")
    print("Directory for Single Videos created.")
except FileExistsError:
    pass
except Exception as e:
    print("Error: " + str(e))

try:
    os.makedirs("downloads/Playlists")
    print("Directory for Playlists created.")
except FileExistsError:
    pass
except Exception as e:
    print("Error: " + str(e))

try:
    os.makedirs("downloads/Channels")
    print("Directory for Channels created.")
except FileExistsError:
    pass
except Exception as e:
    print("Error: " + str(e)) \

# Directory name cleaning function
def clean_name(name):
    name = str(name)
    name_list = list(name)
    count = -1
    for c in name_list:
        count += 1
        if str(c) == r"/" or str(c) == "#" or str(c) == "%" or str(c) == "&" or str(c) == "\\" \
           or str(c) == "{" or str(c) == "}" or str(c) == "<" or str(c) == ">" or str(c) == "*" \
            or str(c) == "?" or str(c) == "=" or str(c) == "$" or str(c) == "!" or str(c) == "'" \
             or str(c) == '"' or str(c) == ":" or str(c) == "@" or str(c) == "+" or str(c) == "`" \
              or str(c) == "|":
            name_list[count] = "-"
    name = "".join(name_list)
    return name

# Function to allow user to choose file type for download
def format_selector(download_type):
    os.system("cls")
    format_selection = 1
    while format_selection == 1:
        print(download_type + ":")
        print("What file format do you want your downloads to be?")
        print("")
        print("[1] - Video files.")
        print("[2] - Audio files.")
        print("[0] - Back to main menu.")
        print("")
        print("Please make your selection and then press enter.")
        selection = input(">> ")
        
        if selection != "1" and selection != "2" and selection != "0":
            os.system("cls")
            print("You have chosen '" + selection + "'. That is not a proper selection.")
            print("Please choose from the following options:")

        if selection == "0":
            file_format = "None"
            return file_format

        if selection == "1":
            file_format = "Video"
            return file_format

        if selection == "2":
            file_format = "Audio"
            return file_format

# Function to check if URL is proper
# Function to download from URL
def check_and_download(download_type, file_format, selection):
    os.system("cls")
    if file_format == "None":
        return "None"

    checking_and_downloading = 1
    while checking_and_downloading == 1:

        # Check URL
        # Ask for new URL if required
        checking = 1
        while checking == 1:
            print(download_type + ", " + file_format + " File" + ":")
            print("Please specify the URL you would like to download from and then press enter.")
            print("Or select [0] to go back.")
            URL = input(">> ")
            if URL == "0":
                return selection
            try:
                if download_type == "Single Video":
                    yt_obj = YouTube(str(URL))
                    checking = 0
                    
                elif download_type == "Playlist":
                    yt_obj = Playlist(str(URL))
                    checking = 0
                    
                else:
                    yt_obj = Channel(str(URL))
                    checking = 0

            except Exception as e:
                print("Error: " + str(e))
                os.system("cls")
                print("You have entered '" + URL + "'")
                print("There is an issue with that URL. Cannot download.")
                print("")

        # Download from URL
        downloading = 1
        destination = ("Downloads/" + str(download_type) + "s")
        while downloading == 1:
            # Download single videos
            if download_type == "Single Video":
                try:
                    author = clean_name(yt_obj.author)
                    title = clean_name(yt_obj.streams.first().default_filename.split(".")[0])
                    if file_format == "Video":
                        stream_list = str(yt_obj.streams.filter(progressive=True))
                        stream_list = stream_list.strip("[")
                        stream_list = stream_list.strip("]")
                        stream_list = stream_list.strip(">")
                        rf_stream_list = stream_list.split("<Stream: ")
                        del rf_stream_list[0]
                        rf_stream_list.reverse()
                        for item in rf_stream_list:
                            item = item.split()
                            item[0] = item[0].strip('itag="')
                            if item[2] == 'res="720p"':
                                yt_obj.streams.get_by_itag(int(item[0])).download(output_path=destination, filename= title + " by " + author + " - " + file_format + ".mp4")
                                break
                            
                            elif item[2] == 'res="480p"':
                                yt_obj.streams.get_by_itag(int(item[0])).download(output_path=destination, filename= title + " by " + author + " - " + file_format + ".mp4")
                                break
                                
                            else:
                                yt_obj.streams.get_by_itag(int(item[0])).download(output_path=destination, filename= title + " by " + author + " - " + file_format + ".mp4")
                                break
                        print(f"Successfully downloaded: {yt_obj.title} at " + str(item[2]).strip('res="') + " resolution")

                    else:
                        yt_obj.streams.filter(only_audio = True, file_extension='mp4').first().download(output_path=destination, filename= title + " by " + author + ".mp4")
                        print(f"Successfully downloaded: {yt_obj.title}")
                        
                except Exception as e:
                        os.system("cls")
                        print("Error: " + str(e))
                        print(f"Sorry, '{yt_obj.title}' is unavailable.")
                        print("It may be private, age-restricted, or area-restricted.")
                        downloading = 0

                os.system("cls")
                if file_format == "Video":
                    print(f"Successfully downloaded: {yt_obj.title} at " + str(item[2]).strip('res="') + " resolution")
                else:
                    print(f"Successfully downloaded: {yt_obj.title}")
                downloading = 0

            # Download playlists
            elif download_type == "Playlist":
                try:
                    pname = clean_name(yt_obj.title)
                    destination = (destination + "/" + pname + f" - {file_format}")
                    os.makedirs(destination)
                    
                except FileExistsError:
                    pass
                
                except KeyError:
                    destination = ("Downloads/" + str(download_type) + "s")
                    
                except Exception as e:
                    print("Error: " + str(e))

                # Download playlist in video format              
                if file_format == "Video":
                    try:
                        print(f"Downloading: {yt_obj.title}")
                        for url in yt_obj.video_urls:
                            try:
                                mini_obj = YouTube(str(url))
                                title = clean_name(str(mini_obj.streams.first().default_filename.split(".")[0]))
                                author = clean_name(str(mini_obj.author))
                                stream_list = str(mini_obj.streams.filter(progressive=True))
                                stream_list = stream_list.strip("[")
                                stream_list = stream_list.strip("]")
                                stream_list = stream_list.strip(">")
                                rf_stream_list = stream_list.split("<Stream: ")
                                del rf_stream_list[0]
                                rf_stream_list.reverse()
                                for item in rf_stream_list:
                                    item = item.split()
                                    item[0] = item[0].strip('itag="')
                                    if item[2] == 'res="720p"':
                                        mini_obj.streams.get_by_itag(int(item[0])).download(output_path=destination, filename= title + " by " + author + " - " + file_format + ".mp4")
                                        break
                                    
                                    elif item[2] == 'res="480p"':
                                        mini_obj.streams.get_by_itag(int(item[0])).download(output_path=destination, filename= title + " by " + author + " - " + file_format + ".mp4")
                                        break
                                        
                                    else:
                                        mini_obj.streams.get_by_itag(int(item[0])).download(output_path=destination, filename= title + " by " + author + " - " + file_format + ".mp4")
                                        break
                                    
                                print(f"Successfully downloaded: {mini_obj.title} at " + str(item[2]).strip('res="') + " resolution")
                                                        
                            except Exception as e:
                                print("Error: " + str(e))
                                print(f"Sorry, '{mini_obj.title}' is unavailable.")
                                print("It may be private, age-restricted, or area-restricted.")
                                
                    except Exception as e:
                        print("Error: " + str(e))
                        os.system("cls")
                        print("You have entered '" + URL + "'")
                        print("There is an issue with that URL. Cannot download.")
                        print("")
                        downloading = 0
                        break

                    os.system("cls")
                    print(f"Successfully downloaded playlist: {yt_obj.title}")
                    downloading = 0

                # Download playlist in audio format
                else:
                    try:
                        print(f"Downloading: {yt_obj.title}")
                        for url in yt_obj.video_urls:
                            try:
                                mini_obj = YouTube(str(url))
                                title = clean_name(str(mini_obj.streams.first().default_filename.split(".")[0]))
                                author = clean_name(str(mini_obj.author))
                                stream = mini_obj.streams.filter(only_audio = True, file_extension='mp4').first()
                                stream.download(output_path=destination, filename= title + " by " + author + ".mp4")
                                print(f"Successfully downloaded: {mini_obj.title}")
                                                            
                            except Exception as e:
                                print("Error: " + str(e))
                                print(f"Sorry, '{mini_obj.title}' is unavailable.")
                                print("It may be private, age-restricted, or area-restricted.")

                    except Exception as e:
                        os.system("cls")
                        print("Error: " + str(e))
                        print("You have entered '" + URL + "'")
                        print("There is an issue with that URL. Cannot download.")
                        print("")
                        downloading = 0
                        break

                    os.system("cls")
                    print(f"Successfully downloaded playlist: {yt_obj.title}")
                    downloading = 0
                    
            # Download channels
            else:
                try:
                    cname = clean_name(yt_obj.channel_name)
                    destination = (destination + "/" + cname + f" - {file_format}")
                    os.makedirs(destination)
                    
                except FileExistsError:
                    pass
                
                except KeyError:
                    destination = ("Downloads/" + str(download_type) + "s")

                except Exception as e:
                    print("Error: " + str(e))

                # Download channel in video format   
                if file_format == "Video":
                    try:
                        print(f"Downloading: {yt_obj.channel_name}")
                        for url in yt_obj.video_urls:
                            try:
                                mini_obj = YouTube(str(url))
                                title = clean_name(str(mini_obj.streams.first().default_filename.split(".")[0]))
                                author = clean_name(str(mini_obj.author))
                                stream_list = str(mini_obj.streams.filter(progressive=True))
                                stream_list = stream_list.strip("[")
                                stream_list = stream_list.strip("]")
                                stream_list = stream_list.strip(">")
                                rf_stream_list = stream_list.split("<Stream: ")
                                del rf_stream_list[0]
                                rf_stream_list.reverse()
                                for item in rf_stream_list:
                                    item = item.split()
                                    item[0] = item[0].strip('itag="')
                                    if item[2] == 'res="720p"':
                                        mini_obj.streams.get_by_itag(int(item[0])).download(output_path=destination, filename= title + " by " + author + " - " + file_format + ".mp4")
                                        break
                                    
                                    elif item[2] == 'res="480p"':
                                        mini_obj.streams.get_by_itag(int(item[0])).download(output_path=destination, filename= title + " by " + author + " - " + file_format + ".mp4")
                                        break
                                        
                                    else:
                                        mini_obj.streams.get_by_itag(int(item[0])).download(output_path=destination, filename= title + " by " + author + " - " + file_format + ".mp4")
                                        break
                                    
                                print(f"Successfully downloaded: {mini_obj.title} at " + str(item[2]).strip('res="') + " resolution")
                                                            
                            except Exception as e:
                                print("Error: " + str(e))
                                print(f"Sorry, '{mini_obj.title}' is unavailable.")
                                print("It may be private, age-restricted, or area-restricted.")
                                
                    except Exception as e:
                        print("Error: " + str(e))
                        os.system("cls")
                        print("You have entered '" + URL + "'")
                        print("There is an issue with that channel URL. Cannot download.")
                        print("")
                        downloading = 0
                        break
                    
                    os.system("cls")
                    print(f"Successfully downloaded channel: {yt_obj.channel_name}")
                    downloading = 0

                # Download channel in audio format
                else:
                    try:
                        print(f"Downloading: {yt_obj.channel_name}")
                        for url in yt_obj.video_urls:
                            try:
                                mini_obj = YouTube(str(url))
                                title = clean_name(str(mini_obj.streams.first().default_filename.split(".")[0]))
                                author = clean_name(str(mini_obj.author))
                                stream = mini_obj.streams.filter(only_audio = True, file_extension='mp4').first()
                                stream.download(output_path=destination, filename= title + " by " + author + " - " + file_format + ".mp4")
                                print(f"Successfully downloaded: {mini_obj.title}")
                                                            
                            except Exception as e:
                                print("Error: " + str(e))
                                print(f"Sorry, '{video.title}' is unavailable.")
                                print("It may be private, age-restricted, or area-restricted.")

                    except Exception as e:
                            print(e)
                            os.system("cls")
                            print("You have entered '" + URL + "'")
                            print("There is an issue with that URL. Cannot download.")
                            print("")
                            downloading = 0
                            break
                        
                    os.system("cls")
                    print(f"Successfully downloaded: {yt_obj.channel_name}")
                    downloading = 0

# Begin the program
on = 1
while on == 1:
    # Main menu selection
    main_selection = 1
    while main_selection == 1:
        print("New YouTube Downloader Suite (Python v. 3.9.5, Pytube v. 11.0.2, circa 2021)")
        print("What would you like to download from YouTube?")
        print("")
        print("[1] - Single Video")
        print("[2] - Playlist")
        print("[3] - Channel")
        print("[4] - Instructions")
        print("[0] - Exit")
        print("")
        print("Please make your selection and then press enter.")
        selection = str(input(">> "))

        # Handle an improper selection
        if selection != "1" and selection != "2" and selection != "3" and selection != "4" and selection != "0":
            os.system("cls")
            print("You have chosen '" + selection + "'. That is not a proper selection.")
            print("Please choose from the following options:")

        # Handle exit selection
        if selection == "0":
            exit()

        # Handle single video selection
        while selection == "1":
            download_type = "Single Video"
            file_format = format_selector(download_type)
            selection = check_and_download(download_type, file_format, selection)

        # Handle playlist selection
        while selection == "2":
            download_type = "Playlist"
            file_format = format_selector(download_type)
            selection = check_and_download(download_type, file_format, selection)

        # Handle channel selection
        while selection == "3":
            download_type = "Channel"
            file_format = format_selector(download_type)
            selection = check_and_download(download_type, file_format, selection)

        # Handle instruction selection
        if selection == "4":
            os.system("cls")
            print("Instructions:")
            print("First select whether you want to download a single video, playlist, or channel from YouTube.")
            print("Then select whether you want to download the single video, playlist, or channel in a video format or an audio format.")
            print("Then copy and past the URL of the single video, playlist, or channel from YouTube into the downloader program.")
            print("You must use a proper URL in order to download.")
            print("To download a single video you must input that video's URL, and not a playlist or channel URL.")
            print("To download a playlist you must input the playlist's URL and not a single video URL or a channel URL.")
            print("To download a channel you must input the channel's URL and not a single video URL or a playlist URL.")
            print("When downloading in the video format the program will automatically attempt to download the highest resolution progressive mp4 streams.")
            print("When downloading in the video format the resolution will usually be either 360p, 480p, or 720p, with a preference for 720p.")
            print("Enter [anything] to return to the main menu.")
            input(">> ")
            
