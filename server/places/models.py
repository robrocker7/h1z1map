from django.db import models

class Place(models.Model):

    """Place Object for displaying non-player locations."""

    class Category(object):

        """Place Categories."""
        
        BASE = 0
        HOUSE = 1
        INDUSTRY = 2
        CAR = 3
        STASH = 4


    lat = models.FloatField()
    lng = models.FloatField()
    name = models.CharField(max_length=36)
    icon_string = models.CharField(max_length=36)
    color = models.CharField(max_length=6)
    category = models.IntegerField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def get_bound_data(self):
        return {
            'id': self.id,
            'lat': self.lat,
            'lng': self.lng,
            'name': self.name,
            'maki-icon': self.icon_string,
            'color': self.color,
            'category': self.category
        }