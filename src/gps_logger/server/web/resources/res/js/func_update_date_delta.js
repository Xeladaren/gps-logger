function update_date_delta()
{
    const dateDeltaElems = document.getElementsByClassName('date-delta');

    for (let index = 0; index < dateDeltaElems.length; index++)
    {
        const dateDeltaElem = dateDeltaElems[index];

        const date_now = new Date();
        const date_mesure = new Date(dateDeltaElem.getAttribute('isodate'));
        const date_diff = Math.round((date_now - date_mesure) / 1000);

        dateDeltaElem.innerHTML = get_human_time(date_diff);
    }
}