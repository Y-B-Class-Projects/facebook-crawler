# facebook-crawler

Python script that downloads data from Facebook.
The script gets the first page from which to download posts and the script knows how to proceed to the pages of other users who wrote comments on the posts on that page.
Besides the script gets the depth of search, how many posts to download per page and how many users to collect from each page.
The script stores all the posts in separate files in the "posts" folder.
Since it is necessary to identify yourself with a Facebook user, a cookie file must be attached to the script with the user data (you can use the "editthiscookie" extension of Chrome)
