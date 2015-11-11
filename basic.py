from sys import * # Allows for command line algorithms, necessary for open_file()

tokens = [] # Things will be stored here after being recognized

def open_file(filename):
	data = open(filename, "r").read() # Reads from the file
	data += "<EOF>"
	return data

# Lex function - interprets the source file and identifies
# things. For example it will recognize 'preach'.
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

	# Runs for each character in the list
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
		
# Parse function - puts it all together
def parse(toks):
# Parse takes the completed tokens list as input.
# Using this list of recognized syntax, it parses
# the code, deciding what to do with each term.
	i = 0
	while(i < len(toks)):
		# Runs for each recognized term in the list
		if toks[i] + " " + toks[i+1][0:6] == "preach STRING" or toks[i] + " " + toks[i][0:3] == "preach NUM":# or toks[i] + " " + toks[i][0:4] == "preach EXPR":
			#elif toks[i+1][0:3] == "NUM":
			#	print(toks[i+1][4:])
			#elif toks[i+1][0:4] == "EXPR":
			#	print(toks[i+1][5:])
			#i += 2
			#if toks[i+1][0:6] == "STRING":
			print(toks[i+1][7:])
			#elif toks[i+1][0:3] == "NUM":
			#	print(toks[i+1][4:])
			print(toks)
			i += 2
			

# What happens when you run the program
def run():
	data = open_file(argv[1]) # Puts contents of .lang file into data
	toks = lex(data) # Sets toks equal to the completed tokens list
	parse(toks) # Runs the parse function on the tokens list
	
# Starts the program
run()
