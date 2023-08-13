/*
 GROUP 38: Joseph Houghton, Lauren Norman Schueneman, Wesley Havens

This small Javascript file binds a few buttons on "items" page, which is our
index.html

It also defines custom behavior for the "reload db" icon on the footer.

 References:
Citation for:
-  Javascript FETCH request syntax
Scope: Function
Date Accessed: July 27th, 2023
Accessed by: Havensw
Modified from previous CS290 final project Javascript source:
-   Source Title: CRUDapp
-   Source URL: http://weshavens.info/CRUDapp/

 */


// Wait for page to load before running the Javascript code:
window.addEventListener('DOMContentLoaded', () =>
{
    // Grab name of current html page so corresponding
    // button binds can be applied:
    let page = window.location.pathname.split("/").pop();
    console.log("Name of current page: ", page);


    // Grab the "reload db" container
    let reload_db_link = document.getElementById("reload_the_db");
    // Grab container for the reload bar icon that will be inserted on click
    let ul_reload_container = document.getElementById("ul_load_bar");

    // Create event listener for on click for reload db icon
    reload_db_link.addEventListener("click", (e) => {
        e.preventDefault();  // to prevent default link following on click

        // Change to the MDL loading bar after click:
        ul_reload_container.innerHTML = "<div id=\"db_reloader_bar\" class=\"mdl-progress mdl-js-progress mdl-progress__indeterminate\"></div>";
        // MDL specific JS to update dom for MDL elements below:
        // Source: https://stackoverflow.com/questions/33061979/mdl-componenthandler-upgradedom-after-ajax-call
        // Full citation on readme.md
        componentHandler.upgradeDom()

        // Send a fetch POST request to reload_the_db route:
        fetch
        ('/reload_the_db',
            {
                method: 'POST',
                headers: {"Content-Type": "application/json"}
            }
        ).then(response => {
            if (response.ok) {
                // Quickly change inner HTML to OK message:
                ul_reload_container.innerHTML = "Reload OK!"
            } else {
                // Quickly change inner HTML to ERROR message:
                ul_reload_container.innerHTML = "Error on DB reload"
            }
            // Either way, do full page reload to display flash() message
            // Received from Flask:
            window.location.reload();
        });
    });

    // We were using JS to bind buttons initially
    // This is remnant code to bind all pages, but we only used it for
    // index.html
    switch(page) {
    case '':
    case '/':
    case 'index.html':
        bind_index();
        break;
    case 'charSelection.html':
        break;
    default:
        console.log("Warning: UI_logic.js could not determine which .html doc " +
            "is currently being viewed")
    }
});

function bind_index() {
    /*
       JS Logic for index.html
       Binds for select user dropdown and insert user button
     */

    // Custom bind for select user dropdown menu on change:
    document.getElementById("select_user")
    .addEventListener("change", (e) => {
        // Send a POST with JSON payload containing the username selected:
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
        e.preventDefault();  // Prevent page reload on button press

        // Disable button while waiting for response from backend:
        insert_usr_btn.setAttribute("disabled", "");

        // Grab the values from the forms:
        let td_list = e.currentTarget.parentElement.parentElement
        let single_td = td_list.children
        let username = single_td[0].children[0].children[0].value;
        let password = single_td[1].children[0].children[0].value;
        let email = single_td[2].children[0].children[0].value;

        // Pre-flight check make sure every field has something at least
        if (username === "" || password === "" || email === "") {
            console.log("Empty field imput");
            // Change button back to functional:
            insert_usr_btn.removeAttribute("disabled")
            insert_usr_btn.innerText = "INSERT";
            return;
        }

        // Check that the email form is has valid text
        // If attribute validationMessage is NOT an empty string,
        // Then there is invalid input in the email field:
        if (single_td[2].children[0].children[0].validationMessage !== '') {
            console.log("Email is invalid format");
            insert_usr_btn.removeAttribute("disabled")
            insert_usr_btn.innerText = "INSERT";
            return;
        }

        // We did our pre-flight checks on the <inputs>
        // Now create a JSON payload:
        let user_payload = {
            table: "User_Accounts",
            username: username,
            password: password,
            email: email
        };

        // Send fetch POST with the payload to backend:
        fetch
        ('/',
            {
                method: 'POST',
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(user_payload),
            }
        ).then(() => {
            insert_usr_btn.removeAttribute("disabled")
            // Full page reload to update changes
            window.location.reload();
        });
    });
}
