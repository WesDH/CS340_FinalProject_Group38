window.addEventListener('DOMContentLoaded', () =>
{
    let reload_db_btn = document.querySelector("input[type=submit]");
    reload_db_btn.addEventListener("click", (event) =>
    {
        console.log(event)
        reload_db_btn.innerText = "...Reloading...";
        reload_db_btn.setAttribute("disabled", "");
        fetch
        ('/reload_the_db',
        {
                method: 'POST',
                headers: {"Content-Type": "application/json"}
            }
        ).then(response =>
            {
                reload_db_btn.removeAttribute("disabled")
                if (response.ok)
                {
                    reload_db_btn.innerText = "OK!";
                    window.location.reload();
                }
                else
                {
                    reload_db_btn.innerText = "Error on DB Reload! Try again?";
                }
            })
    });
});