from sys import * # Allows for command line algorithms, necessary for open_file()

tokens = [] # Things will be stored here after being recognized

def open_file(filename):
	data = open(filename, "r").read() # Reads from the file
	data += "<EOF>"
	return data

# Lex function - interprets the source file
# This returns a list of recognized syntax
def lex(filecontents):

	# Defining variables
	tok = ""
	state = 0
	isexpr = 0
	string = ""
	expr = ""
	n = 0

	# Splits contents of the file into chars in a list
	filecontents = list(filecontents)

	# For loop runs for each character in the list
	for char in filecontents:
		tok += char
		if tok == " ":
			# Runs if the character is a space
			if state == 0:
				# Removes the space if it is not within a string
				tok = ""
			else:
				# Does not remove the space if in a string
				tok = " "
		elif tok == "\n" or tok == "<EOF>":
			# Runs if it is a new line or the end of file
			if expr != "" and isexpr == 1:
				# Runs only if it is an expression
				tokens.append("EXPR:" + expr) # Adds the expression to tokens
				expr = "" # Resets expression
			elif expr != "" and isexpr == 0:
				# Runs if it is just a number
				tokens.append("NUM:" + expr) # Adds the number to tokens
				expr = "" # Resets expression
			tok = ""
		elif tok.upper() == "PREACH":
			# Runs if tok is preach, case insensitive
			tokens.append("preach") # Adds "preach" to tokens list
			tok = ""
		elif tok.isdigit():
			# Runs if the tok is a digit
			expr += tok # Adds digits into the expression
			tok = ""
		elif tok == "+":
			# Runs if an operator is present
			isexpr = 1 # Says it is an expression not just a number
			expr += tok # Adds any operator sign into expression
			tok = ""
		elif tok == "\"":
			# Runs if it is a "
			if state == 0:
				# Start of a string (first ")
				state = 1
			elif state == 1:
				# End of a string (second ")
				tokens.append("STRING:" + string + "\"") # Adds the full string into the tokens list
				string = "" # Empties string
				state = 0; # Ends the string
				tok = ""
		elif state == 1:
			# Runs for each character between quotes
			string += tok # Adds each char into the string
			tok = ""
	print(tokens) # Prints full list of recognized syntax
	return tokens # Returns full list of recognized syntax
		
# Parse function - takes the list of syntax
# from  lex and applies the defined action.
def parse(toks):
	i = 0
	# While loop runs for each term in the list
	while(i < len(toks)):

		# The following confusing if statement will run if it
			# recognizes any of the terms we defined for it
			# earlier, via the toks list. Then it will print
			# the correct part of the list item based on what
			# type it is, which it knows from the first part
			# of each list item.
		if toks[i] + " " + toks[i+1][0:6] == "preach STRING" or toks[i] + " " + toks[i+1][0:3] == "preach NUM" or toks[i] + " " + toks[i+1][0:4] == "preach EXPR":
			# Pretty confusing, this took me a while to get the list stuff right
			# The reason for starting the print at various locations is that
			# the first part of each item is the datatype (string, expr, num, etc)
			# followed by a colon. So you have to start the print after the colon.

			# If it is a string, print the string
			if toks[i+1][0:6] == "STRING":
				print(toks[i+1][7:])

			# If it is a number, print the number
			elif toks[i+1][0:3] == "NUM":
				print(toks[i+1][4:])

			# If it is an expression, print the expression
			elif toks[i+1][0:4] == "EXPR":
				print(toks[i+1][5:])
			i += 2
			

# What happens when you run the program
def run():
	data = open_file(argv[1]) # Puts contents of .lang file into data
	toks = lex(data) # Sets toks equal to the completed tokens list
	parse(toks) # Runs the parse function on the tokens list
	
# Starts the program
run()
