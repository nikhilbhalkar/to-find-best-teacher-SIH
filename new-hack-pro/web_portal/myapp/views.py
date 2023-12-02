from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import OurUser
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from django.contrib.auth.models import User

api_key = 'AIzaSyDAPQCy1PO5QRrax0MjjWqD33UY1Jnn7l8'

import os
import csv
import googleapiclient.discovery
from textblob import TextBlob
from datetime import datetime, timedelta
import wikipedia

# Create your views here.
def home(request):
    
    return render(request, 'landing_page.html')


def mainhome(request):
    return render(request, 'home_page.html')

def login1(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def registeruser(request):

    if request.method=='POST':

        username=request.POST['username']
        email=request.POST['email']
        #fname=request.POST['fname']
        #lname=request.POST['lname']
        pass1=request.POST['password']
        interest=request.POST['interest']
        level=request.POST['level']
        learningstyle=request.POST['learningstyle']
        pass2=pass1
        fname="nikhil"
        lname="bhalkar"
        
       
    
        #create the user
        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, 'Your Account has been succesfully created')
        new_data = OurUser(username=username,email=email,password=pass1,interest=interest,level=level,learningstyle=learningstyle)
        new_data.save()

        return redirect('login1')

        
    else:
         return HttpResponse('404 - Not Found')     
     
     

     
   
def loginuser(request):
    print("nihkilllll")
    if request.method=='POST':
        loginusername = request.POST['username']
        loginpassword = request.POST['password']
        print(loginpassword)
        print(loginusername)

        user = authenticate(username = loginusername, password = loginpassword)
        print(user)
        

        if user is not None:
            login(request, user)
            messages.success(request, "Succesfully Logged In")
            return redirect('mainhome')
        else:
            messages.error(request, "Invalid Username or Password")  
            return redirect('login1')  
    return HttpResponse('404 - Not Found')


def logout(request):
        #logout(request)
        messages.success(request, "Succesfully Logged out")
        return redirect('home')
    
    
def findteacher(request):
    currentuser_email = request.user.email
    currentuser_username = request.user.username
    user_profile = OurUser.objects.get(email=currentuser_email,username=currentuser_username)
   
    search = ''

    if request.method == 'POST':
        search = request.POST.get('searchinfo', '')


   
    if search == "":
        search_query = user_profile.interest
    else:
        search_query = search
    
    info = wikipedia.summary(search_query)
    print(info)
    context = {
        'info' : info,
        'search_query' : search_query,
       
    }
    return render(request, 'findteacher.html',context)



def findcourse(request):
    return render(request, 'findcourse.html')






def indexprofile(request):
    currentuser_email = request.user.email
    currentuser_username = request.user.username
    user_profile = OurUser.objects.get(email=currentuser_email,username=currentuser_username)
    print("================================")
    print(currentuser_email)
    print(currentuser_username)
    print(user_profile.level)
    print("================================")
    return render(request, 'index.html', {'user_profile':user_profile})    


@login_required
def profilepage(request):
    return render(request, 'profile.html')


