from django.core.management.base import BaseCommand, CommandError
from backend.models import HonoraryMember
import csv
import datetime

class Command(BaseCommand):
	args = '<file file ...>'
	help = "Import Chaosnummern from office dump (first line should contain field definition)"

	# NOTE: THIS IS SPECIFIC FOR 29C3!
	# IF YOU ARE NOT ON 29C3 THIS IS NOT GOING TO WORK FOR YOU.

	# We're looking for VORNAME, NACHNAME, CHAOSNR, BEZBIS
	# BEZBIS can either be a date (DD.MM.YY) or "Dauerauftrag"
	# The date should not be more than 12 months older than 20.12.12.

	# Please note that we do not delete existing entries that 
	# are missing or unpaid. Should be fine though.

	def handle(self, *args, **options):
		debug = True if int(options['verbosity']) == 3 else False
		for importfile in args:
			self.stdout.write("Reading file %s\n" % importfile)

			csv_file = open(importfile)
			csv_reader = csv.reader(csv_file, delimiter=';')
			import_rows = 0
			i = 0
			row_definition = dict()
			for row in csv_reader:
				if i == 0:
					# First row.
					j = 0
					for x in row:
						row_definition[x] = j
						j += 1
					i += 1
					continue
				name = row[row_definition['VORNAME']] + " " + row[row_definition['NACHNAME']]
				chaosnr = row[row_definition['CHAOSNR']]
				paid = row[row_definition['BEZBIS']]
				is_paid = False

				if paid == "Dauerauftrag":
					is_paid = True
				else:
					try:
						paid_until = datetime.datetime.strptime(paid, "%d.%m.%Y")
					except:
						print "failed to parse %s" % paid
						continue
					if datetime.datetime.now() - paid_until < datetime.timedelta(360):
						# has been paid less than a year ago, which counts according to dodger
						is_paid = True
				if is_paid:
					try:
						honmem = HonoraryMember.objects.get(membership_number=chaosnr)
						print "Not importing (exists already) #%s: %s" % (chaosnr, name)
					except HonoraryMember.DoesNotExist:
						honmem = HonoraryMember(membership_number=chaosnr, full_name=name)
						if debug: 
							print "Importing #%s: %s" % (chaosnr, name)
						honmem.save()
						import_rows += 1
				else:
					if debug: 
						print "Not importing (unpaid) #%s: %s" % (chaosnr, name)
				i += 1
			
			i -= 1 # first row doesn't count
			self.stdout.write("Imported %d/%d entries.\n" % (import_rows, i))