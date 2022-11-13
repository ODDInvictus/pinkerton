from django.db import models

from ibs.users.models import User


class ProductCategory(models.Model):
  name = models.CharField(max_length=512, verbose_name='Naam')
  image = models.ImageField(upload_to='product_categories', verbose_name='Afbeelding')

  class Meta:
    verbose_name = 'Productcategorie'
    verbose_name_plural = 'Productcategorieën'

  def __str__(self):
    return self.name


class Product(models.Model):
  name = models.CharField(max_length=512, verbose_name='Naam')
  category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name='Categorie')
  price = models.FloatField(verbose_name='Prijs')

  class Meta:
    verbose_name = 'Product'
    verbose_name_plural = 'Producten'

  def __str__(self):
    return f'{self.name} ({self.category})'


class AlcoholProduct(Product):
  alcohol_percentage = models.FloatField(verbose_name='Alcoholpercentage')
  volume = models.FloatField(verbose_name='Volume')

  class Meta:
    verbose_name = 'Alcohol-houdend product'
    verbose_name_plural = 'Alcohol-houdende producten'

  def __str__(self):
    return f'{self.name} ({self.category}), {self.alcohol_percentage}% alcohol, {self.volume}ml'


class Transaction(models.Model):
  """
  Class that represents a transaction, only here as a base class for other transactions
  """
  date = models.DateField(verbose_name='Datum', auto_now_add=True)
  description = models.CharField(max_length=512, verbose_name='Omschrijving')
  price = models.FloatField(verbose_name='Prijs', default=0.00)

  added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Toegevoegd door', related_name='added_by')
  user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Gebruiker')

  class Meta:
    verbose_name = 'Transactie'
    verbose_name_plural = 'Transacties'
    ordering = ['-date']

  def __str__(self):
    return f'{self.user.get_full_name()} heeft {self.price} betaald voor {self.description} op {self.date}'

  
class ContributionTransaction(Transaction):
  """
  Class that represents a contribution transaction for membership
  """
  class Meta:
    verbose_name = 'Contributie'
    verbose_name_plural = 'Contributies'

  def __str__(self):
    return f'{self.user.get_full_name()} heeft {self.price} betaald voor contributie op {self.date}'
  

class SaleTransaction(Transaction):
  """
  Class that represents a sale
  """
  product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Product')

  class Meta:
    verbose_name = 'Verkoop'
    verbose_name_plural = 'Verkopen'


class AlcoholSaleTransaction(Transaction):
  product = models.ForeignKey(AlcoholProduct, on_delete=models.CASCADE, verbose_name='Product')

  class Meta:
    verbose_name = 'Alcohol-verkoop'
    verbose_name_plural = 'Alcohol-verkopen'

  