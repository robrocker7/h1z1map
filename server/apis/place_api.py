import logging

from server.common.service import api_wrapper, InvalidParameterError
from server.places.models import Place


@api_wrapper()
def get_all_places(request, *args, **kwargs):
    """Return all places to display."""
    places = Place.objects.all()
    return [p.get_bound_data() for p in places]


def verify_place_request(request, update=False):
    """Verify place object from request."""
    lat = request.GET.get('lat', None)
    lng = request.GET.get('lng', None)
    name = request.GET.get('name', None)
    icon_string = request.GET.get('maki_icon', None)
    color = request.GET.get('color', None)
    category = request.GET.get('category', 0)

    if lat is None:
        raise InvalidParameterError('GET `lat` required')

    if lng is None:
        raise InvalidParameterError('GET `lng` required')

    if name is None:
        raise InvalidParameterError('GET `name` required')

    if icon_string is None:
        raise InvalidParameterError('GET `icon_string` required')

    if color is None:
        raise InvalidParameterError('GET `color` required')

    ctx = {
        'lat': lat,
        'lng': lng,
        'name': name,
        'icon_string': icon_string,
        'color': color,
        'category': category
    }

    if update:
        uid = request.GET.get('id', 0)

        if uid is None:
            raise InvalidParameterError('GET `id` required')

        ctx['id'] = uid

    return ctx


@api_wrapper()
def add_place(request, *args, **kwargs):
    """Add a new Place."""
    place_info = verify_place_request(request)

    place = Place.objects.create(lat=place_info['lat'],
                                 lng=place_info['lng'],
                                 name=place_info['name'],
                                 icon_string=place_info['icon_string'],
                                 color=place_info['color'],
                                 category=place_info['category'])

    return place.get_bound_data()


@api_wrapper()
def update_place(request, *args, **kwargs):
    """Update a existing Place."""
    place_info = verify_place_request(request, update=True)

    try:
        place = Place.objects.get(place_info['id'])
    except Place.DoesNotExist:
        raise InvalidParameterError('GET `id` did not return a Place')

    place.lat = place_info['lat']
    place.lng = place_info['lng']
    place.name = place_info['name']
    place.icon_string = place_info['icon_string']
    place.color = place_info['color']
    place.category = place_info['category']
    place.save()

    return place.get_bound_data()

