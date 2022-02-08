import os
import time
from datetime import datetime
from datetime import timedelta

from facebook_scraper import get_posts, get_group_info
from io import open
import shutil

POSTS_PATH = '/posts'


def write_post_data_to_file(path, post, count):
    if post['text'] != "":
        out_file = open(path + "/" + str(post['username']) + "_" + str(count) + ".txt", mode="w+", encoding="utf-8")
        try:
            out_file.writelines("Username: " + str(post['username']) + "\n")
            out_file.writelines("Post_url: " + str(post['post_url']) + "\n")
            out_file.writelines(
                "Text: " + str(post['text'].encode('utf-8', 'ignore').decode("utf-8")) + "\n")
            try:
                out_file.writelines("Date: " + str(post['time']) + "\n")
            except Exception as e1:
                out_file.writelines("Date: None\n")
            out_file.writelines("Likes: " + str(post['likes']) + "\n")
            out_file.writelines("Comments: " + str(post['comments']) + "\n")
            out_file.writelines("Shares: " + str(post['shares']) + "\n")
            out_file.close()
            count += 1
        except Exception as e1:
            print("ERROR: ", e1)
            file = out_file.name
            out_file.close()
            os.remove(file)
    return count


def is_group(id):
    try:
        get_group_info(id, cookies="cookies.json")
        return True
    except:
        return False


def posts_and_commenters(users, current_depth, max_depth, post_per_page, users_to_add_each_iteration, folder_path):
    print("Depth = ", current_depth, '/', max_depth)
    users_id = []

    path = os.path.join(folder_path, 'depth_' + str(current_depth).zfill(2))
    if not os.path.exists(path):
        os.mkdir(path)
    if current_depth >= 2:
        parent_depth = current_depth-1
        parent_folder_path = os.path.join(folder_path, 'depth_' + str(parent_depth).zfill(2))
        parent_files = os.listdir(parent_folder_path)
        for file_name in parent_files:
            shutil.copy2(os.path.join(parent_folder_path, file_name), path)

    for user in users:
        print("user: ", user)
        count = 1
        if is_group(user):
            posts = get_posts(group=user, pages=2 * post_per_page, extra_info=True, options={"comments": True},
                              cookies="cookies.json")
        else:
            posts = get_posts(account=user, pages=2 * post_per_page, extra_info=True, options={"comments": True},
                              cookies="cookies.json")
        for post in posts:
            try:
                if count <= post_per_page:
                    count = write_post_data_to_file(path, post, count)
                else:
                    break
                time.sleep(10)  # 10s
            except Exception as ex:
                print("ERROR:", ex)
                time.sleep(3600)    # 1h
                print(str(datetime.now() + timedelta(minutes=60)))
                pass

            for comment in post['comments_full'][:users_to_add_each_iteration]:
                users_id.append(comment['commenter_id'])
    if current_depth < max_depth:
        print("done user collected", len(users_id), "users!")
        posts_and_commenters(set(users_id[:users_to_add_each_iteration]), current_depth + 1, max_depth, post_per_page,
                             users_to_add_each_iteration, folder_path)


def main(posts_path):
    users = ['شباب-الناصرة-ضد-التجنيد-471403769637849',
             'شبيبة-عيلبون-مع-التجنيد-צעירי-עיילבון-בעד-גיוס-העדה-הנוצרית-411973295600587',
             'شبيبة-معليا-مع-التجنيد-צעירי-מעיליא-בעד-גיוס-העדה-הנוצרית-615445638492146',
             '951427798526855',
             '171810053014040']

    for user in users:
        folder_path = os.path.join(posts_path, str(user))
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
        posts_and_commenters([user],
                             current_depth=1,
                             max_depth=2,
                             post_per_page=100,
                             users_to_add_each_iteration=5,
                             folder_path=folder_path)


if __name__ == '__main__':
    posts_path = os.getcwd()
    posts_path = os.path.join(posts_path, 'posts')
    if not os.path.exists(posts_path):
        os.mkdir(posts_path)
    main(posts_path)
