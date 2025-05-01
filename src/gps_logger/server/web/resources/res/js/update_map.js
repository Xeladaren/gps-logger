
var last_timestamp = 0;

function get_api_url(){
    let page_url = document.URL;
    // console.log(page_url);

    let api_url = page_url.replace("/web/", "/api/");
    // console.log(api_url);

    return api_url;
}

function update_map(data)
{
    if(data.timestamp != last_timestamp)
    {
        let pos = L.latLng(data.lat, data.lon);

        // console.log(data);

        update_marker(pos);
        update_widget(data);

        last_timestamp = data.timestamp;
    }

    update_date_delta();
}

async function get_api(url) {
    let response = await fetch(url);
    // console.log(response);

    get_api_url()

    if (response.ok) { // if HTTP-status is 200-299
    // obtenir le corps de réponse (la méthode expliquée ci-dessous)
        let json = await response.json();
        update_map(json);
    } else {
        alert("HTTP-Error: " + response.status);
    }
}