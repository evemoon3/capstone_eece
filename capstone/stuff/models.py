from django.db import models


"""
Point
- x: x coord
- y: y coord
- z: z coord
- is_realsense: bool, is it from realsense (true) or radar (false)
- created_at: datetime created could be used for filtering plots
- batch: batch num got from could also be use for identfiying which points should be in which plot
"""
class Point(models.Model):
  x = models.IntegerField()
  y = models.IntegerField()
  z = models.IntegerField()
  is_realsense = models.BooleanField()
  batch = models.IntegerField()
  created_at = models.DateTimeField(auto_now_add=True)

