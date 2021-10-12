import re
from facebook_scraper import get_posts

out_file = open(r"output.txt","w+")

for post in get_posts('FoxNews', pages=500):
    str1 = re.sub('[^A-Za-z0-9\'\"., ]+', '', post['text'])
    print(str(str1))
    out_file.writelines(str(str1))
    out_file.writelines("\n\n")

out_file.close()