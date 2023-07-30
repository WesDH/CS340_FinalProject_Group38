/*
-- GROUP 38: Joseph Houghton, Lauren Norman Schueneman, Wesley Havens
--
-- Contains some custom JS logic for a few event listeners.
 */

window.addEventListener('DOMContentLoaded', () =>
{
    // Grab name of current html page so corresponding
    // button binds can be applied:
    let page = window.location.pathname.split("/").pop();
    console.log("Name of current page: ", page);


    let reload_db_link = document.getElementById("reload_the_db");
    //console.log(reload_db_link);
    let ul_reload_container = document.getElementById("ul_load_bar");
    console.log(ul_reload_container)
    reload_db_link.addEventListener("click", (e) => {
        e.preventDefault();
        ul_reload_container.innerHTML = "<div id=\"db_reloader_bar\" class=\"mdl-progress mdl-js-progress mdl-progress__indeterminate\"></div>";
        componentHandler.upgradeDom() // MDL specific to update dom for MDL elements
        console.log(reload_db_link)
        fetch
        ('/reload_the_db',
            {
                method: 'POST',
                headers: {"Content-Type": "application/json"}
            }
        ).then(response => {
            if (response.ok) {
                //insert_usr_btn.innerText = "OK!";
                console.log("Reload OK")
                ul_reload_container.innerHTML = "Reload OK!"

            } else {
                console.log("Reload NOT OK")
                ul_reload_container.innerHTML = "Error on DB reload"
                //insert_usr_btn.innerText = "Error! Try again?";
            }
            window.location.reload();
        });
    });



    switch(page) {
    case '':
    case '/':
    case 'index.html':
        bind_index();
        break;
    case 'charSelection.html':
        bind_char_selection();
        break;
    default:
        console.log("Warning: UI_logic.js could not determine which .html doc " +
            "is currently being viewed")
    }
});

function bind_char_selection() {
    // Assumption is the FIRST table is the CRUD table based on our layout:
    let table = document.getElementById("cruddy_tbody");
    let route = "/charSelection.html"
    let method = "PATCH";

    let cols = 5;
    Array.from(table.children).forEach(function (single_tr) {

        // this gives us the index of the <td>'s,
        // UPDATE button is always inside second to last <td>:
        let number_of_tds = single_tr.children.length;
        //console.log("btn to be bound: ",single_tr.children[number_of_tds - 2].children[0]);
        let input_btn = single_tr.children[number_of_tds - 2].children[0];
        let i = 0;
        let update_payload = {}
        update_payload["character_id"] = single_tr.getAttribute("char_id");
        Array.from(single_tr.children).forEach(function (single_td) {
            i++;
            if (i <= cols) {
                //console.log(single_td.children[0].children[0].getAttribute("name"));
                let attribute = single_td.children[0].children[0].getAttribute("name");
                //console.log(single_td.children[0].children[0].value)
                let value = single_td.children[0].children[0].value;
                update_payload[attribute] = value
            }
            if (i === cols ) {
                btn_bind_and_fetch(input_btn, cols, route, method);
            }
        });
    });
}

function bind_index() {
    /*
       Logic for index.html
       Binds for select user dropdown and insert user button
     */
    document.getElementById("select_user")
    .addEventListener("change", (e) => {

        fetch
        ('/',
        {
                method: 'POST',
                headers: {"Content-Type": "application/json"},
                body : JSON.stringify(
                {
                    table: 'User_Accounts',
                    username: e.target.value,
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
    // Bind and send FETCH request for INSERT user btn
    let insert_usr_btn = document.getElementById("insert_usr_btn")
    insert_usr_btn.addEventListener("click", (e) =>
    {
        e.preventDefault();
        insert_usr_btn.setAttribute("disabled", "");
        let td_list = e.currentTarget.parentElement.parentElement
        let single_td = td_list.children
        let username = single_td[0].children[0].children[0].value;
        let password = single_td[1].children[0].children[0].value;
        let email = single_td[2].children[0].children[0].value;
        if (username === "" || password === "" || email === "") {
            console.log("Empty field imput");
            insert_usr_btn.removeAttribute("disabled")
            insert_usr_btn.innerText = "INSERT";
            return;
        }

        if (single_td[2].children[0].children[0].validationMessage !== '') {
            console.log("Email is invalid format");
            insert_usr_btn.removeAttribute("disabled")
            insert_usr_btn.innerText = "INSERT";
            return;
        }
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
                body: JSON.stringify(user_payload),
            }
        ).then(response => {
            insert_usr_btn.removeAttribute("disabled")
            window.location.reload();
            if (response.ok) {
                //insert_usr_btn.innerText = "OK!";
                //window.location.reload();
            } else {
                //insert_usr_btn.innerText = "Error! Try again?";
            }
        });
    });
}


// to parameterize:
// METHOD, PAYLOAD, BUTTON
function btn_bind_and_fetch(button, cols, route, method_type) {
        console.log("btn bound function", button)



        button.addEventListener("click", (e) =>
        {
            e.preventDefault();
            //button.preventDefault();
            button.innerText = "......";
            button.setAttribute("disabled", "");

            let tr = button.parentNode.parentNode;

            // this gives us the index of the <td>'s,
            // UPDATE button is always inside second to last <td>:
            let number_of_tds = tr.children.length;
            let i = 0;
            let payload = {}
            payload["character_id"] = tr.getAttribute("char_id");
            Array.from(tr.children).forEach(function (single_td) {
                i++;
                if (i <= cols) {
                    //console.log(single_td.children[0].children[0].getAttribute("name"));
                    let attribute = single_td.children[0].children[0].getAttribute("name");
                    //console.log(single_td.children[0].children[0].value)
                    let value = single_td.children[0].children[0].value;
                    payload[attribute] = value
                }
                if (i === cols ) {
                    //console.log("Payload to be bound: ", update_payload);
                }
            });


            console.log("Payload prior to fetch ", payload);


            fetch(route, {
                    method: method_type,
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify(payload)
                }).then(response => {
                button.removeAttribute("disabled")
                if (response.ok) {
                    button.innerText = "UPDATE";
                    //window.location.reload();
                } else {
                    button.innerText = "UPDATE_ERR";
                }
            });
    }, false);
}
