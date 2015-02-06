from datetime import timedelta

from django.db import models

from server.lib.utils import get_now_datetime_cst


class Move(models.Model):
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)
    heading = models.FloatField(blank=True, null=True)
    life = models.IntegerField(db_index=True)

    def get_bound_data(self):
        return {
            'lat': self.lat,
            'lng': self.lng,
            'heading': self.heading,
            'life': self.life,
            'id': self.id,
        }


class Player(models.Model):

    """
    Player Object used for displaying markers on the map.
    """

    character_name = models.CharField(max_length=64, db_index=True, unique=True)
    color = models.CharField(max_length=6, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(blank=True, null=True, db_index=True)
    current_life = models.IntegerField(default=1)
    moves = models.ManyToManyField(Move)

    def save(self, *args, **kwargs):
        """Save object with central time."""
        self.last_updated = get_now_datetime_cst()
        super(Player, self).save(*args, **kwargs)

    def login_session(self, request):
        """Login the user to the session."""
        request.session['character_id'] = self.id

    def get_moves_by_life(self, life):
        return self.moves.filter(life=life).order_by('-id')

    def get_current_life_moves(self):
        return self.get_moves_by_life(self.current_life)

    def get_paths(self):
        moves = self.get_current_life_moves()
        if len(moves) < 2:
            return []

        paths = []
        for i in range(len(moves)):
            if i == 0:
                continue

            try:
                last_move = moves[(i-1)]
            except KeyError:
                continue

            move = moves[i]
            if last_move.lat == move.lat and last_move.lng == move.lng:
                continue
            paths.append({
                    'start': {
                        'lat': last_move.lat,
                        'lng': last_move.lng,
                    },
                    'end': {
                        'lat': move.lat,
                        'lng': move.lng,
                    }
                })
        return paths

    def get_bound_data(self):
        """Return JSON format."""
        return {
            'id': self.id,
            'name': self.character_name,
            'color': self.color,
            'current_life': self.current_life,
            'current_life_moves': [m.get_bound_data() for m in self.get_current_life_moves()],
            'paths': self.get_paths(),
        }

    def add_move(self, lat, lng, heading):
        m = Move(lat=lat, lng=lng, heading=heading, life=self.current_life)
        m.save()
        self.moves.add(m)

    def death(self):
        self.current_life = self.current_life + 1

    @staticmethod
    def get_all_by_recent_activity(minutes=30):
        """Return all Players recently active."""
        central_now = get_now_datetime_cst()
        players = Player.objects.filter(last_updated__gte=(central_now - timedelta(minutes=minutes)))
        return players

    def __unicode__(self):
        """Return Name."""
        return self.character_name
