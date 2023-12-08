import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from textblob import TextBlob
import time
import tkinter as tk
from tkinter import scrolledtext
import sys

class CustomTextWidget:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, text):
        self.text_widget.insert(tk.END, text)

# Instructions for the user
# 1. Replace 'YOUR_YOUTUBE_API_KEY' with your actual YouTube Data API key.
# 2. Replace the 'video_url' with the YouTube video URL you want to analyze.
# 3. Customize the display_metrics function to show your desired metrics.

# Specify your YouTube Data API key
youtube_api_key = "YOUR_YOUTUBE_API_KEY"

# Extract video ID from the YouTube URL
video_url = "your video url"
video_id = video_url.split("v=")[1]

class YouTubeSentimentAnalysisUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Your Custom Sentiment Analysis App Title")  # Replace with your desired title
        self.create_widgets()

    def create_widgets(self):
        self.text_area = scrolledtext.ScrolledText(self.root, width=80, height=20)
        self.text_area.pack(pady=10)

        self.show_metrics_button = tk.Button(self.root, text="Show Metrics", command=self.show_metrics)
        self.show_metrics_button.pack(pady=10)

    def show_metrics(self):
        # Clear the text area
        self.text_area.delete(1.0, tk.END)

        # Create a custom stream object
        custom_text_widget = CustomTextWidget(self.text_area)

        # Replace the standard output with the custom stream object
        sys.stdout = custom_text_widget

        # Run the existing code to display metrics
        self.display_metrics()

        # Restore the standard output
        sys.stdout = sys.__stdout__

    def display_metrics(self):
        # Placeholder for user-specific metrics display
        print("Customize this part to display your own metrics.")

if __name__ == "__main__":
    # Call the function to get authenticated API service
    api_service = build('youtube', 'v3', developerKey=youtube_api_key)

    # Call the function to get video comments using the authenticated API service
    comment_params = {
        'part': 'snippet',
        'videoId': video_id,
        'textFormat': 'plainText',
        'key': youtube_api_key,
        'maxResults': 1000,
    }

    comments, replies_count = get_video_comments(api_service, **comment_params)

    # Analyze sentiments of the comments
    sentiment_comments = {
        'positive': [],
        'neutral': [],
        'negative': [],
    }

    for comment in comments:
        sentiment = analyze_sentiment(comment)
        sentiment_category = 'positive' if sentiment > 0.1 else 'neutral' if -0.1 <= sentiment <= 0.1 else 'negative'
        sentiment_comments[sentiment_category].append(comment)

    # ... (rest of the code)


    # Display individual comments and their sentiment scores
    for i, comment in enumerate(comments[:10]):  # Display sentiment scores for the first 10 comments
        sentiment = analyze_sentiment(comment)
        print(f"Comment {i + 1}: {comment}")
        print(f"Sentiment Score: {sentiment}")
        print()

    # Display totals and metrics
    print(f"Total comments: {len(comments)}")
    print()

    for sentiment, comments_list in sentiment_comments.items():
        print(f"{sentiment.capitalize()} comments ({len(comments_list)}):")
        for comment in comments_list:
            print(comment)
        print()

    # Display totals and metrics
    total_positive_comments = len(sentiment_comments['positive'])
    total_neutral_comments = len(sentiment_comments['neutral'])
    total_negative_comments = len(sentiment_comments['negative'])

    # Run the Tkinter UI
    app = YouTubeSentimentAnalysisUI()
    app.root.mainloop()
