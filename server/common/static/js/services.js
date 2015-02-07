var Dialog = function() {
    var self = this;

    self.DIALOGS = {
        ADD_CHARACTER: 'add-player-container',
        UPDATE_LOCATION: 'update-player-container',
        ADD_PLACE: 'add-place-container'
    }

    self.show_dialog = function(dialog_id) {
        $('.map_overlay > div').hide();
        $('#'+dialog_id).show();
    }

    self.init = function() {
        self.show_dialog(self.DIALOGS.ADD_CHARACTER);
    }
    self.init();
}

var Places = function(map) {
    var self = this;

    self.MAP = null;
    self.PLACE_MARKERS = {};
    self.PLACES = {};

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
            }).bindPopup('Base').addTo(self.MAP);

        self.PLACE_MARKERS[place['id']] = marker;
    };

    self.add_place = function(lat, lng, name, icon_string, color, category) {
        $.get('/api/place/add/', {
                lat: lat,
                lng: lng,
                name: name,
                icon_string: icon_string,
                color: color,
                category: category
            }).done(function(json_response) {
                var place = json_response['result'];
                self.PLACES[place['id']] = place;
                self.add_place_to_map(place);
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

    self.get_all_places = function(callback) {
        $.get('/api/place/all/', {})
            .done(function(json_response) {
                self.PLACES = json_response['result'];
                callback();
            });
    };

    self.init = function(map) {
        self.MAP = map;
        self.get_all_places(function() {
            $.each(self.PLACES, function(i) {
                self.add_place_to_map(self.PLACES[i]);
            })
        });
    };
    self.init(map);
}