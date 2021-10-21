import re
from facebook_scraper import get_posts

out_file = open(r"output.txt", "w+")

for post in get_posts('foxnews', pages=1, extra_info=True, options={"comments": True}):
    for it in post['comments_full']:
        print(it['commenter_id'])
        try:
            for i in get_posts(it['commenter_id'], pages=3, cookies="g.JSON"):
                print(i)
        except Exception as e:
            print("An exception occurred", e)

out_file.close()
