# native imports
import string
import sys

# project imports
import database
from resources import flexcon

# external imports
import sqlalchemy

ARG_DICT = {
	'username': 1,
	'password': 2,
	'database': 3,
	'file': 4
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

with open(arg('file')) as import_contents:
	category = None
	whitespace_to_replace = string.whitespace.replace(' ', '')
	
	for line in import_contents:
		if len(line) is 0:
			continue
		
		entry = line.strip(whitespace_to_replace)
		
		if len(entry) is 0:
			continue
		
		if entry[0] == '@':
			category = entry[1:]
		else:
			parsed_entry = entry.split('|')
			one_to_one = parsed_entry[0] == '1'
			question = parsed_entry[1]
			answer = parsed_entry[2]
			
			flashcard = database.Flashcard()
			flashcard.question = question
			flashcard.answer = answer
			flashcard.category = category
			flashcard.one_to_one = one_to_one
			
			try:
				session.add(flashcard)
				session.commit()
			except sqlalchemy.exc.IntegrityError:
				out.write('Skipped over duplicate entry.')
				session.rollback()

session.commit()
session.flush()

