from os import system
import sys, subprocess

def gap(f):
	penis = "%.2f" % float(f)
	return " "*(5-len(penis))+"%.2f" % float(f)

def print_receipt(sale, printer, do_open_drawer=True):
	# open drawer
	if do_open_drawer:
		open_drawer(printer)
	logo = "\x1d\x28\x4c\x06\x00\x30\x45\x30\x30\x01\x01"
	summe = 0
	positions = ""
	for pos in sale.positions():
		if pos.ticket.invoice_price == 0:
			continue
		positions += " %s%s %s\r\n" % (pos.ticket.receipt_name, " "*(34-len(pos.ticket.receipt_name)), gap(pos.ticket.invoice_price))
		summe += pos.ticket.invoice_price

	if summe == 0:
		return

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
	mwst = float(summe)-float(summe)/float(1.19)
	receipt += "                  enthaltene MwSt:   %s\r\n" % gap(mwst)
	receipt += "                            Summe:  %s\r\n" % gap(summe)
	receipt += """

    Leistungsdatum gleich Rechnungsdatum
           Preise inkl. 19% MwSt
               Vielen Dank!

        AG Charlottenburg, HRB 71629
            USt-ID: DE203286729
"""
	receipt += "          %s %s\r\n" % (sale.time.strftime("%d.%m.%Y %H:%M"), sale.cashdesk.invoice_name)
	receipt += "              Belegnummer: %d\r\n" % (sale.pk)


	receipt += ("\r\n"*8) + "\x1D\x561"
	lpr = subprocess.Popen(['/usr/bin/lpr', '-l', '-P', printer], stdin = subprocess.PIPE)

	lpr.stdin.write(receipt)
	lpr.stdin.close()
	
	return

def open_drawer(printer):
	print "Opening drawer at printer %s" % printer
	return system("echo -e '\033p07y' | lpr -l -P %s" % printer)
