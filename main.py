import os
from datetime import datetime
from facebook_scraper import get_posts
from io import open


def posts_and_commenters(users, depth , post_per_page, users_to_add_each_iteration):
    print("Depth = ", depth)
    users_id = []
    for user in users:
        print("user: ", user)
        count = 1
        for post in get_posts(user, pages=2*post_per_page, extra_info=True, options={"comments": True}, cookies="cookies.json"):
            print("new post")
            try:
                if count <= post_per_page:
                    if post['text'] != "":
                        print("post_id",post['post_id'])
                        out_file = open("posts/" + str(post['username']) + "_" + str(count) + ".txt", mode="w+", encoding="utf-8")
                        out_file.writelines("Username: " + str(post['username']) + "\n")
                        out_file.writelines("Post_id: " + str(post['post_id']) + "\n")
                        out_file.writelines("Text: " + str(post['text'].encode('utf-8','ignore').decode("utf-8")) + "\n")
                        try:
                            out_file.writelines("Date: " + str(datetime.fromtimestamp(post['timestamp'])) + "\n")
                        except Exception as e1:
                            out_file.writelines("Date: None\n")
                        out_file.writelines("Likes: " + str(post['likes']) + "\n")
                        out_file.writelines("Comments: " + str(post['comments']) + "\n")
                        out_file.writelines("Shares: " + str(post['shares']) + "\n")
                        out_file.close()
                        count += 1
                else:
                    break
            except Exception as e1:
                print("ERROR: ", e1)
                file = out_file.name
                out_file.close()
                os.remove(file)
            for comment in post['comments_full'][:users_to_add_each_iteration]:
                users_id.append(comment['commenter_id'])
    if depth > 0:
        print("done user collected", len(users_id), "users!")
        posts_and_commenters(set(users_id[:users_to_add_each_iteration]), depth-1, post_per_page, users_to_add_each_iteration)


posts_and_commenters(['Netanyahu'], depth=2 , post_per_page=10, users_to_add_each_iteration=5)
