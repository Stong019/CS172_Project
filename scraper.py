import praw
import requests
import os

# Save HTML content to a file
def save_html_to_file(url, file_path):
    response = requests.get(url)
    with open(file_path, 'wb') as file:
        file.write(response.content)

# Linking program to our Reddit Developer Account to scrape posts & comments
reddit = praw.Reddit(
    client_id="jU9lQ5ZNRqRV_VJ0MzhKaQ",
    client_secret="JIUYlpI18PiSeT5MgiGzSb9c3HYzaA",
    user_agent="CS172 my-app scraper",
)

# Initializing Subreddit Searching
subreddit = reddit.subreddit("AmIOverreacting")  # Subreddit name == "AmIOverreacting"
top_posts = subreddit.top(limit=10)  # Limits to 10 posts

# Create a directory to store crawled HTML pages if it doesn't exist
if not os.path.exists('crawled_pages'):
    os.makedirs('crawled_pages')

# Iterate over top posts & print them
unique_posts = {}
for post in top_posts:
    print("Title - ", post.title)
    print("ID - ", post.id)
    print("Author - ", post.author)
    print("URL - ", post.url)
    print("Score - ", post.score)
    print("Comment count - ", post.num_comments)
    print("Created - ", post.created_utc)
    print()

    # If post is not a duplicate, save it as html
    if post.id not in unique_posts:
        unique_posts[post.id] = 1  #Put post into dictionary/hashmap

        # Save HTML content to a file
        file_name = f"crawled_pages/{post.id}.html"
        save_html_to_file(post.url, file_name)

        print("HTML content saved to:", file_name)
        print('----------')

print('----------')
post = reddit.submission(id="l0wpxj")  # Grabbing one of the ids of a post
comments = post.comments

for comment in comments[:2]:  # Grab first 2 comments of that specific post
    print("Printing comment...")
    print("Comment body - ", comment.body)
    print("Author - ", comment.author)
    print()

#print(reddit.read_only)