def findvideo(request):
    currentuser_email = request.user.email
    currentuser_username = request.user.username
    user_profile = OurUser.objects.get(email=currentuser_email,username=currentuser_username)
    search = ''

    if request.method == 'POST':
        search = request.POST.get('search', '')

    # Rest of your view logic
    # ...

    youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=api_key)

    # Your search query
    if search == "":
        search_query = user_profile.interest
    else:
        search_query = search

    # Maximum number of videos to retrieve
    max_results = 10

    data = []

    # Function to retrieve all comments for a video
    def get_all_comments(video_id):
        all_comments = []
        next_page_token = None

        while True:
            comments_response = youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                textFormat='plainText',
                maxResults=100,  # Maximum comments per page
                pageToken=next_page_token
            ).execute()

            for comment in comments_response['items']:
                comment_text = comment['snippet']['topLevelComment']['snippet']['textDisplay']
                all_comments.append(comment_text)

            next_page_token = comments_response.get('nextPageToken')

            if not next_page_token:
                break

        return all_comments

    # Function to retrieve limited comments with sentiment analysis for a video
    def get_limited_comments_with_sentiment(video_id, max_comments=500):
        all_comments_with_sentiment = []
        next_page_token = None
        comment_count = 0

        while True:
            try:
                comments_response = youtube.commentThreads().list(
                    part='snippet',
                    videoId=video_id,
                    textFormat='plainText',
                    maxResults=100,  # Maximum comments per page
                    pageToken=next_page_token
                ).execute()

                for comment in comments_response['items']:
                    comment_text = comment['snippet']['topLevelComment']['snippet']['textDisplay']

                    # Sentiment Analysis using TextBlob
                    analysis = TextBlob(comment_text)
                    sentiment_score = analysis.sentiment.polarity

                    all_comments_with_sentiment.append((comment_text, sentiment_score))
                    comment_count += 1

                    if comment_count >= max_comments:
                        return all_comments_with_sentiment

                next_page_token = comments_response.get('nextPageToken')

                if not next_page_token:
                    break

            except googleapiclient.errors.HttpError as e:
                if 'commentsDisabled' in str(e):
                    print(f"Comments are disabled for video with ID {video_id}. Skipping...")
                    break  # Skip this video if comments are disabled
                else:
                    raise  # Raise the exception if it's not due to disabled comments

        return all_comments_with_sentiment


    # Make a request to search for videos
    search_response = youtube.search().list(
        q=search_query,
        type='video',
        part='id',
        maxResults=max_results
    ).execute()

    # Extract video IDs from the search results
    video_ids = [item['id']['videoId'] for item in search_response['items']]

    video_sentiment_scores = []

    # Fetch and print likes, views, comments, and channel information for each video
    for video_id in video_ids:
        video_response = youtube.videos().list(
            part='snippet,statistics',
            id=video_id
        ).execute()

        video_info = video_response['items'][0]
        title = video_info['snippet']['title']
        views = video_info['statistics'].get('viewCount', 'N/A')
        likes = video_info['statistics'].get('likeCount', 'N/A')
        pubish_date = video_info['snippet']['publishedAt']
        video_link = f"https://www.youtube.com/embed/{video_id}"  # Construct video link

        ## Extracting year from date
        publish_year = int(pubish_date.split('-')[0])
        
    #     print(publish_year)
        
        
        # Calculate the likes-to-views ratio for the video
        if likes != 'N/A' and views != 'N/A':
            likes_to_views_ratio = int(likes) / max(int(views), 1)  # Avoid division by zero
        else:
            likes_to_views_ratio = 0.0

        # Retrieve limited comments with sentiment analysis
        video_comments = get_limited_comments_with_sentiment(video_id, max_comments=30)
        
        # Calculate the average sentiment score for comments on this video
        video_sentiments = [score for _, score in video_comments]

        # Check if the video_comments list is empty before calculating the average
        if video_sentiments:
            avg_sentiment = sum(video_sentiments) / len(video_sentiments)
        else:
            avg_sentiment = 0.0  # Set the default average sentiment to 0 if no comments

        video_sentiment_scores.append(avg_sentiment)

        # Fetch channel information by making an additional request
        channel_response = youtube.channels().list(
            part='snippet,contentDetails,statistics',
            id=video_info['snippet']['channelId']
        ).execute()

        if 'items' in channel_response:
            channel_info = channel_response['items'][0]
            channel_name = channel_info['snippet']['title']
            subscribers = channel_info['statistics'].get('subscriberCount', 'N/A')
            total_views = channel_info['statistics'].get('viewCount', 'N/A')
            total_videos = channel_info['statistics'].get('videoCount', 'N/A')
            
            # Calculate the 'Subscribers to Views' ratio
            if subscribers != 'N/A' and total_views != 'N/A':
                subscribers_to_views_ratio = int(subscribers) / max(int(total_views), 1)  # Avoid division by zero
            else:
                subscribers_to_views_ratio = 0.0

            data.append({
                'Video Title': title,
                'Views': views,
                'Likes': likes,
                'Likes-to-Views Ratio': likes_to_views_ratio,
                'Channel Name': channel_name,
                'Subscribers': subscribers,
                'Total Views (Channel)': total_views,
                'Total Videos (Channel)': total_videos,
                'comments': [comment for comment, _ in video_comments[1:]],  # Extract only comments
                'Average Sentiment': avg_sentiment,
                'Video Link': video_link,  # Include video link
                'Subscribers to Views Ratio': subscribers_to_views_ratio,
                'Publish Year' : publish_year
            })
            
    def calculate_combined_score(video):
        sentiment_weight = 3  # Adjust the weight as needed
        likes_to_views_weight = 5  # Adjust the weight as needed
        subscribers_to_views_weight = 1  # Adjust the weight as needed
        
        sentiment_score = video['Average Sentiment']
        likes_to_views_ratio = video['Likes-to-Views Ratio']
        subscribers_to_views_ratio = video['Subscribers to Views Ratio']
        
        combined_score = (
            sentiment_weight * sentiment_score +
            likes_to_views_weight * likes_to_views_ratio +
            subscribers_to_views_weight * subscribers_to_views_ratio
        )
        
        return combined_score


    sorted_videos = sorted(data, key=calculate_combined_score, reverse=True)

    filtered_videos = [video for video in sorted_videos if video['Publish Year'] >= 2020]


    # Print the top 3 videos based on the combined score
    print("\nTop 3 Videos Based on Combined Score (Sentiment + Likes-to-Views Ratio + Subscribers to Views Ratio):")



    # Create an empty dictionary to store the video data
    video_data_dict = {}

    # Iterate through the filtered videos and convert each video's information into a dictionary
    for i, video in enumerate(filtered_videos[:3]):
        video_info_dict = {
            'Video Title': video['Video Title'],
            'Combined Score': calculate_combined_score(video),
            'Average Sentiment Score': video['Average Sentiment'],
            'Likes-to-Views Ratio': video['Likes-to-Views Ratio'],
            'Subscribers to Views Ratio': video['Subscribers to Views Ratio'],
            'Views': video['Views'],
            'Likes': video['Likes'],
            'Channel Name': video['Channel Name'],
            'Subscribers': video['Subscribers'],
            'Total Views (Channel)': video['Total Views (Channel)'],
            'Total Videos (Channel)': video['Total Videos (Channel)'],
            'Video Link': video['Video Link']
        }
        video_data_dict[f"Video {i + 1}"] = video_info_dict

    # Print the video data as a dictionary
    # print(video_data_dict)
    video_links = {video_name: {"Video Title": video_info["Video Title"], "Video Link": video_info["Video Link"]} for video_name, video_info in video_data_dict.items()}

    v1_link = video_links['Video 1']['Video Link']
    v1_title = video_links['Video 1']['Video Title']
    v2_link = video_links['Video 2']['Video Link']
    v2_title = video_links['Video 2']['Video Title']
    v3_link = video_links['Video 3']['Video Link']
    v3_title = video_links['Video 3']['Video Title']
    print("============================")
    print(v3_link)
    
    context = {
        'v1_link' : v1_link,
        'v2_link' : v2_link,
        'v3_link' : v3_link,
        'v1_title' : v1_title,
        'v2_title' : v2_title,
        'v3_title' : v3_title,
    }

        
    return render(request, 'findvideo.html', context)


