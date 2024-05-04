import praw

#Linking program to our Reddit Developer Account to scrape posts & comments"
reddit = praw.Reddit(
    client_id="jU9lQ5ZNRqRV_VJ0MzhKaQ",
    client_secret="JIUYlpI18PiSeT5MgiGzSb9c3HYzaA",
    user_agent="CS172 my-app scraper",
)

subreddit = reddit.subreddit("HydroHomies") #subreddit name == "HydroHomies"
top_posts = subreddit.top(limit=10) #limits to 10 posts
new_posts = subreddit.new(limit=10)

#Print out details of first 10 posts in the HydroHomies subreddit
for post in top_posts:  #more details in praw documentation
    print("Title - ", post.title)
    print("ID - ", post.id)
    print("Author - ", post.author)
    print("URL - ", post.url)
    print("Score - ", post.score)
    print("Comment count - ", post.num_comments)
    print("Created - ", post.created_utc) #returns timestamp of post
    print()

print('----------')
post = reddit.submission(id="l0wpxj") #grabbing one of the ids of a post
comments = post.comments

for comment in comments[:2]: #grab first 2 comments of that specific post
    print("Printing comment...")
    print("Comment body - ", comment.body)
    print("Author - ", comment.author)
    print()

#print(reddit.read_only)

