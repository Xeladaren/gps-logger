
var marker;
var map;
var path;

function build_map(pos, zoom, pres)
{
    map = L.map('map')

    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', 
    {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    map.setView(pos, zoom);

    marker = L.marker(pos).addTo(map);
    path   = L.polyline([], {color: 'red', opacity: 0.3}).addTo(map);
    path.addLatLng(pos);
    if(pres > 0)
    {
        var cyrcle_pres = L.circle(pos, {radius: pres}).addTo(map);
    }
}

function update_marker(pos)
{
    let follow_checkbox = document.getElementById("follow-marker");
    marker.setLatLng(pos);
    path.addLatLng(pos);

    if(follow_checkbox.checked)
    {
        map.panTo(pos);
    }
}