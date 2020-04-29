import pandas as pd
from collections import Counter
import random


# TELEGRAM
telegram_handle = pd.read_csv('TELEGRAM.csv')
telegram_handle = list(telegram_handle['telegram_handle'])
for i in range(len(telegram_handle)):
	s = ''
	for j in telegram_handle[i].lower():
		if ord(j)>=97 and ord(j)<=122:
			s+=j
	telegram_handle[i] = s

data = []
for i in range(len(telegram_handle)):
	data.append([i+1,i+1,telegram_handle[i]])

data = pd.DataFrame(data, columns=['user_id','telegram_id','telegram_handle'])
data.to_csv('sanitize/telegram.csv',index=False)


# ORGANISATION
organisations = pd.read_csv('ORGANISATION.csv')
emails = []
for i in organisations.itertuples():
	e = i[2].replace(' ','')
	e = e.lower()
	emails.append(e+'@'+e+'.com')

organisations['email'] = emails
organisations.to_csv('sanitize/organisation.csv', index=False)


# USER
users = pd.read_csv('USER.csv')
organisation_id = [random.randint(1,50) for i in range(users.shape[0])] 
users['organisation_id'] = organisation_id
users.to_csv('sanitize/user.csv', index=False)


# BOARD_USER
user_id = []
for i in range(1,1001):
	for j in range(4):
		user_id.append(i)

board_id = [random.randint(1,50) for i in range(4*1000)]
data_ub = []
for i in range(4*1000):
	data_ub.append([user_id[i], board_id[i]])
x = pd.DataFrame(data_ub, columns=['user_id','board_id'])
x.to_csv('sanitize/user_board.csv', index=False)


# BOARD
board_admin = []
for i in range(1,51):
	for j in data_ub:
		if j[1]==i:
			board_admin.append(j[0])
			break

assert len(board_admin)==50

boards = pd.read_csv('BOARD.csv')
boards['board_admin_id'] = board_admin
boards.to_csv('sanitize/board.csv', index=False)


# MULTIMEDIA
objects = pd.read_csv('MULTIMEDIA.csv')
objects = list(objects['multimedia_object'])
multimedia_id = [i for i in range(1,801)]
m = []
for i in range(800):
	m.append([multimedia_id[i],objects[1]])
multimedia = pd.DataFrame(m, columns=['multimedia_id', 'multimedia_object'])
multimedia.to_csv('sanitize/multimedia.csv', index=False)


# LIST
lists = pd.read_csv('LIST.csv')

list_admin = []
board_id = []
for i in range(200):
	z = data_ub[random.randint(0,4000-1)]
	list_admin.append(z[0])
	board_id.append(z[1])

lists['list_admin_id'] = list_admin
lists['board_id'] = board_id
lists.to_csv('sanitize/list.csv',index=False)


# CARD
cards = pd.read_csv('CARD.csv')
list_id = []
card_admin = []
for i in range(1,201):
	for j in range(4):
		list_id.append(i)
		card_admin.append(list_admin[i-1])


cards['list_id'] = list_id
cards['card_admin_id'] = card_admin
cards['multimedia_id'] = [random.randint(1,800) for i in range(800)]
cards.to_csv('sanitize/card.csv', index=False)


# ANNOUNCEMENT
announcements = pd.read_csv('ANNOUNCEMENT.csv')
announcements['board_id'] = [i for i in range(1,51)]
announcements['user_id'] = board_admin
announcements['multimedia_id'] = [random.randint(1,800) for i in range(50)]
announcements.to_csv('sanitize/announcement.csv', index=False)


# CARD_COMMENT
card_comment = pd.read_csv('CARD_COMMENT.csv')
card_comment['card_id'] = [i for i in range(1,801)]
card_comment['user_id'] = card_admin
card_comment.to_csv('sanitize/card_comment.csv', index=False)

# DEADLINE
deadlines = pd.read_csv('DEADLINE.csv')
deadlines.to_csv('sanitize/deadline.csv', index=False)

#MOVE
#EMPTY