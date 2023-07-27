console.log("Saved username", localStorage.getItem("saved_username"));

window.addEventListener('DOMContentLoaded', () =>
{
    // let reload_db_btn = document.getElementById("reload_db_btn")
    // reload_db_btn.addEventListener("click", () =>
    // {
    //     reload_db_btn.innerText = "...Reloading...";
    //     reload_db_btn.setAttribute("disabled", "");
    //     fetch
    //     ('/reload_the_db',
    //     {
    //             method: 'POST',
    //             headers: {"Content-Type": "application/json"}
    //         }
    //     ).then(response =>
    //         {
    //             reload_db_btn.removeAttribute("disabled")
    //             if (response.ok)
    //             {
    //                 reload_db_btn.innerText = "OK!";
    //                 window.location.reload();
    //             }
    //             else
    //             {
    //                 reload_db_btn.innerText = "Error on DB Reload! Try again?";
    //             }
    //         })
    // });

    // Grab name of current html page so corresponding
    // button binds can be applied:
    let page = window.location.pathname.split("/").pop();
    console.log("Name of current page: ", page);

    switch(page) {
    case '':
    case '/':
    case 'index.html':
        bind_index_html();
    break;
    case 'test.html':

    break;
    default:
        console.log("Warning: UI_logic.js could not determine which .html doc " +
            "is currently being viewed")
    }

});

function bind_index_html() {

    // Bind select user dropdown, save into page variable in JS
    // And send username to Flask with POST request
    document.getElementById("select_user")
    .addEventListener("change", (e) => {
        localStorage.setItem("saved_username", e.target.value);
        console.log("Saved username", localStorage.getItem("saved_username"));
        fetch
        ('/',
        {
                method: 'POST',
                headers: {"Content-Type": "application/json"},
                body : JSON.stringify(
                {
                    table: 'User_Accounts',
                    username: localStorage.getItem("saved_username"),
                }
            ),
            }
        ).then(response =>
            {
                if (response.ok)
                {
                    console.log("Username passed to backend")
                }
                else
                {
                    console.log("Username passed to backend HTTP error")
                }
            })
    });



    let insert_usr_btn = document.getElementById("insert_usr_btn")
    insert_usr_btn.addEventListener("click", (e) =>
    {
        e.preventDefault();
        //console.log(e.target.parentElement.parentElement.parentElement);
        insert_usr_btn.innerText = "...Sending Request...";
        insert_usr_btn.setAttribute("disabled", "");

        let td_list = e.currentTarget.parentElement.parentElement


        //childNodes[1].childNodes[1].value
        let single_td = td_list.children

        let username = single_td[0].children[0].children[0].value;
        let password = single_td[1].children[0].children[0].value;
        let email = single_td[2].children[0].children[0].value;

        let user_payload = {
            table: "User_Accounts",
            username: username,
            password: password,
            email: email
        };
        let i = 0;
        for (let item of single_td) {
            if (i === single_td.length - 1) break;
            console.log(item.children[0].children[0].value);
            i++;
        }

        fetch
        ('/',
        {
                method: 'POST',
                headers: {"Content-Type": "application/json"},
                body : JSON.stringify(user_payload),
            }
        ).then(response =>
            {
                insert_usr_btn.removeAttribute("disabled")
                if (response.ok)
                {
                    insert_usr_btn.innerText = "OK!";
                    //window.location.reload();
                }
                else
                {
                    insert_usr_btn.innerText = "Error! Try again?";
                }
            })
    });

}

