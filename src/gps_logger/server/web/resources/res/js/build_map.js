
function build_map(pos, zoom, pres)
{
    var map = L.map('map')

    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', 
    {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    map.setView(pos, zoom);

    var marker = L.marker(pos).addTo(map);
    if(pres > 0)
    {
        var cyrcle_pres = L.circle(pos, {radius: pres}).addTo(map);
    }
}