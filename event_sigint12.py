# -*- coding: utf-8 -*-
"""
c4sh event config
=================

You'll create one of these files per event. It contains certain
constants used by the software for this event. c4sh can only have
one event loaded at a time.
When you change this file in production, remember to restart all
python processes or else the changes won't be in effect.
"""

# Short name of your event
EVENT_NAME_SHORT = 'SIGINT12'

# Unix-friendly name of your event (lowercase, a-z0-9)
EVENT_NAME_UNIX = 'sigint12'

# Official name of your event
EVENT_NAME = 'SIGINT 2012'

# Postal address of host (for invoices)
EVENT_INVOICE_ADDRESS = "CCC Veranstaltungs GmbH\n" + \
                        "Wurststraße 23\n" + \
                        "01234 Berlin"

# Your name (yes, your name. You, the one setting up this software!)
# It makes sense to include real-time contact information suitable
# for your event (i.e. a DECT number if you have a POC).
EVENT_C4SH_SUPPORT_CONTACT = "Your Name, DECT 1234, +49123456789, <your@mail>"

# Do you have preorders (see c4sh.preorder.models)?
EVENT_PREORDERS = True

# Do you have receipt printers?
EVENT_RECEIPTS = True

# Do you have invoice printers?
EVENT_INVOICES = False

# Do you have cash drawers (see documentation for configuration howto)?
EVENT_DRAWER = False

# Supervisor information
EVENT_DASHBOARD_TEXT = "Here be important event-related supervisor information.<br />" + \
                       "You can define this text in EVENT_DASHBOARD_TEXT."

# Supervisor IPs
EVENT_SUPERVISOR_IPS = ('127.0.0.1', '172.17.0.1',)

# Printer related settings
'''
Printers used at CCC events: EPSON TM-88IV

42 fixed width chars
'''

# Printed on each session end
EVENT_RECEIPT_SESSION_ENDED = """
  -----------------------------------------
  -----------------------------------------
  -----------------------------------------

           Your session has ended.
        Please inform your supervisor!

  -----------------------------------------
  -----------------------------------------
  -----------------------------------------




"""

# Printed on each receipt before any sales postion
EVENT_RECEIPT_POS_LIST_HEADER = """ Ticket                                EUR
 -----------------------------------------
"""

EVENT_RECEIPT_SEPERATOR = " -----------------------------------------\r\n"

# DO NOT CHANGE :-)
# Receipt printer header (default is the logo that is flashed into the printer)  
EVENT_RECEIPT_HEADER = "\x1d\x28\x4c\x06\x00\x30\x45\x30\x30\x01\x01\r\n"

# Address on receipt. Automaticaly centered.
EVENT_RECEIPT_ADDRESS = """
            Chaos Computer Club
       Veranstaltungsgesellschaft mbH
             Postfach 000 00 0
               10000 Berlin

"""

# Receipt printer footer
EVENT_RECEIPT_FOOTER = """

    Leistungsdatum gleich Rechnungsdatum
               Vielen Dank!

        AG Charlottenburg, HRB 12345
            USt-ID: DE12345677
"""

# Localized receipt number description, must have %d format specifier
EVENT_RECEIPT_SERIAL_FORMAT = "              Belegnummer: %d\r\n"

# Localized receipt sum excl. sales tax, must have %s format specifier
EVENT_RECEIPT_TOTAL_EXCL_TAX_FORMAT = "                      Nettosumme:  %s\r\n"

# Localized receipt sum excl. sales tax, must have 3 %s format specifiers. first %s is actual tax rate (eg. 19)
# second %s is tax identifier (eg A), third %s is tax amount
EVENT_RECEIPT_SALES_TAX_FORMAT = "                    MwSt %(tax_rate)s%% (%(tax_identifier)s):  %(tax_amount)s\r\n" 

# Localized receipt total, must have %s format specifier
EVENT_RECEIPT_TOTAL_FORMAT = "                           Summe:  %s\r\n"

# Localized receipt total, must have 2 %s format specifiers. first date, second cashdesk identifier
EVENT_RECEIPT_TIMESTAMP_FORMAT = "            %(timestamp)s %(cashdesk_identifier)s\r\n"
