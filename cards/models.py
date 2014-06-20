from django.db import models
from django.contrib import admin
from django.core.validators import RegexValidator

class CreditCard(models.Model):
	class Meta:
		verbose_name = "Credit Card"
		verbose_name_plural = "Credit Cards"

	CARD_TYPES = (
			('visa', 'Visa'),
			('mastercard', 'MasterCard'),
			('amex', 'Amex'),
			('discover', 'Discover'),
			('unknown', 'Unknown'),
			)

	MONTH_RANGE = [(i,i) for i in range(1,13)]
	YEAR_RANGE = [(i,i) for i in range(1999,2050)]

	card_type = models.CharField(max_length=50,
			choices=CARD_TYPES,
			default='unknown')

	card_holder = models.CharField(max_length=255, verbose_name="Card Holder", null=True, blank=True)
	card_number = models.CharField(max_length=16, verbose_name="Card Number", validators=[RegexValidator(regex='^.{13,16}$', message='Card invalid!', code='nomatch')])
	expiry_date_month = models.CharField(verbose_name="Expiration Date Month", null=True, blank=True, choices=MONTH_RANGE, max_length=2)
	expiry_date_year = models.CharField(verbose_name="Expiration Date Year", null=True, blank=True, choices=YEAR_RANGE, max_length=4)
	card_code = models.CharField(max_length=3, verbose_name="CVV", null=True, blank=True)

	unique_together = (("card_type","card_number"),)

	def __unicode__(self):
		return unicode(self.card_type + ' - ' + self.card_holder)

class CreditCardAdmin(admin.ModelAdmin):
	list_display = ['card_type', 'card_holder', 'card_number', 'expiry_date_month', 'expiry_date_year', 'card_code']
	list_filter = ['card_type', 'card_holder']
	search_fields = ['card_type', 'card_holder', 'card_number']
	readonly_fields = ('card_type',)


try:
	admin.site.register(CreditCard, CreditCardAdmin)
except Exception,e:
	print str(e)
	pass
