////////////////////////////////////////////////////////////////////////////////
//                               HTMX                                         //
////////////////////////////////////////////////////////////////////////////////

// Add CSRF token to every HTMX requests
document.body.addEventListener('htmx:configRequest', (event) => {
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    event.detail.headers['X-CSRFToken'] = csrfToken;
});

function generateRoom(userId) {
    var formId = "create-room-form-" + userId;
    var name = "Room " + Math.floor(Math.random() * 1000);
    var slug = name.toLowerCase().replace(/\s+/g, '-');

    document.getElementById(formId).querySelector("input[name='name']").value = name;
    document.getElementById(formId).querySelector("input[name='slug']").value = slug;

    document.getElementById(formId).submit();
}

////////////////////////////////////////////////////////////////////////////////
//                       Single Page Application                              //
////////////////////////////////////////////////////////////////////////////////

const root = document.getElementById("app-root")
const body = document.getElementById("app-body")

const targets = {
    "root": root,
    "body": body,
}

////////////////////

// all niviguation links share the `nav-item` class
// in order to select them all at once
// let nav_items = Array.from(document.getElementsByClassName("nav-item"));
// nav_items.forEach(item => {
//     item.addEventListener('click', handleNaviguationClick);
// })

const nav_home = document.getElementById("nav-home")
const nav_logo = document.getElementById("nav-logo")
const nav_play = document.getElementById("nav-play")
const nav_chatapp = document.getElementById("nav-chatapp")
const nav_profile = document.getElementById("nav-profile")
const nav_stats = document.getElementById("nav-stats")
const nav_login_page = document.getElementById("nav-login")
const nav_signup_page = document.getElementById("nav-signup")

nav_home.addEventListener('click', handleNaviguationClick);
nav_logo.addEventListener('click', handleNaviguationClick);
nav_play.addEventListener('click', handleNaviguationClick);
nav_chatapp.addEventListener('click', handleNaviguationClick);
nav_profile.addEventListener('click', handleNaviguationClick);
nav_stats.addEventListener('click', handleNaviguationClick);
if (nav_login_page) {
    nav_login_page.addEventListener('click', handleNaviguationClick);
}
if (nav_signup_page) {
    nav_signup_page.addEventListener('click', handleNaviguationClick);
}

function handleNaviguationClick(event) {
    event.preventDefault();
    swap_ui(this.getAttribute("href"), "app-root");
}

async function swap_ui(endpoint, swap_target) {
    try {
        const response = await fetch(endpoint, {
            method: 'GET',
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "spa-check": "true"
            }
        })
        if (response.ok === true) {
            const data = await response.json()
            const target = document.getElementById(swap_target)
            target.innerHTML = "";
            target.insertAdjacentHTML("afterbegin", data["html"])
            document.title = data["title"] || "placeholder"
            window.history.pushState({}, "", endpoint)
        } else {
            throw new Error('spa related, home')
        }
    } catch (error) {
        console.log("Caught exception: ", error)
    }
 }

window.addEventListener('popstate', function (e) {
    // this.alert("Went back")
    let state = e.state;
    console.log("Popstate: ", state)
})
