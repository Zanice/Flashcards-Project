import re, sys

BACKUP_CHAR = '\x1b[A'
NON_WHITESPACE_REGEX = r'[\S]'
EMPTY_CHAR = ''
NEWLINE_CHAR  ='\n'
SPACE_CHAR = ' '

class Flexcon(object):
	def __init__(self):
		self.segment = EMPTY_CHAR
	
	def to_segment_top(self, line_count):
		self.write('\r', newline=False)
		for _ in range(line_count):
			self.write(BACKUP_CHAR, newline=False)
	
	def write(self, text, tentative=False, newline=True):
		end_char = NEWLINE_CHAR if newline else EMPTY_CHAR
		sys.stdout.write(text + end_char)
		sys.stdout.flush()
		self.segment = text + end_char if tentative else EMPTY_CHAR
	
	def rewrite(self, text, tentative=False, newline=True):
		segment = self.segment
		
		segment_line_count = segment.count(NEWLINE_CHAR)
		split_segment = segment.split(NEWLINE_CHAR)
		
		text_line_count = text.count(NEWLINE_CHAR)
		split_text = text.split(NEWLINE_CHAR)
		
		self.to_segment_top(segment_line_count)
		
		new_text = EMPTY_CHAR
		for line_num, line in enumerate(split_text):
			new_text += line
			if line_num < len(split_segment) and len(split_segment[line_num]) > len(line):
				new_text += SPACE_CHAR*(len(split_segment[line_num]) - len(line))
			if line_num != text_line_count:
				new_text += NEWLINE_CHAR
		
		self.write(new_text, tentative=tentative, newline=newline)

out = Flexcon()

