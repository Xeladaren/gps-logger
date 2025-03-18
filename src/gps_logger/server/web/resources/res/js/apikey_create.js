const timezoneElem = document.getElementById("timezone");
const timezoneVal = Intl.DateTimeFormat().resolvedOptions().timeZone;
timezoneElem.setAttribute("value", timezoneVal);

const checkboxElem = document.getElementById("expire");
const expireDateElem = document.getElementById("expire-date");
const date = new Date();
const date_str_local = date.toLocaleString('sv', {year:'numeric', month:'numeric', day:'numeric', hour:'numeric', minute:'numeric'}).replace(' ', 'T');

expireDateElem.setAttribute('min', date_str_local)

checkboxElem.addEventListener('change', (event) => {
    if (event.currentTarget.checked)
    {
        expireDateElem.removeAttribute("disabled")
        expireDateElem.setAttribute("required", "")
    }
    else
    {
        expireDateElem.setAttribute("disabled", "")
        expireDateElem.removeAttribute("required")
    }
})