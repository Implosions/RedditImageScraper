import requests, shutil, os.path, sys, argparse

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("subreddit", help = "The subreddit to download images from")
arg_parser.add_argument("sort", help = "top, hot, rising, new, random, controversial")
arg_parser.add_argument("time", help = "year, month, week, day, hour, all")
arg_parser.add_argument("limit", type=int, help = "The number of posts to scrape images from (from 25 to 100)")
arg_parser.add_argument("-d", "--dir", help="The directory to save the images to")
sortParams = {'top', 'hot', 'new', 'rising', 'controversial', 'random'}
timeParams = {'hour', 'day', 'week', 'month', 'year', 'all'}

def download(subreddit, sort, time, limit, savedir=os.getcwd()):
    url = "https://www.reddit.com/r/" + subreddit + ".json"
    data = ""
    headers = {'user-agent': 'RedditImageScraper Version 1.0.0'}
    p = {'sort': sort, 't': time, 'limit': limit}
    
    r = requests.get(url, headers=headers, params=p)

    data = r.json()

    count = 1
    for i in data["data"]["children"]:
        try:
            imageurl = i["data"]["url"]
            r = requests.get(imageurl, stream=True)
            tokens = r.headers['content-type'].split("/")
            ext = ""
            if tokens[0] == "image":
                urltokens = imageurl.split("/")
                name = urltokens[-1]
                filepath = os.path.join(savedir, name)

                with open(filepath, "wb") as imgfile:
                    imgfile.write(r.content)
                    imgfile.close()
                print("Saved image: " + imageurl)

                count += 1
        except Exception as e:
            print("Error saving image: " + imageurl)
    print("\n" + str(count) + " images downloaded")

# Driver
args = arg_parser.parse_args()

if not args.sort in sortParams:
	print("Error! Unrecognized sort parameter")
	exit()
if not args.time in timeParams:
	print("Error! Unrecognized time parameter")
	exit()
if not args.limit >= 25 and args.limit <= 100:
	print("Error! Limit must be a number from 25 to 100")
	exit()
if not args.dir == None:
	if not os.path.isdir(args.dir):
		print("Error! Invalid save directory")
		exit()
	else:
		download(args.subreddit, args.sort, args.time, args.limit, args.dir)
else:
	download(args.subreddit, args.sort, args.time, args.limit)
	
print("Completed!")