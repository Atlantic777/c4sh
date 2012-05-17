from os import system

def print_receipt(printer):
	# open drawer
	open_drawer(printer)
	
	return

def open_drawer(printer):
	return system("echo -e '\033p07y' | lpr -l -P %s" % printer)
