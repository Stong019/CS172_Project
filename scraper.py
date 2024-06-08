import praw
import json
import os
from tqdm import tqdm
import time

reddit = praw.Reddit(
    client_id="jU9lQ5ZNRqRV_VJ0MzhKaQ",
    client_secret="JIUYlpI18PiSeT5MgiGzSb9c3HYzaA",
    user_agent="CS172 my-app scraper",
)

num_subreddits = int(input("Enter the number of subreddits to scrape: "))

subreddits = []
for i in range(num_subreddits):
    subreddit_name = input(f"Enter name of subreddit {i + 1}: ")
    subreddits.append(subreddit_name)

num_posts = int(input("Enter the number of posts to scrape per subreddit: "))

if not os.path.exists('crawled_posts'):
    os.makedirs('crawled_posts')

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

unique_posts = {}
post_num = 10
posts_collection = []
total_posts = 0
posts_saved_for_subreddit = 0
current_subreddit = None

for subreddit_name in subreddits:
    subreddit_folder = os.path.join('crawled_posts', subreddit_name)
    if not os.path.exists(subreddit_folder):
        os.makedirs(subreddit_folder)

    print(f"Fetching posts from subreddit: {subreddit_name}")
    subreddit = reddit.subreddit(subreddit_name)
    top_posts = subreddit.top(limit=num_posts)

    progress_bar = tqdm(total=num_posts, desc=f"Scraping {subreddit_name}", bar_format="{l_bar}{bar:10}{r_bar}", colour='green')

    for post in top_posts:
        if post.id not in unique_posts:
            unique_posts[post.id] = 1
            total_posts += 1
            posts_saved_for_subreddit += 1
            posts_collection.append(post)
            if posts_saved_for_subreddit % post_num == 0:
                file_name = os.path.join(subreddit_folder, f"{posts_saved_for_subreddit // post_num}.json")
                save_posts_to_json(posts_collection, file_name)
                posts_collection = []
        sleep_duration = min(0.1, 0.1 * num_posts)
        time.sleep(sleep_duration)
        progress_bar.update(1)
    
    if posts_collection:
        file_name = os.path.join(subreddit_folder, f"{posts_saved_for_subreddit // post_num + 1}.json")
        save_posts_to_json(posts_collection, file_name)
        posts_collection = []

    posts_saved_for_subreddit = 0  
    progress_bar.close()

print("FINISHED CRAWLING POSTS")
