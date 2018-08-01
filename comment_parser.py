import sqlite3


def main():
	conn = sqlite3.connect('comments.sqlite3')
	cursor = conn.execute('SELECT * from comments;')

	comments = []
	replies = []

	previous_comment = ""

	for row in cursor:
		if len(row[2]) <= 250:
			if row[1] == None:
				previous_comment = row[2]
			else:
				replies.append(row[2])
				comments.append(previous_comment)
				previous_comment = row[2]

	return comments, replies

	
if "__name__" == "main":
	main()