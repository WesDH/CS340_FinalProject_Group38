

window.addEventListener('DOMContentLoaded', (event) =>
{
    console.log("DOM content loaded")
    let reload_db_btn = document.getElementById("reload_db_btn")

    reload_db_btn.addEventListener("click", function(event)
    {
        console.log(event);
        reload_db_btn.innerText = "...Reloading...";
        reload_db_btn.setAttribute("disabled", "");
        // split().slice() used below to grab current page name
        // reference: https://stackoverflow.com/questions/16611497/how-can-i-get-the-name-of-an-html-page-in-javascript
        // Havens, W, July 22nd, 2023
        fetch
        ('/reload_the_db',
        {
            method: 'POST',
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify
            ({
                page_name: location.href.split("/").slice(-1)
            })
        }
    )
        .then(response => handle(response))
    });
    function  handle(response) {
        reload_db_btn.removeAttribute("disabled")
        console.log(response)
        if (response.ok) {
            reload_db_btn.innerText = "OK!";
            console.log(response.url);
            window.location.replace(response.url);
        } else {
            reload_db_btn.innerText = "Error on DB Reload! Try again?";
        }
    }
});