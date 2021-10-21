from datetime import datetime

from facebook_scraper import get_posts


# out_file = open(r"output.txt", "w+")
# out_file.close()

def posts_and_commenters(users, max_depth):
    print("starting")
    users_id = []
    for user in users:
        print("user: ", user)
        count = 0
        for post in get_posts(user, pages=2, extra_info=True, options={"comments": True}, cookies="cookies.json"):
            print("post_id",post['post_id'])
            out_file = open(r"" + str(post['username']) + "_" + str(count), "w+")
            count += 1
            out_file.writelines("Username: " + str(post['username']) + "\n")
            out_file.writelines("Post_id: " + str(post['post_id']) + "\n")
            out_file.writelines("Text: " + str(post['text']) + "\n")
            try:
                out_file.writelines("Date: " + str(datetime.fromtimestamp(post['timestamp'])) + "\n")
            except Exception as e1:
                out_file.writelines("Date: None\n")
            out_file.writelines("Likes: " + str(post['likes']) + "\n")
            out_file.writelines("Comments: " + str(post['comments']) + "\n")
            out_file.writelines("Shares: " + str(post['shares']) + "\n")
            out_file.close()
            print("close file")
            print("comments")
            for comment in post['comments_full'][:5]:
                print(comment['commenter_id'])
                users_id.append(comment['commenter_id'])
            print("done user")
    if(max_depth > 0):
        print(users_id)
        posts_and_commenters(users_id, max_depth-1)


posts_and_commenters(['foxnews'], 2)
