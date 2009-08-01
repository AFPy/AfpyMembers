var addMarker = function(map, user, marker) {
        GEvent.addListener(marker, 'click', function() {
            this.openInfoWindowHtml(user.uid);
        });
        map.addOverlay(marker);
}

var addPoint = function(map, point) {
    var ll = new GPoint(point.point[0], point.point[1])
    var marker = new GMarker(ll);
    map.addOverlay(marker);
    GEvent.addListener(marker, 'click', function() {
        this.openInfoWindowHtml('<h5>'+point.address+'</h5>'+point.users);
    });
}

$(document).ready(function(e) {
    if (GBrowserIsCompatible()) {
        var map = new GMap2(document.getElementById("map"));
        map.addControl(new GLargeMapControl());
        map.addControl(new GMapTypeControl());
        map.addControl(new GOverviewMapControl());
        var geocoder = new GClientGeocoder();
        geocoder.getLatLng('bourges, france', function(point) {
            map.setCenter(point, 5); });
        GEvent.addListener(map, 'load', function() {
            $.getJSON($('a#data_url').attr('href'), function(datas) {
                $(datas.result).each(function(i, point) {
                    addPoint(map, point);
                });
            });
        });
    }
});


