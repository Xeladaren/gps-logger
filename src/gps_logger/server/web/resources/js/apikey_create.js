const timezoneElem = document.getElementById("timezone");
const timezoneVal = Intl.DateTimeFormat().resolvedOptions().timeZone;
timezoneElem.setAttribute("value", timezoneVal);

const checkboxElem = document.getElementById("expire");
const expireDateElem = document.getElementById("expire-date");

checkboxElem.addEventListener('change', (event) => {
    if (event.currentTarget.checked)
    {
        console.log("expire checked")
        expireDateElem.removeAttribute("disabled")
    }
    else
    {
        console.log("expire unchecked")
        expireDateElem.setAttribute("disabled", "")
    }
})