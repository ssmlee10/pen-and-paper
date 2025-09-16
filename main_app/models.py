from django.db import models

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

class Pen(models.Model): 
  brand = models.CharField(max_length=100)
  model = models.CharField(max_length=100)
  nib_size = models.CharField(
    max_length = 2,
    choices = NIB_SIZE,
    default = NIB_SIZE[0][0]
  )
  nib_material = models.CharField(
    max_length = 3,
    choices = NIB_MATERIAL,
    default = NIB_MATERIAL[0][0]
  )
  ink_fill = models.CharField(
    max_length = 2,
    choices = INK_FILL_MECHANISM,
    default = INK_FILL_MECHANISM[0][0]
  )
  acquired_date = models.DateField(blank=True, null=True)
  notes = models.TextField(blank=True, null=True)

  def __str__(self):
    return f"{self.brand} {self.model} ({self.nib_size})"