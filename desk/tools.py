from os import system
from os import path
import sys, subprocess
import c4sh.settings as settings
import image_tools

def gap(f):
	formatted_value = "%.2f" % float(f)
	return " "*(7-len(formatted_value))+"%.2f" % float(f)

def print_session_end_bon(printer):
	text = settings.EVENT_RECEIPT_SESSION_ENDED
	text += ("\r\n"*8) + "\x1D\x561"

	try:
		send_data_to_printer(text, printer)
	except:
		pass
	
	return

def print_receipt(sale, printer, do_open_drawer=True):
	# open drawer
	if do_open_drawer:
		open_drawer(printer)
	total_sum = 0
	positions = ""
	tax_rates = set()
	tax_sums = dict()
	tax_symbol = dict()

	for pos in sale.positions():
		if pos.ticket.invoice_price == 0:
			continue
		total_sum += pos.ticket.invoice_price
		current_tax_rate = pos.ticket.tax_rate
		tax_rates.add(current_tax_rate)
		if str(current_tax_rate) not in tax_sums:
			tax_sums.update({str(current_tax_rate):pos.ticket.invoice_price})
			tax_symbol.update({str(current_tax_rate):str(unichr(0x40+len(tax_rates)))})
		else:
			tax_sums[str(current_tax_rate)] += pos.ticket.invoice_price

		positions += " %s (%s)%s %s\r\n" % (pos.ticket.receipt_name, tax_symbol[str(current_tax_rate)], " "*(29-len(pos.ticket.receipt_name)), gap(pos.ticket.invoice_price))


	if total_sum == 0:
		return

	receipt = str(bytearray([0x1B,0x61,1]))
	receipt += settings.EVENT_RECEIPT_ADDRESS
	receipt += settings.EVENT_RECEIPT_SEPERATOR
	receipt += settings.EVENT_RECEIPT_POS_LIST_HEADER

	# print positions block
	receipt += positions
	receipt += settings.EVENT_RECEIPT_SEPERATOR

	# calculate total exluding taxes and amount of paid taxes for every tax rate
	sum_of_all_taxes = 0
	for a_tax in tax_rates:
		current_tax_sum = float(tax_sums[str(a_tax)])-float(tax_sums[str(a_tax)])/float(float(100+a_tax)/float(100))
		sum_of_all_taxes += current_tax_sum
		tax_sums[str(a_tax)] = current_tax_sum

	# print total excluding taxes
	receipt += settings.EVENT_RECEIPT_TOTAL_EXCL_TAX_FORMAT % gap(float(total_sum)-sum_of_all_taxes)

	# print actual tax rates and amounts
	for a_tax in sorted(list(tax_symbol))[::-1]:
		receipt += settings.EVENT_RECEIPT_SALES_TAX_FORMAT % {'tax_rate':str(a_tax), 'tax_identifier':tax_symbol[str(a_tax)], 'tax_amount':gap(tax_sums[str(a_tax)])}

	# print total
	receipt += settings.EVENT_RECEIPT_TOTAL_FORMAT % gap(total_sum)

	# footer
	receipt += settings.EVENT_RECEIPT_FOOTER
	receipt += settings.EVENT_RECEIPT_TIMESTAMP_FORMAT % {'timestamp':sale.time.strftime("%d.%m.%Y %H:%M"), 'cashdesk_identifier':sale.cashdesk.invoice_name}
	receipt += settings.EVENT_RECEIPT_SERIAL_FORMAT % (sale.pk)

	# newlines
	receipt += ("\r\n"*2)

	try:
		send_data_to_printer(image_tools.get_imagedata(settings.STATIC_ROOT + '/' + settings.EVENT_RECEIPT_HEADER), printer)
		send_data_to_printer(receipt, printer)
		send_data_to_printer(image_tools.get_imagedata(settings.STATIC_ROOT + '/sigint13-printad.png'), printer)
		send_data_to_printer(bytearray([0x1D, 0x56, 66, 100]), printer) #cut
	except Exception, e:
		pass
	
	return

def send_data_to_printer(data, printer):
	lpr = subprocess.Popen(['/usr/bin/lpr', '-l', '-P', printer], stdin = subprocess.PIPE)
	lpr.stdin.write(data)
	lpr.stdin.close()

def open_drawer(printer):
	cmd = bytearray([0x1B,'p',48,255,255])
	send_data_to_printer(cmd, printer)
	return

