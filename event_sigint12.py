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

# Receipt printer header
EVENT_RECEIPT_HEADER = "Quittung"

# Receipt printer footer
EVENT_RECEIPT_FOOTER = "fnord!"

# Your name (yes, your name. You, the one setting up this software!)
EVENT_C4SH_SUPPORT_CONTACT = "zakx, DECT 2666, +4915140418284, <zakx@koeln.ccc.de>"

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