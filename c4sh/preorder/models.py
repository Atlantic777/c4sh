from django.db import models
import uuid
from c4sh.backend.models import Ticket

# add UUIDField to south
from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^c4sh\.preorder\.models.UUIDField"])

class UUIDField(models.CharField) :
	"""
	Defining our custom UUIDField field for PreorderPositions
	""" 
	def __init__(self, *args, **kwargs):
		kwargs['max_length'] = kwargs.get('max_length', 64 )
		kwargs['blank'] = True
		models.CharField.__init__(self, *args, **kwargs)
	
	def pre_save(self, model_instance, add):
		if add :
			value = str(uuid.uuid4())
			setattr(model_instance, self.attname, value)
			return value
		else:
			return super(models.CharField, self).pre_save(model_instance, add)

"""
This data model was created to enable implementation of a preorder system and, foremost,
the import of such preorder-related data. One could easily build a standalone Django app
building on this data model or at least build a reasonable export using it.

Obviously there won't be any actual implementation of a preorder system within c4sh itself.
"""

class PreorderTicket(models.Model):
	"""
	This is the PreorderTicket model. It defines the various ticket types available for preorder.
	Please be aware that there cannot be an edit or delete function for this model.
	Instead, the software should create a copy of the Ticket instance and set the old
	one to deleted=True.
	"""
	name = models.CharField(max_length=255, verbose_name="Ticket name")
	backend_id = models.SmallIntegerField(verbose_name="Primary key of the corresponding Ticket object in backend (for export)")

	price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Ticket price including tax")
	currency = models.CharField(max_length=3, default="EUR") # Enirely cosmetic right now, no conversations planned

	tax_rate = models.SmallIntegerField(default=19, verbose_name="Included tax rate in percent")

	limit_timespan = models.BooleanField(default=False, verbose_name="Can this ticket only be sold within a certain timespan?")
	valid_from = models.DateTimeField(blank=True, null=True, verbose_name="Ticket can be sold from..")
	valid_until = models.DateTimeField(blank=True, null=True, verbose_name="Ticket can be sold until..")

	limit_amount = models.IntegerField(blank=True, null=True, verbose_name="How many tickets of this type may be sold?")
	limit_amount_user = models.IntegerField(blank=True, null=True, verbose_name="How many tickets of this type may be sold to a single user?")

	is_ticket = models.BooleanField(default=True, verbose_name="Is this a ticket to redeem at the cashdesk?") # This is the t-shirt option.

	active = models.BooleanField(default=False, verbose_name="Is active (will show up in cashier frontend)?")
	deleted = models.BooleanField(default=False, verbose_name="Is deleted (won't show up in supervisor backend)?")

	def __unicode__(self):
		return "%s (%.2f %s)" % (self.name, self.price, self.currency)

	def delete(self):
		# No real deletion here. See above.
		self.deleted = True
		self.active = False
		return super(self, Ticket).save()
	
	class Meta:
		ordering = ['active', 'name', '-price']

class PreorderPosition(models.Model):
	"""
	PreorderPositions are PreorderTickets.
	"""
	preorder = models.ForeignKey("Preorder")
	ticket = models.ForeignKey(PreorderTicket)
	uuid = UUIDField(unique=True, editable=False)
	redeemed = models.BooleanField(default=False)

	def get_backend_ticket(self):
		return Ticket.objects.get(pk=self.ticket.backend_id)

	def __unicode__(self):
		return "%s %s (%s)" % (self.uuid, self.preorder.unique_secret, self.preorder.username)

class Preorder(models.Model):
	"""
	The Preorder model holds the various preorders. 
	"""
	name = models.CharField(max_length=255, verbose_name="Name of buyer")
	username = models.CharField(max_length=255, verbose_name="Username of buyer")
	user_id = models.IntegerField(verbose_name="User id of buyer")
	additional_info = models.TextField(blank=True, null=True, verbose_name="Additional identifying information")
	unique_secret = models.CharField(max_length=255, unique=True, verbose_name="Unique secret to verify ticket ownership at cashdesk (e.g. barcode data)")

	#cached_sum = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Sale amount (cached)")
	cached_sum = models.TextField(verbose_name="Sale amount (cached) (json)") # As we "could" have multiple currencies in one preorder, this is a json string with all payment data cached
	time = models.DateTimeField(verbose_name="Time of sale")

	paid = models.BooleanField(default=False, verbose_name="Is this preorder paid?")
	paid_time = models.DateTimeField(blank=True, null=True, verbose_name="Time of payment acknowledgement")
	paid_via = models.CharField(max_length=30, blank=True, null=True, verbose_name="How was this paid for?")
