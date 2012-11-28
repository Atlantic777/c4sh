from django.db import models
from django.contrib.auth.models import User
#from c4sh.preorder.models import PreorderTicket
from c4sh.desk.models import SalePosition

class UserProfile(models.Model):
	"""
	This is the UserProfile model.
	It can be constructed using (django.contrib.auth.models.)User.get_profile().
	"""
	user = models.ForeignKey(User)

	supervisor_auth_code = models.CharField(max_length=64, unique=True, verbose_name="Superuser authentication code for special tickets, UUID", null=True, blank=True)

	created_by = models.ForeignKey(User, null=True, blank=True, verbose_name="User has been created by..", related_name="user_created_by")

	def __unicode__(self):
		return "%s" % self.user.username

class Ticket(models.Model):
	"""
	This is the Ticket model. It defines the various available ticket types.
	Please be aware that there cannot be an edit or delete function for this model.
	Instead, the software should create a copy of the Ticket instance and set the old
	one to deleted=True. That way, SalePosition references won't get fucked up.
	"""
	name = models.CharField(max_length=255, verbose_name="Ticket name (internal)")
	receipt_name = models.CharField(max_length=255, verbose_name="Ticket name (to show on receipt)")
	invoice_name = models.CharField(max_length=255, verbose_name="Ticket name (to show on invoice)")
	description = models.TextField(blank=True, null=True, verbose_name="Optional verbose description of the ticket type (internal)")

	sale_price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Ticket price (money to collect at cash desk)")
	invoice_price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Ticket price (to show on invoice and receipt -- including tax)")
	currency = models.CharField(max_length=3, default="EUR") # Enirely cosmetic right now, no conversations planned

	tax_rate = models.SmallIntegerField(default=19, verbose_name="Included tax rate in percent")
	rabate_rate = models.SmallIntegerField(default=0, verbose_name="Included instant rabate in percent")

	limit_timespan = models.BooleanField(default=False, verbose_name="Can this ticket only be sold within a certain timespan?")
	valid_from = models.DateTimeField(blank=True, null=True, verbose_name="Ticket can be sold from..")
	valid_until = models.DateTimeField(blank=True, null=True, verbose_name="Ticket can be sold until..")

	limit_supervisor = models.BooleanField(default=False, verbose_name="Does this ticket need supervisor authorization?")

	preorder_sold = models.BooleanField(default=False, verbose_name="Is this a ticket sold through preorder? (If so, it will not be displayed in the ticket list and can only be added with QRCode/UUID)")

	receipt_autoprint = models.BooleanField(default=True, verbose_name="Print a receipt for this ticket automatically?")
	receipt_advice = models.TextField(blank=True, null=True, verbose_name="Additional text to be printed on receipt when buying this ticket")

	invoice_autoprint = models.BooleanField(default=True, verbose_name="Print an invoice for this ticket automatically?")
	invoice_advice = models.TextField(blank=True, null=True, verbose_name="Additional text to be printed on invoice when buying this ticket")

	#valid_payment_types = models.ManyToManyField("PaymentType", verbose_name="Valid payment types")

	active = models.BooleanField(default=False, verbose_name="Is active (will show up in cashier frontend)?")
	deleted = models.BooleanField(default=False, verbose_name="Is deleted (won't show up in supervisor backend)?")

	def __unicode__(self):
		return "%s (%.2f %s)" % (self.name, self.sale_price, self.currency)

	def delete(self):
		# No real deletion here. See above.
		self.deleted = True
		self.active = False
		return super(self, Ticket).save()

	"""def is_preorderable(self):
		try:
			return PreorderTicket.objects.get(backend_id=self.pk)
		except PreorderTicket.DoesNotExist:
			return False"""

	class Meta:
		ordering = ['active', 'name', '-sale_price']

class Cashdesk(models.Model):
	"""
	Cashdesks
	"""
	name = models.CharField(max_length=255, unique=True, verbose_name="Unique identifier of that cashdesk (internal)")
	invoice_name = models.CharField(max_length=255, unique=True, verbose_name="Unique identifier of that cashdesk (to show on invoice, keep it short)")

	ip = models.IPAddressField(unique=True, verbose_name="IP Address of this cashdesk (for access control and receipt printers)")

	receipt_printer = models.BooleanField(default=True, verbose_name="Does this cashdesk have a receipt printer?")
	receipt_printer_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Receipt printer name (optional)")
	invoice_printer = models.BooleanField(default=True, verbose_name="Does this cashdesk have an invoice printer?")
	invoice_printer_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Invoice printer name (optional)")

	allow_supervisor = models.BooleanField(default=False, verbose_name="Allow supervisor login on this cashdesk?")
	active = models.BooleanField(default=False, verbose_name="Is this cashdesk enabled?")

	active_session = models.ForeignKey("CashdeskSession", related_name="active_session_set", unique=True, blank=True, null=True, verbose_name="Active CashdeskSession object (don't fill in)")

	def __unicode__(self):
		return "%s (%s)" % (self.name, self.ip)

	class Meta:
		ordering = ['name']

