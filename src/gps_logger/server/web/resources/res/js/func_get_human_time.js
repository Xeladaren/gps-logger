function get_human_time(time)
{
    output_str = ""
    if(time >= 0)
    {
        output_str += "il y a";
    }
    else
    {
        output_str += "dans";
        time = -time;
    }

    day = Math.trunc(time/(60*60*24));
    if(day > 0)
    {
        output_str += " " + day + " jours"
        time -= day * 3600 * 24
    }

    hour = Math.trunc(time/(60*60));
    if(hour > 0)
    {
        output_str += " " + hour + " heurs"
        time -= hour * 3600
    }

    minute = Math.trunc(time/(60));
    if(minute > 0)
    {
        output_str += " " + minute + "min"
        time -= minute * 60
    }

    output_str += " " + time+"s";

    return output_str
}

function pad(d) {
    return (d < 10) ? '0' + d.toString() : d.toString();
}

function get_human_date(date)
{
    let now = new Date();
    var output_string = "";

    if(date.toDateString() != now.toDateString())
    {
        output_string += pad(date.getFullYear()) + "-";
        output_string += pad(date.getMonth()+1) + "-";
        output_string += pad(date.getDate()) + " ";
    }

    output_string += pad(date.getHours()) + ":";
    output_string += pad(date.getMinutes()) + ":";
    output_string += pad(date.getSeconds());

    return output_string;
}