def findcourse(request):
    # currentuser_email = request.user.email
    # currentuser_username = request.user.username
    # user_profile = OurUser.objects.get(email=currentuser_email,username=currentuser_username)
    
    search = ''

    if request.method == 'POST':
        search = request.POST.get('searchcourse', '')

    # Rest of your view logic
    # ...
    print(search)
    youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=api_key)

    # Your search query
    if search == "":
        search_query = 'Data Structure'
    else:
        search_query = search
    #youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=api_key)
    print(search_query)
    # if searchvideo == "":
    #     search_query = 'Data Structures and Algorithms'
    # else:    
    #     search_query = searchvideo
    
    #search_query = 'Data Structures and Algorithms'

    # Your search query for playlists
      # Change this to your desired topic

    # Maximum number of playlists to retrieve
    max_results = 5  # You can adjust this as needed

    data = []

    # Function to fetch likes and views for a video
    def get_likes_and_views(video_id):
        video_response = youtube.videos().list(
            part='statistics',
            id=video_id
        ).execute()

        video_info = video_response['items'][0]
        likes = video_info['statistics'].get('likeCount', 'N/A')
        views = video_info['statistics'].get('viewCount', 'N/A')

        return likes, views

    # Function to get channel subscribers count
    def get_channel_subscribers(channel_id):
        channel_response = youtube.channels().list(
            part='statistics',
            id=channel_id
        ).execute()

        channel_info = channel_response['items'][0]
        subscribers = channel_info['statistics'].get('subscriberCount', 'N/A')

        return subscribers

    # Function to check if the last video in the playlist is related to the topic
    def is_playlist_completed(playlist_id, topic_keywords):
        video_ids = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=1,  # Fetch only the last video
            fields='items(snippet/resourceId/videoId,snippet/title,snippet/description)'
        ).execute()

        if 'items' in video_ids:
            last_video = video_ids['items'][0]['snippet']
            video_id = last_video['resourceId']['videoId']
            video_title = last_video['title']
            video_description = last_video['description']
            
            # Check if the video title or description contains any of the topic keywords
            for keyword in topic_keywords:
                if keyword.lower() in video_title.lower() or keyword.lower() in video_description.lower():
                    return True
        
        return False

    # Make a request to search for playlists
    search_response = youtube.search().list(
        q=search_query,
        type='playlist',
        part='id',
        maxResults=max_results
    ).execute()

    # Extract playlist IDs from the search results
    playlist_ids = [item['id']['playlistId'] for item in search_response['items']]

    # Specify the keywords related to the topic of interest
    topic_keywords = ['last video','complete','last','full course', 'complete course', 'complete playlist','completed','finally','final','done']

    # Fetch and print playlist information for each playlist
    for playlist_id in playlist_ids:
        playlist_response = youtube.playlists().list(
            part='snippet',
            id=playlist_id
        ).execute()

        playlist_info = playlist_response['items'][0]
        title = playlist_info['snippet']['title']
        channel_name = playlist_info['snippet']['channelTitle']
        total_videos = playlist_info['snippet'].get('videoCount', 'N/A')
        playlist_link = f"https://www.youtube.com/embed/videoseries?si=pgviQYqXBbWo5SXc&amp;list={playlist_id}"  # Construct playlist link

        # Check if the playlist is completed for the topic
        playlist_completed = is_playlist_completed(playlist_id, topic_keywords)

        # Calculate likes-to-views ratio, total views, and channel subscribers to views ratio for the playlist
        video_ids = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=50  # Maximum number of videos to consider
        ).execute()
        
        total_likes = 0
        total_views = 0
        total_subscribers = 0  # Initialize total subscribers
        
        for video in video_ids['items']:
            video_id = video['snippet']['resourceId']['videoId']
            likes, views = get_likes_and_views(video_id)
            total_likes += int(likes) if likes != 'N/A' else 0
            total_views += int(views) if views != 'N/A' else 0
            
            # Fetch channel ID for the video
            channel_id = video['snippet']['channelId']
            subscribers = get_channel_subscribers(channel_id)
            total_subscribers += int(subscribers) if subscribers != 'N/A' else 0
        
        # Calculate likes-to-views ratio, total views, and channel subscribers to views ratio
        likes_to_views_ratio = total_likes / max(total_views, 1)  # Avoid division by zero
        
        # Calculate the accurate Channel Subscribers to Views Ratio
        channel_subscribers_to_views_ratio = total_subscribers / max(total_views, 1)  # Avoid division by zero

        data.append({
            'Playlist Title': title,
            'Channel Name': channel_name,
            'Total Videos': total_videos,
            'Playlist Link': playlist_link,
            'Likes-to-Views Ratio': likes_to_views_ratio,
            'Total Views': total_views,
            'Channel Subscribers to Views Ratio': channel_subscribers_to_views_ratio,
            'Playlist Completed': playlist_completed
        })

    # Print the top 3 playlists based on your criteria
    print("\nTop 3 Playlists Based on Your Criteria:")

    # Sort the playlists based on your criteria and select the top 3
    sorted_playlists = sorted(data, key=lambda x: (x['Likes-to-Views Ratio'], x['Total Views'], x['Channel Subscribers to Views Ratio']), reverse=True)[:3]

    # Create an empty list to store playlist data
    playlist_data = []

    # Iterate through the playlists and convert each playlist's information into a dictionary
    for i, playlist in enumerate(sorted_playlists):
        playlist_info_dict = {
            'Playlist Title': playlist['Playlist Title'],
            'Channel Name': playlist['Channel Name'],
            'Total Videos': playlist['Total Videos'],
            'Likes-to-Views Ratio': playlist['Likes-to-Views Ratio'],
            'Total Views': playlist['Total Views'],
            'Channel Subscribers to Views Ratio': playlist['Channel Subscribers to Views Ratio'],
            'Playlist Completed': 'Yes' if playlist['Playlist Completed'] else 'No',
            'Playlist Link': playlist['Playlist Link']
        }
        playlist_data.append(playlist_info_dict)

    # Create a dictionary to hold all playlist data
    output_dict = {
        'Top 3 Playlists': playlist_data
    }

    # Print the output dictionary
    playlist_data = []

# Iterate through the playlists and convert each playlist's information into a dictionary
    for i, playlist in enumerate(sorted_playlists):
        playlist_info_dict = {
        'Playlist Title': playlist['Playlist Title'],
        'Playlist Link': playlist['Playlist Link']
    }
        playlist_data.append(playlist_info_dict)

    title1 = playlist_data[0]['Playlist Title']
    link1 = playlist_data[0]['Playlist Link']
    title2 = playlist_data[1]['Playlist Title']
    link2 = playlist_data[1]['Playlist Link']
    title3 = playlist_data[2]['Playlist Title']
    link3 = playlist_data[2]['Playlist Link']
    
    
    context = {
        'title1' : title1,
        'link1' : link1,
        'title2' : title2,
        'link2' : link2,
        'title3' : title3,
        'link3' : link3,
    }
    return render(request, 'findcourse.html', context)