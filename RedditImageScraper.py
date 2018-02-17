import requests, time, shutil, os.path, sys

sortParams = {'top', 'hot', 'new', 'rising', 'controversial', 'random'}
timeParams = {'hour', 'day', 'week', 'month', 'year', 'all'}
sfp_flatfile = "savefilepath.txt"
helpMsg = """\nsubreddit: The name of the subreddit
sort parameters: 'top', 'hot', 'new', 'rising', 'controversial', 'random'
time parameters: 'hour', 'day', 'week', 'month', 'year', 'all'
limit: the number posts to return from 25 to 100\n"""

def hasValidSaveDir():
    if os.path.isfile(sfp_flatfile):
        try:
            if os.path.isdir(getSaveDir()):
                return True
        except:
            print("Error! Could not open " + sfp_flatfile)
    return False
    
def getSaveDir():
    with open(sfp_flatfile) as flatfile:
        filepath = flatfile.read()
        flatfile.close()
        return filepath

def addSaveDir():
    fp = input("Enter a directory to save the images to:\n")
    while(not os.path.isdir(fp)):
        fp = input("Error! Invalid directory, check the path and retry\n")
    
    with open(sfp_flatfile, "w") as flatfile:
        flatfile.write(fp)
        flatfile.close()

def download(subreddit, sort, time, limit):
    imgdir = getSaveDir()

    if not imgdir[-1] == "//":
        imgdir += "//"
    
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
                filepath = imgdir + name

                with open(filepath, "wb") as imgfile:
                    imgfile.write(r.content)
                    imgfile.close()
                print("Saved image: " + imageurl)

                count += 1
        except Exception as e:
            print("Error saving image: " + imageurl)
            
    print("\nCompleted: " + str(count) + " images downloaded\n")

# Driver
print("Reddit Image Scraper\nEnter 'help' to get help, enter 'exit' to exit.\n")

while(True):
    if not hasValidSaveDir():
        addSaveDir()
    
    userInput = input("Enter information to begin downloading:\n<subreddit> <sort> <time> <limit>\n\n")
    tokens = userInput.lower().split(" ")
    
    if len(tokens) == 1:
        if tokens[0] == "help":
            print(helpMsg)
        elif tokens[0] == "exit":
            exit()
    elif len(tokens) > 3:
        subreddit = tokens[0]
        sort = tokens[1]
        time = tokens[2]
        limit = tokens[3]
                
        if not sort in sortParams:
            print("Error! Unrecognized sort parameter")
            continue
        if not time in timeParams:
            print("Error! Unrecognized time parameter")
            continue
        try:
            if not int(limit) >= 25 and int(limit) <= 100:
                print("Error! Limit must be a number from 25 to 100")
                continue
        except ValueError:
            print("Error! Limit must be a number from 25 to 100")
            continue
        
        download(subreddit, sort, time, limit)
