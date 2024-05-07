import praw
import json
import os

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

if not os.path.exists('crawled_posts'):
    os.makedirs('crawled_posts')

# save Reddit post data to JSON file
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

# Iterate over top posts & print them
unique_posts = {}
post_num = 5
posts_collection = []
total_posts = 0
for subreddit_name in subreddits:
    subreddit = reddit.subreddit(subreddit_name)
    top_posts = subreddit.top(limit=10)  # Limits to 1,000 posts
    for post in top_posts:
        # If post is not a duplicate, save post to collection
        if post.id not in unique_posts:
            unique_posts[post.id] = 1
            total_posts += 1
            posts_collection.append(post)
            if total_posts % post_num == 0:
                file_name = f"crawled_posts/{total_posts // post_num}.json"
                save_posts_to_json(posts_collection, file_name)
                print(f"Post collection {total_posts // post_num} saved to {file_name}")
                posts_collection = []

# Save any remaining posts to a JSON file
if posts_collection:
    file_name = f"crawled_posts/{total_posts // post_num + 1}.json"
    save_posts_to_json(posts_collection, file_name)
    print(f"Post collection {total_posts // post_num + 1} saved to {file_name}")


print("FINISHED CRAWLING POSTS")
# print('----------')
# ppost = reddit.submission(id="l0wpxj")  # Grabbing one of the ids of a post
# comments = post.comments

# for comment in comments[:2]:  # Grab first 2 comments of that specific post
#     print("Printing comment...")
#     print("Comment body - ", comment.body)
#     print("Author - ", comment.author)
#     print()

#print(reddit.read_only)