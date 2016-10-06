# native imports
import sys
from random import shuffle

# project imports
import database
from resources import flexcon

# external imports
import sqlalchemy

ARG_DICT = {
	'username': 1,
	'password': 2,
	'database': 3
}

def args():
	return len(ARG_DICT)

def arg(arg_key):
	return sys.argv[ARG_DICT[arg_key]]

def check_args():
	return len(sys.argv) is len(ARG_DICT) + 1

# -- MAIN PROCESS --

# save output reference
out = flexcon.out

# assert valid arguments
if not check_args():
	out.write('<< ERROR: Bad arguments! >>')
	sys.exit(1)

# connect to the PSQL database via SQLAlchemy
out.write('Connecting to the database...', tentative=True, newline=False)
arg_user = arg('username')
arg_pass = arg('password')
arg_db = arg('database')
database.init_db(arg_user, arg_pass, arg_db)
session = database.Session
out.rewrite('Connected to the database.')

flashcards = session.query(database.Flashcard.question, database.Flashcard.answer, database.Flashcard.category, database.Flashcard.one_to_one).all()

opposite_flashcards = []
for flashcard in flashcards:
	if flashcard[3]:
		opposite_flashcards.append((flashcard[1], flashcard[0], flashcard[2], flashcard[3]))
flashcards.extend(opposite_flashcards)
shuffle(flashcards)

count = len(flashcards)
for number, flashcard in enumerate(flashcards):
	out.write("\n\nQUESTION {} OF {}".format(number + 1, count))
	out.write("Question:\t{}".format(flashcard[0]))
	raw_input("Your Answer:\t")
	out.write("Answer:\t\t{}".format(flashcard[1]))

