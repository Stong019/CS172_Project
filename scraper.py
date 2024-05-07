import praw
import json
import os
from tqdm import tqdm  
import time
# Linking program to our Reddit Developer Account to scrape posts & comments
reddit = praw.Reddit(
    client_id="jU9lQ5ZNRqRV_VJ0MzhKaQ",
    client_secret="JIUYlpI18PiSeT5MgiGzSb9c3HYzaA",
    user_agent="CS172 my-app scraper",
)

# Ask user for the number of subreddits to scrape
num_subreddits = int(input("Enter the number of subreddits to scrape: "))

subreddits = []
# Ask user for subreddit names
for i in range(num_subreddits):
    subreddit_name = input(f"Enter name of subreddit {i + 1}: ")
    subreddits.append(subreddit_name)

# Ask user for the number of posts to scrape per subreddit
num_posts = int(input("Enter the number of posts to scrape per subreddit: "))

if not os.path.exists('crawled_posts'):
    os.makedirs('crawled_posts')

# Function to save Reddit post data to a JSON file
def save_posts_to_json(posts, file_path):
    data = []
    for post in posts:
        post_data = {
            "post_id": post.id,
            "author": str(post.author),
            "title": post.title,
            "url": post.url,
            "score": post.score,
            "num_comments": post.num_comments,
            "created_utc": post.created_utc,
            "selftext": post.selftext,
            "permalink": post.permalink,
            "comments": [comment.body for comment in post.comments if not isinstance(comment, praw.models.MoreComments)]
        }
        data.append(post_data)

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Function to scrape and save posts
def scrape_and_save_post(subreddit_name, num_posts):
    subreddit = reddit.subreddit(subreddit_name)
    top_posts = subreddit.top(limit=num_posts)
    posts_collection = []
    total_posts = 0
    progress_bar = tqdm(total=num_posts, desc=f"Scraping {subreddit_name}", bar_format="{l_bar}{bar:10}{r_bar}", colour='green')
    for post in top_posts:
        # Save post to collection if not a duplicate
        if post.id not in unique_posts:
            unique_posts[post.id] = 1
            total_posts += 1
            posts_collection.append(post)
        # Calculate sleep duration based on number of posts
        sleep_duration = min(0.1, 0.1 * num_posts)  # This lets us show the user the progress bar move over time, however if the number of posts is too large then we want to minimize time slept
        time.sleep(sleep_duration)
        progress_bar.update(1)

    # Quality of life update, After scraping all posts, save them into a single JSON file
    file_name = f"crawled_posts/{subreddit_name}.json"
    save_posts_to_json(posts_collection, file_name)
    print(f"All posts from {subreddit_name} saved to {file_name}")
    progress_bar.close()

unique_posts = {}
post_num = 10  # Number of posts per JSON file

# Iterate over each subreddit
for subreddit_name in subreddits:
    print(f"Fetching posts from subreddit: {subreddit_name}")
    scrape_and_save_post(subreddit_name, num_posts)

print("FINISHED CRAWLING POSTS")
