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

// adds event listeners to all naviguation links
let nav_items = Array.from(document.getElementsByClassName("nav-item"));
nav_items.forEach(item => {
    item.addEventListener('click', handleNaviguation);
})

// replaces default links behaviour with the following:
// Fetch to get new content, swap UI, save state to browser history
async function handleNaviguation(event) {
    event.preventDefault();
    const endpoint = this.getAttribute("href")
    if (!endpoint)
        return ;
    const ui_target = "app-root"
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
            const json = await response.json()
            updateUI(json, ui_target, endpoint)
            window.history.pushState(json, "", endpoint)
        } else {
            throw new Error(`Fetch failed: ${response}`)
        }
    } catch (error) {
        console.log("Caught exception: ", error)
    }
}

function updateUI(content, target) {
    const t = document.getElementById(target)
    if (t) {
        document.title = content.title || "Ft_transcendance"
        t.innerHTML = "";
        t.insertAdjacentHTML("afterbegin", content["html"])
    }
}

// updates UI when using the browser's backward/forward buttons
window.addEventListener('popstate', function (event) {
    let state = event.state;
    if (state) {
        updateUI(state, "app-root") // what if target is app-body?
    }
})
