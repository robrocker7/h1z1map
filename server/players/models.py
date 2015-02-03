from datetime import timedelta

from django.db import models

from server.lib.utils import get_now_datetime_cst


class Player(models.Model):
    character_name = models.CharField(max_length=64, db_index=True, unique=True)
    color = models.CharField(max_length=6, blank=True, null=True)
    
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)
    heading = models.FloatField(blank=True, null=True)

    last_updated = models.DateTimeField(blank=True, null=True, db_index=True)


    def save(self, *args, **kwargs):
        """Save object with central time."""
        self.last_updated = get_now_datetime_cst()
        super(Player, self).save(*args, **kwargs)


    def login_session(self, request):
        """Login the user to the session."""
        request.session['character_id'] = self.id


    def get_bound_data(self):
        return {
            'id': self.id,
            'name': self.character_name,
            'color': self.color,
            'lat': self.lat,
            'lng': self.lng,
            'heading': self.heading
        }


    @staticmethod
    def get_all_by_recent_activity():
        central_now = get_now_datetime_cst()
        players = Player.objects.filter(last_updated__gte=(central_now - timedelta(minutes=30)))
        return players


    def __unicode__(self):
        return self.character_name