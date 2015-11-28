import praw

# login info
userAgent = 'roochainche2cker v0.1:for discovering broken links in the chain of switcharoos for r/switcharoo.'
usersName = 'example'
usersPass = 'example'
# The user that should be messaged in case the bot goes wrong
userRunningBot = '/u/username'

# How many links the roobot will be going through (until it hits a broken link)
rooChainLength = 50

# Keep true if you want to submit the post to r/switcharoo, change to false
# If you want to print output locally. Useful for checking ouput before submitting.
submitError = False

# Tell reddit our user agent, login and retreive subreddit.
r = praw.Reddit(user_agent=userAgent)
subreddit = r.get_subreddit('switcharoo')
r.login(usersName, usersPass)

# This simply gets the first submission url in the switcharoo sub (that isn't META).
def getFirstSubmission():
	for submission in subreddit.get_new(limit = 5):
		if 'meta' not in submission.title.lower():
			firstSubmission = submission
			return firstSubmission.url
		else:
			continue

# The function to convert the url into something usable
backupURL = 'Blank'
tempURL = 'Blank'
def urlMagicConverter(link):
	global backupURL
	global tempURL
	if 'http' in link:
		try:
			urlToList = link.split('/')
			for i in urlToList:
				if 'http' in i:
					place = urlToList.index(i)
					placeID = place + 8
			urlToList[placeID] = urlToList[placeID][0:7]
			urlToList = urlToList[place:placeID+1]
			urlToList[place] = urlToList[place][-6:]
			urlToString = '/'.join(urlToList)
			tempURL = backupURL
			backupURL = urlToString
			return urlToString
		except:
			return link
	else:
		return link

# This is (hopefully) what happens if the bot encounters a broken link.
def failLink(link):
	global userRunningBot
	global testBool
	if submitError == True:
		r.submit('switcharoo', '[META](bot) Error found in the roo chain', text='[This switcharoo]({0}) seems to be broken. \n\nThe roo that links to the [broken roo is here.]({1}) \n\nGood luck on roohunting! (I am a bot, if there is an error with this bot, please message {2}).'.format(link, tempURL, userRunningBot))
	else:
		print('\n\nThis switcharoo: \n{0} \nSeems to be broken. \nThe roo that links to the broken roo is here: \n{1}\n\n'.format(link, tempURL))

# The function that gets the comment from the already converted URL.
def urlToCommentBody(link):
	switchSubmission = r.get_submission(url=link)
	comment = switchSubmission.comments[0].body
	return comment

# The part that gets repeated.
# Each iteration is another step through the old reddit switcharoo chain.
# Hopefully this will be carried out until the bot reaches a link that doesn't work.
def startChain(link):
	global getComment
	global backupURL
	global rooChainLength
	for i in range(1, rooChainLength):
		try:
			commentURL = urlMagicConverter(getComment)
			try:
				getComment = urlToCommentBody(commentURL)
			except:
				print(backupURL)
				print('Found an exception.')
				failLink(backupURL)
				break
	
		except:
			failLink(backupURL)
			break

# Get the first submission and it's comment.
link = urlMagicConverter(getFirstSubmission())
getComment = urlToCommentBody(link)
# Start the roochain.
startChain(link)






