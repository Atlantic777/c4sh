from os import system
import sys, subprocess

def print_receipt(sale, printer, do_open_drawer=True):
	logo = "\x1d\x28\x4c\x06\x00\x30\x45\x30\x30\x01\x01"
	summe = 0
	for pos in sale.positions():
		positions = " %s%s %.2f\r\n" % (pos.ticket.receipt_name, " "*(36-len(pos.ticket.receipt_name)), pos.ticket.invoice_price)
		summe += pos.ticket.invoice_price


	receipt = logo + """
	            Chaos Computer Club
	       Veranstaltungsgesellschaft mbH
	             Postfach 640 23 6
	               10048 Berlin

	 Ticket                                EUR
	 -----------------------------------------
	"""
	receipt += positions
	receipt += " -----------------------------------------\r\n"
	receipt += "                  enthaltene MwSt:   %.2f\r\n" % (float(summe)-float(summe)/1.19)
	receipt += "                            Summe:   %.2f\r\n" % float(summe)
	receipt += """

	    Leistungsdatum gleich Rechnungsdatum
	           Preise inkl. 19% MwSt
	               Vielen Dank!

	        AG Charlottenburg, HRB 71629
	            USt-ID: DE203286729
	"""
	receipt += "        %d.%d.%d - %d:%d %s\r\n" % (sale.time.day, sale.time.month, sale.time.year, sale.time.hour, sale.time.minute, sale.cashdesk.invoice_name)
	receipt += "            Belegnummer: %d\r\n" % (sale.pk)


	receipt += ("\r\n"*8) + "\x1D\x561"
	lpr = subprocess.Popen(['/usr/bin/lpr', '-l', '-P', printer], stdin = subprocess.PIPE)

	lpr.stdin.write(receipt)
	lpr.stdin.close()

	# open drawer
	if do_open_drawer:
		open_drawer(printer)
	
	return

def open_drawer(printer):
	print "Opening drawer at printer %s" % printer
	return system("echo -e '\033p07y' | lpr -l -P %s" % printer)
