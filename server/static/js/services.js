var Dialog = function() {
    var self = this;

    self.DIALOGS = {
        ADD_CHARACTER: 'add-player-container',
        UPDATE_LOCATION: 'update-player-container',
        ADD_PLACE: 'add-place-container'
    }

    self.show_dialog = function(dialog_id) {
        $('.map_overlay #player-action-container form').hide();
        if(dialog_id == self.DIALOGS.ADD_CHARACTER) {
            $('#player-action-container').hide();
            $('#add-player-container').show();
        } else {
            $('#player-action-container').show();
            $('#add-player-container').hide();
            $('#'+dialog_id).show();
            self.change_tab_action_state(dialog_id);
        }
    }

    self.change_tab_action_state = function(tab_id) {
        $('#player-action-container .list-group-item').removeClass('active');
        $('#player-action-container .list-group-item[data-tab="'+tab_id+'"]').addClass('active');
    }

    self.bind_events = function() {
        $('#player-action-container .list-group-item').on('click', function(e) {
            e.preventDefault();
            self.show_dialog($(this).attr('data-tab'));
        });
    }

    self.init = function() {
        self.bind_events();
        self.show_dialog(self.DIALOGS.ADD_CHARACTER);
    }
    self.init();
}

var dialog_api = new Dialog();

var Places = function(map) {
    var self = this;

    self.MAP = null;
    self.PLACE_MARKERS = {};
    self.PLACES = {};
    self.POLL = null;

    self.add_place_to_map = function(place) {

        switch(place['maki_icon']) {
            case 5:
                var icon_string = 'commercial';
                break;
            case 4:
                var icon_string = 'car';
                break;
            case 3:
                var icon_string = 'pharmacy';
                break;
            case 2:
                var icon_string = 'industrial';
                break;
            case 1:
                var icon_string = 'building';
                break;
            case 0:
            default:
                var icon_string = 'embassy';
                break;
        }

        var placeIcon = L.MakiMarkers.icon({
            icon: icon_string,
            color: "#"+place['color'],
            size: "m"
        });

        var location = convertLatLng(place['lat'], place['lng']);
        var latlng = new L.LatLng(location.lat, location.lng);
        var marker = L.rotatedMarker(latlng, {
                icon: placeIcon,
            }).bindPopup(place['name']).addTo(self.MAP);

        self.PLACE_MARKERS[place['id']] = marker;
    };

    self.clear_place_form = function() {
        $('#add-place-container input[name="loc"], #add-place-container input[name="name"]').val('');
    }

    self.add_place = function(loc_string, color, name) {
        $.get('/api/place/add/', {
                loc_string: loc_string,
                color: color,
                name: name
            }).done(function(json_response) {
                var place = json_response['result'];
                self.PLACES[place['id']] = place;
                self.add_place_to_map(place);
                self.clear_place_form();
            });
    };

    self.update_place = function(place){
        $.get('/api/place/update/', {
                id: place['id'],
                lat: place['lat'],
                lng: place['lng'],
                name: place['name'],
                icon_string: place['icon_string'],
                color: place['color'],
                category: place['category']
            }).done(function(json_response) {
                var place = json_response['result'];
                self.PLACES[place['id']] = place;
                self.add_place_to_map(place);
            });
    };

    self.get_all_places = function() {
        $.get('/api/place/all/', {})
            .done(function(json_response) {
                var places = json_response['result'];
                $.each(places, function(i) {
                    var place = places[i];
                    if(!self.PLACES.hasOwnProperty(place['id'])) {
                        self.add_place_to_map(place);
                    } else {
                        var old_place = self.PLACES[place['id']];
                        if(place.lat != old_place.lat || place.lng != old_place.lat) {
                            var marker = self.PLACE_MARKERS[place['id']];
                            self.MAP.removeLayer(marker);
                            self.add_place_to_map(place);
                        }
                    }
                    self.PLACES[place['id']] = place;
                    
                });
            });
    };

    self.bind_events = function() {
        $('#add-place-container button').on('click', function(e) {
            e.preventDefault();
            self.add_place($('#add-place-container input[name="loc"]').val(),
                           $('#place-color').spectrum("get").toHexString().replace('#', ''),
                           $('#add-place-container input[name="name"]').val());
        });
    }

    self.init = function(map) {
        self.MAP = map;
        self.get_all_places();
        self.bind_events();
        self.POLL = setInterval(self.get_all_places, 10000);
        $("#place-color").spectrum({
            color: "#CCCCCC"
        });
    };
    self.init(map);
}