class CashdeskSession(models.Model):
	"""
	Sessions for Cashdesks -- without a session, a cashier can't do shit
	"""
	cashdesk = models.ForeignKey(Cashdesk, verbose_name="Cashdesk")
	cashier = models.ForeignKey(User, verbose_name="Cashier")
	supervisor_before = models.ForeignKey(User, related_name="supervised_before_cashdisksession_set", verbose_name="Supervisor (before session)")

	valid_from = models.DateTimeField(blank=False, null=False, verbose_name="Cashier can sell from..")
	valid_until = models.DateTimeField(blank=False, null=False, verbose_name="Cashier can sell until..")

	change = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Change the cashier has gotten before session start")

	day_passes_before = models.IntegerField(null=False, blank=False, verbose_name="Day passes before session")
	day_passes_after = models.IntegerField(null=True, blank=True, verbose_name="Day passes after session")

	full_passes_before = models.IntegerField(null=False, blank=False, verbose_name="Full passes before session")
	full_passes_after = models.IntegerField(null=True, blank=True, verbose_name="Full passes after session")

	parktickets_before = models.IntegerField(null=False, blank=False, verbose_name="Parktickets before session")
	parktickets_after = models.IntegerField(null=True, blank=True, verbose_name="Parktickets after session")

	is_logged_in = models.BooleanField(default=False, verbose_name="Is the cashier logged in at the cashdesk? (do not change manually)", editable=False)
	was_logged_in = models.BooleanField(default=False, verbose_name="Did the cashier ever log into this session? (do not change manually)", editable=False)

	drawer_sum = models.DecimalField(null=True, blank=True, max_digits=7, decimal_places=2, verbose_name="Amount of money in cash drawer after session")
	drawer_sum_ok = models.NullBooleanField(default=None, blank=True, null=True, verbose_name="Amount of money in cash drawer after session was okay")

	supervisor_after = models.ForeignKey(User, null=True, blank=True, related_name="supervised_after_cashdisksession_set", verbose_name="Supervisor (after session)")
	total = models.DecimalField(null=True, blank=True, max_digits=7, decimal_places=2, verbose_name="Actual winnings (after change)")

	notes = models.TextField(null=True, blank=True, verbose_name="Any additional notes for this cashdesk session")

	def get_reversed_positions(self):
		# fetch positions which sale is marked as not fulfilled and reversed
		positions_reversed = SalePosition.objects.filter(sale__session=self, sale__fulfilled=False, sale__reversed=True)
		positions_reversed_merged = {}
		total = 0
		for position in positions_reversed:
			if not positions_reversed_merged.get(position.ticket.pk):
				positions_reversed_merged[position.ticket.pk] = {
					'ticket': position.ticket,
					'amount': 1,
					'total': position.ticket.sale_price
				}
			else:
				positions_reversed_merged[position.ticket.pk]['amount'] += 1
				positions_reversed_merged[position.ticket.pk]['total'] = positions_reversed_merged[position.ticket.pk]['amount'] * positions_reversed_merged[position.ticket.pk]['ticket'].sale_price
			total = total + position.ticket.sale_price

		return {'positions': positions_reversed_merged, 'total': total}

	def get_merged_positions(self):
		# fetch positions which sale is marked as fulfilled and not reversed
		positions = SalePosition.objects.filter(sale__session=self, sale__fulfilled=True, sale__reversed=False)
		positions_merged = {}
		total = 0
		for position in positions:
			if not positions_merged.get(position.ticket.pk):
				positions_merged[position.ticket.pk] = {
					'ticket': position.ticket,
					'amount': 1,
					'total': position.ticket.sale_price
				}
			else:
				positions_merged[position.ticket.pk]['amount'] += 1
				positions_merged[position.ticket.pk]['total'] = positions_merged[position.ticket.pk]['amount'] * positions_merged[position.ticket.pk]['ticket'].sale_price

			total = total + position.ticket.sale_price

		return {'positions': positions_merged, 'total': total}

	def drawer_supposed_sum(self):
		return self.get_merged_positions()['total'] + self.change

	def __unicode__(self):
		return "#%d for %s at %s (%s - %s)" % (self.pk, self.cashier.username, self.cashdesk.name, self.valid_from, self.valid_until)

	class Meta:
		ordering = ['valid_from', 'cashdesk']

"""
class PaymentType(models.Model):
	name = models.CharField(max_length=255)
	is_cash = models.BooleanField(default=False, verbose_name="Does this payment type handle cash at the cashdesk?")

	def __unicode__(self):
		if self.is_cash:
			cash = "handles cash"
		else:
			cash = "no cash"
		return "%s (%s)" % (self.name, cash)

	class Meta:
		ordering = ['is_cash', 'name']
"""