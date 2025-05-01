
function get_dms_pos(value, pos_symbol, neg_symbol)
{
    let output_str = "";

    if(value > 0)
    {
        var dir = pos_symbol;
    }
    else
    {
        var dir = neg_symbol;
        value = - value;
    }

    let deg = Math.trunc(value);
    let min = ( value - deg ) * 60;
    output_str += deg + "&deg;"

    let min_int = Math.trunc(min);
    let sec = ( min - min_int ) * 60;
    output_str += " " + min_int + "'"
    output_str += " " + sec.toFixed(2) + "''"
    output_str += " " + dir

    return output_str;
}

function update_latlon(data)
{
    let lat_span = document.getElementById("widget-lat");
    let lon_span = document.getElementById("widget-lon");
    let geolink_node = document.getElementById("geolink");

    lat_span.innerHTML = get_dms_pos(data.lat, "N", "S");
    lon_span.innerHTML = get_dms_pos(data.lon, "E", "W");
    geolink = "geo:" + data.lat + "," + data.lon;
    geolink_node.setAttribute("href", geolink)
}

function update_spd(data)
{
    let spd_span = document.getElementById("widget-spd");

    if(spd_span)
    {
        let value = Math.round(data.spd * 3.6) + " km/h";
        // console.log("Spd : ", value);
        spd_span.innerHTML = value;
    }
}

function update_ele(data)
{
    let ele_span = document.getElementById("widget-ele");

    if(ele_span)
    {
        let value = Math.round(data.ele) + " m";
        // console.log("Ele : ", value);
        ele_span.innerHTML = value;
    }
}

function update_dir(data)
{
    let dir_span = document.getElementById("widget-dir");

    if(dir_span)
    {
        let value = Math.round(data.ele) + "&deg;";
        // console.log("Ele : ", value);
        dir_span.innerHTML = value
    }
}

function update_posdate(data)
{
    let widget_date = document.getElementById("widget-date");
    let widget_timedelta = document.getElementById("widget-timedelta");
    let date = new Date(data.timestamp * 1000);
    // console.log(date.toISOString());

    if(widget_date)
    {
        widget_date.innerHTML = get_human_date(date);
    }
    if(widget_timedelta)
    {
        widget_timedelta.setAttribute('isodate', date.toISOString())
    }
}

function update_sat(data)
{
    let widget_node = document.getElementById("widget-sat");

    if(widget_node)
    {
        let value = Math.round(data.sat) + " sat";
        // console.log("Sat : ", value);
        widget_node.innerHTML = value
    }
}

function update_acc(data)
{
    let widget_node = document.getElementById("widget-acc");

    if(widget_node)
    {
        let value = Math.round(data.acc) + " m";
        // console.log("Acc : ", value);
        widget_node.innerHTML = value;
    }
}

function update_batt(data)
{
    let widget_node = document.getElementById("widget-batt");

    if(widget_node)
    {
        let value = Math.round(data.batt) + " %";
        // console.log("Batt : ", value);
        widget_node.innerHTML = value;
    }
}

function update_widget(data)
{
    update_latlon(data);
    update_spd(data);
    update_ele(data);
    update_dir(data);
    update_posdate(data);
    update_sat(data);
    update_acc(data);
    update_batt(data);
}