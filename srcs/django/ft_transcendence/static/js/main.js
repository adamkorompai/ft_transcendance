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

// re-attach events to corresponding classes
// let nav_items = Array.from(document.getElementsByClassName("spa-nav-item"));
// nav_items.forEach(item => {
//     item.addEventListener('click', handleNaviguation);
// })

// adds event listeners to all naviguation links
let container = document.getElementById("app-body");
container.addEventListener('click', (event) => {
    if (event.target && event.target.classList.contains("spa-nav-item")) {
        handleNaviguation(event);
    }
})

// replaces default links behaviour with the following:
// Fetch to get new content, swap UI, save state to browser history
async function handleNaviguation(event) {
    event.preventDefault();
    const endpoint = event.target.getAttribute("href");
    console.log(`Go to URL: ${endpoint}`);
    if (!endpoint)
        return ;
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
            const json = await response.json();
            updateUI(json, "app-root");
            window.history.pushState(json, "", endpoint);
        } else {
            throw new Error(`Fetch failed: ${response}`);
        }
    } catch (error) {
        console.log("Caught exception: ", error);
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

////////////////////////////////////////////////////////////////////////////////
//                                  Pong                                      //
////////////////////////////////////////////////////////////////////////////////

// const player1ReadyBox = document.getElementById('player1-ready');
// const player2ReadyBox = document.getElementById('player2-ready');
// const opponentInput = document.getElementById('opponent-username');
// const readyText = document.getElementById('ready-text');
// const opponentImage = document.getElementById('opponent-image');
// const suggestionList = document.getElementById('opponent-suggestions');

// let player1Ready = false;
// let player2Ready = false;
// let opponentValid = false;

// function toggleReady(player) {
//     if (player === 'player1') {
//         player1Ready = !player1Ready;
//         player1ReadyBox.classList.toggle('ready-green', player1Ready);
//         player1ReadyBox.classList.toggle('ready-red', !player1Ready);
//         checkGameReady();
//     } else if (player === 'player2') {
//         validateOpponent().then(() => {
//             if (!player2Ready && opponentInput.value.trim() && !opponentValid) {
//                 return;
//             }

//             player2Ready = !player2Ready;
//             player2ReadyBox.classList.toggle('ready-green', player2Ready);
//             player2ReadyBox.classList.toggle('ready-red', !player2Ready);
//             opponentInput.readOnly = player2Ready;

//             if (!player2Ready) {
//                 opponentValid = false;
//                 validateOpponent();
//             }

//             checkGameReady();
//         });
//     }
// }

// async function checkGameReady() {
//     if (player1Ready && player2Ready) {
//         const player1Username = "{{ request.user.username }}";
//         const player2Username = opponentInput.value.trim();

//         setTimeout(() => {
//             let form;
//             if (player2Username && opponentValid) {
//                 form = createForm("{% url 'pong_game' %}", {
//                     player1: player1Username,
//                     player2: player2Username
//                 });
//             } else {
//                 form = createForm("{% url 'pong_ia_game' %}", {
//                     player1: player1Username
//                 });
//             }
//             document.body.appendChild(form);
//             form.submit();
//         }, 2000);
//     }
// }

// function createForm(action, inputs) {
//     const form = document.createElement('form');
//     form.action = action;
//     form.method = 'POST';
//     form.innerHTML = `{% csrf_token %}`;
//     for (const name in inputs) {
//         form.innerHTML += `<input type="hidden" name="${name}" value="${inputs[name]}">`;
//     }
//     return form;
// }

// const debounce = (func, delay) => {
//     let timeoutId;
//     return (...args) => {
//         clearTimeout(timeoutId);
//         timeoutId = setTimeout(() => func(...args), delay);
//     };
// };

// const validateOpponentDebounced = debounce(validateOpponent, 500);

// async function validateOpponent() {
//     const opponentName = opponentInput.value.trim();
//     const playerName = "{{ request.user.username }}";

//     if (opponentName === '') {
//         resetOpponentUI();
//         return;
//     }

//     if (playerName === opponentName) {
//         opponentImage.src = "{% static '../media/default.png' %}";
//         opponentValid = false;
//         player2ReadyBox.classList.add('disabled');
//         readyText.textContent = 'Invalid Selection';
//         return;
//     }

//     try {
//         const response = await fetch('/play/check-user/' + opponentName + '/');
//         const data = await response.json();
//         if (data.exists) {
//             opponentImage.src = data.profile_image;
//             opponentValid = true;
//             player2ReadyBox.classList.remove('disabled');
//             if (!player2Ready) {
//                 readyText.textContent = 'Ready ?';
//             }
//         } else {
//             resetOpponentUI();
//         }
//     } catch (error) {
//         console.error('Error:', error);
//     }
// }

// function resetOpponentUI() {
//     opponentImage.src = "{% static '../media/default.png' %}";
//     opponentValid = false;
//     player2ReadyBox.classList.add('disabled');
//     readyText.textContent = 'IA Game';
// }

// async function searchOpponents() {
//     const opponentName = opponentInput.value.trim();

//     if (opponentName === '') {
//         readyText.textContent = 'IA Game';
//         suggestionList.innerHTML = '';
//         return;
//     }

//     try {
//         const response = await fetch('/play/search-opponents/?query=' + encodeURIComponent(opponentName));
//         const data = await response.json();
//         suggestionList.innerHTML = '';
//         data.forEach(opponent => {
//             const suggestionItem = document.createElement('li');
//             suggestionItem.textContent = opponent.username;
//             suggestionItem.addEventListener('click', function() {
//                 opponentInput.value = opponent.username;
//                 validateOpponentDebounced();
//                 suggestionList.innerHTML = '';
//             });
//             suggestionList.appendChild(suggestionItem);
//         });
//     } catch (error) {
//         console.error('Error:', error);
//     }
// }

// window.addEventListener('pageshow', function(event) {
//     if (event.persisted || (window.performance && window.performance.navigation.type === 2)) {
//         opponentInput.value = '';
//     }
// });