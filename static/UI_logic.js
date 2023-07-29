console.log("Saved username", localStorage.getItem("saved_username"));

window.addEventListener('DOMContentLoaded', () =>
{
    // Grab name of current html page so corresponding
    // button binds can be applied:
    let page = window.location.pathname.split("/").pop();
    console.log("Name of current page: ", page);

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
        //console.log("outer loop", single_tr);
        //console.log(single_tr.getAttribute("char_id"));

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
                //console.log("Payload to be bound: ", update_payload);
                btn_bind_and_fetch(input_btn, cols, route, method);
            }
            // console.log(i);
            // console.log(cols);
        });
    });


// Not needed: Works with standard HTML forms:
    // let insert_char_btn = document.getElementById("insert_char_btn")
    // insert_char_btn.addEventListener("click", (e) =>
    // {
    //     e.preventDefault();
    //     insert_char_btn.innerText = "...Sending Request...";
    //     insert_char_btn.setAttribute("disabled", "");
    //
    //     let td_list = e.currentTarget.parentElement.parentElement;
    //
    //     console.log(td_list);
    //
    //     let single_td = td_list.children;
    //     let character_name = single_td[0].children[0].children[0].value;
    //     let race = single_td[1].children[0].children[0].value;
    //     let char_class = single_td[2].children[0].children[0].value;
    //     let type = single_td[3].children[0].children[0].value;
    //     let alignment = single_td[4].children[0].children[0].value;
    //
    //     let user_payload = {
    //         table: "Characters",
    //         character_name: character_name,
    //         race: race,
    //         char_class: char_class,
    //         type: type,
    //         alignment: alignment
    //     };
    //
    //     console.log(user_payload);
    //
    //     throw new error();

        // if (username === "" || password === "" || email === "") {
        //     console.log("Empty field imput");
        //     insert_usr_btn.removeAttribute("disabled")
        //     insert_usr_btn.innerText = "INSERT";
        //     return;
        // }
        //
        // if (single_td[2].children[0].children[0].validationMessage !== '') {
        //     console.log("Email is invalid format");
        //     insert_usr_btn.removeAttribute("disabled")
        //     insert_usr_btn.innerText = "INSERT";
        //     return;
        // }


    //
    //     let i = 0;
    //     for (let item of single_td) {
    //         if (i === single_td.length - 1) break;
    //         console.log(item.children[0].children[0].value);
    //         i++;
    //     }
    //
    //     fetch
    //     ('/',
    //     {
    //             method: 'POST',
    //             headers: {"Content-Type": "application/json"},
    //             body : JSON.stringify(user_payload),
    //         }
    //     ).then(response =>
    //         {
    //             insert_usr_btn.removeAttribute("disabled")
    //             if (response.ok)
    //             {
    //                 insert_usr_btn.innerText = "OK!";
    //                 //window.location.reload();
    //             }
    //             else
    //             {
    //                 insert_usr_btn.innerText = "Error! Try again?";
    //             }
    //         })
    // });

}

function bind_index() {

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
        insert_usr_btn.innerText = "...Sending Request...";
        insert_usr_btn.setAttribute("disabled", "");

        let td_list = e.currentTarget.parentElement.parentElement

        let single_td = td_list.children
        console.log(single_td[2].children[0].children[0])
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
            if (response.ok) {
                insert_usr_btn.innerText = "OK!";
                window.location.reload();
            } else {
                insert_usr_btn.innerText = "Error! Try again?";
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
