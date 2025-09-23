from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone

NIB_SIZE = (
  ('EF', 'Extra Fine'),
  ('F', 'Fine'),
  ('M', 'Medium'),
  ('B', 'Bold'),
  ('S', 'Stub'),
)

NIB_MATERIAL = (
  ('SS', 'Stainless Steel'),
  ('G14', 'Gold 14k'),
  ('G18', 'Gold 18k'),
  ('G21', 'Gold 21k'),
  ('T', 'Titanium'),
  ('P', 'Platinum'),
  ('B', 'Bronze'),
  ('G', 'Glass'),
)

INK_FILL_MECHANISM = (
  ('CA', 'Cartridge'),
  ('CO', 'Cartridge-Converter'),
  ('P', 'Piston-Fill'),
  ('V', 'Vacuum-Fill'),
)

SIZE = (
  ('B', 'Bottle'),
  ('S', 'Sample'),
)

class Ink(models.Model):
  brand = models.CharField(max_length=100)
  name = models.CharField(max_length=100)
  color = models.CharField(max_length=20)
  shimmer = models.BooleanField(default=False)
  sheen = models.BooleanField(default=False)
  size = models.CharField(
    max_length=1,
    choices=SIZE,
    default=SIZE[0][0]
  )
  acquired_date = models.DateField('Acquired Date', default=timezone.now)
  hex_code = models.CharField(max_length=7, default="#000000")
  swatch_img = models.ImageField(upload_to="swatches/", blank=True, null=True)
  notes = models.TextField(blank=True, null=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return f"{self.brand} {self.name}"
  
  def save(self, *args, **kwargs):
    if self.brand:
      self.brand = self.brand.strip().title()
      super().save(*args, **kwargs)
  
  def get_absolute_url(self):
    return reverse('ink-detail', kwargs={'ink_id': self.id})
  
  def days_owned(self):
    return (timezone.now().date() - self.acquired_date).days
  
class PenInkLog(models.Model):
  pen = models.ForeignKey("Pen", on_delete=models.CASCADE, related_name="ink_logs")
  ink = models.ForeignKey("Ink", on_delete=models.CASCADE, related_name="pen_logs")
  date_inked = models.DateField('Date Inked', default=timezone.now)
  date_cleaned = models.DateField('Date Cleaned', null=True, blank=True)

  @property
  def days_inked(self):
    end_date = self.date_cleaned or timezone.now().date()
    days = (end_date - self.date_inked).days
    return max(1, days)

  class Meta:
    ordering = ['-date_inked']

class Pen(models.Model):
  brand = models.CharField(max_length=100)
  model = models.CharField(max_length=100)
  nib_size = models.CharField(
    max_length=2,
    choices=NIB_SIZE,
    default=NIB_SIZE[0][0]
  )
  nib_material = models.CharField(
    max_length=3,
    choices=NIB_MATERIAL,
    default=NIB_MATERIAL[0][0]
  )
  ink_fill = models.CharField(
    max_length=2,
    choices=INK_FILL_MECHANISM,
    default=INK_FILL_MECHANISM[0][0]
  )
  acquired_date = models.DateField('Acquired Date', null=True, blank=True)
  notes = models.TextField(blank=True, null=True)

  user = models.ForeignKey(User, on_delete=models.CASCADE)

  inks = models.ManyToManyField(Ink, blank=True)

  def __str__(self):
    return f"{self.brand} {self.model} ({self.nib_size})"

  def get_absolute_url(self):
    return reverse('pen-detail', kwargs={'pen_id': self.id})