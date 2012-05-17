# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
import c4sh.backend.models as backend

class SalePosition(models.Model):
	"""
	Every SalePosition is a position of a Sale
	"""
	sale = models.ForeignKey("Sale")
	ticket = models.ForeignKey(backend.Ticket)
	sale_price = models.DecimalField(blank=True, null=True, max_digits=7, decimal_places=2, verbose_name="Manual override for Ticket price (money to collect at cash desk)")
	invoice_price = models.DecimalField(blank=True, null=True, max_digits=7, decimal_places=2, verbose_name="Manual override for Ticket price (to show on invoice and receipt -- including tax)")

	uuid = models.CharField(max_length=65, blank=True, null=True, verbose_name="Is this position derived by a preorder? If so, we save the UUID here")

	tax_rate = models.SmallIntegerField(blank=True, null=True, verbose_name="Manual override for included tax rate in percent")
	rabate_rate = models.SmallIntegerField(blank=True, null=True, verbose_name="Manual override for included instant rabate in percent")
	supervisor = models.ForeignKey(User, related_name="authorized_positions", blank=True, null=True, verbose_name="Supervisor authorizing this position")

class Sale(models.Model):
	"""
	Actual sales. Sales consist of one or more SalePositions.
	"""
	cashier = models.ForeignKey(User)
	cashdesk = models.ForeignKey(backend.Cashdesk)
	session = models.ForeignKey(backend.CashdeskSession)
	
	cached_sum = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Sale amount (cached)")

	time = models.DateTimeField()

	fulfilled = models.BooleanField(default=False, verbose_name="Has this sale been fulfilled?")
	reversed = models.BooleanField(default=False, verbose_name="Has this sale been reversed?")

	def positions(self):
		try:
			return SalePosition.objects.filter(sale=self)
		except SalePosition.DoesNotExist:
			return []

	def __unicode__(self):
		return "#%d: sum=%.2f, %d items (desk %s/%s/%s)" % (self.pk, self.cached_sum, len(SalePosition.objects.filter(sale=self)), self.cashdesk, self.cashier.username, self.time)
	


