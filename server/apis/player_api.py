import logging

from server.common.service import api_wrapper, InvalidParameterError

from server.players.models import Player
from server.lib.utils import parse_loc_string


@api_wrapper()
def add_or_login_player(request, *args, **kwargs):
    name = request.GET.get('name', None)

    lat, lng, heading = parse_loc_string(name)
    if lat is not None or lng is not None or heading is not None:
        raise InvalidParameterError('Name should not evaluate as a location.')

    player, created = Player.objects.get_or_create(character_name=name)
    player.login_session(request)
    return player.get_bound_data()


@api_wrapper()
def get_all_players(request, *args, **kwargs):
    return [p.get_bound_data() for p in Player.get_all_by_recent_activity()]


@api_wrapper()
def get_player(request, *args, **kwargs):
    uid = request.GET.get('id', None)
    if uid is None:
        raise InvalidParameterError('GET param `id` is required')

    try:
        player = Player.objects.get(id=uid)
    except Player.DoesNotExist:
        raise InvalidParameterError('`id` did not find a player')

    return player.get_bound_data() 


@api_wrapper()
def update_player(request, *args, **kwargs):
    uid = request.GET.get('id', None)

    loc_string = request.GET.get('loc_string')
    color = request.GET.get('color', None)
    death = True if request.GET.get('death', 'false') == 'true' else False

    if uid is None:
        raise InvalidParameterError('GET param `id` is required')

    if loc_string is None:
        raise InvalidParameterError('GET param `loc_string` is required')

    if color is None:
        raise InvalidParameterError('GET param `color` is required')

    try:
        player = Player.objects.get(id=uid)
    except Player.DoesNotExist:
        raise InvalidParameterError('`id` did not find a player')


    lat, lng, heading = parse_loc_string(loc_string)
    logging.info('String: {0}'.format(loc_string))
    logging.info('Results: {0}, {1}, {2}'.format(lat, lng, heading))

    player.color = color
    if death:
        player.death()

    player.add_move(lat, lng, heading)
    player.save()

    return player.get_bound_data()


@api_wrapper()
def receive_screenshot(request, character_name, *args, **kwargs):
    image_data = request.FILES.get('screenshot', None)
    if image_data is None:
        raise InvalidParameterError('FILES param `screenshot` is required')

    try:
        character = Player.objects.get(character_name=character_name)
    except Player.DoesNotExist:
        raise InvalidParameterError('Player with name {0} DoesNotExist'.format(character_name))

    logging.info(image_data)
