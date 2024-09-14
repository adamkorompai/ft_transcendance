////////////////////////////////////////////////////////////////////////////////
//                           FRIEND SYSTEM                                    //
////////////////////////////////////////////////////////////////////////////////

async function sendFriendRequest(id, csrf) {
    payload = {
        "receiver_user_id": id,
    }
    const r = await fetch("/accounts/friend_request/", {
        method: 'POST',
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-CSRFToken": csrf
        },
        body: JSON.stringify(payload)
    })
    if (r.ok === true) {
        r.json().then(body => {
            res = body['response'];
            if (res == "Friend request sent.") {
                onFriendRequestSent(id, csrf);
            }
            else if (res === 'Friend request accepted while sending mine') {
                onFriendRequestAccepted('header_status_bar', data);
            }
            else if (res != null) {
                console.log(data['response']);
            }
        })
        return
    }
    throw new Error('Could not SEND friend request.')
}

function onFriendRequestSent(id, csrf) {
    var status_bar = document.getElementById("header_status_bar");
    status_bar.innerHTML = "";

    var cancel_request_btn = createCancelFriendRequestBtn(id, csrf);

    status_bar.append(cancel_request_btn);
}

////////////////////////////////////////////////////////////////////////////////

async function cancelFriendRequest(id, csrf) {
    payload = {
        "receiver_user_id": id,
    }
    const r = await fetch("/accounts/cancel_friend_request/", {
        method: 'POST',
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-CSRFToken": csrf
        },
        body: JSON.stringify(payload)
    })
    if (r.ok === true) {
        r.json().then(body => {
            res = body['response'];
            if (res == "Friend request cancelled") {
                onFriendRequestCanceled()
            }
            else if (res != null) {
                location.reload()
                console.log(res)
            }
        })
        return
    }
    throw new Error('Could not CANCEL friend request.')
}

function onFriendRequestCanceled() {
    var status_bar = document.getElementById("header_status_bar");
    status_bar.innerHTML = ""
    id = status_bar.getAttribute("data-id")
    csrf = status_bar.getAttribute("data-csrf")

    var addFriendBtn = createAddFriendBtn(id, csrf);
    var blockBtn = createBlockUnblockBtn(id, "block");

    status_bar.append(addFriendBtn, blockBtn);
}

////////////////////////////////////////////////////////////////////////////////

async function acceptFriendRequest(friend_request_id, container, csrf) {
    var url = "/accounts/accept_friend_request/"
    payload = {
        "friend_request_id": friend_request_id,
    }
    const r = await fetch(url, {
        method: 'POST',
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-CSRFToken": csrf,
            "html_container": container
        },
        body: JSON.stringify(payload)
    })
    if (r.ok === true) {
        r.json().then(body => {
            res = body['response'];
            if (res == "Friend request accepted") {
                onFriendRequestAccepted(container, body['content'])
            }
            else if (res != null) {
                location.reload()
            }
        })
        return
    }
    throw new Error('Could not ACCEPT friend request.')
}

function onFriendRequestAccepted(origin, data) {
    container = document.getElementById(origin);
    container.innerHTML = "";
    id = container.getAttribute('data-id');
    csrf = container.getAttribute('data-csrf');
    
    console.log("Origin: ", origin)
    if (origin === "header_status_bar") {
        var unfriend_btn = createUnfriendBtn(id, csrf);
        var dm_btn = createMessageBtn();
        var block_btn = createBlockUnblockBtn(id, "block");
        container.append(unfriend_btn, dm_btn, block_btn);
    } else if (origin === 'widget_status_bar') { // widget_status_bar
        console.log("MSG: widget section")
        container.innerHTML = data
    }
}

////////////////////////////////////////////////////////////////////////////////

async function declineFriendRequest(friend_request_id, origin, csrf) {
    var url = "/accounts/decline_friend_request/"
    payload = {
        "friend_request_id": friend_request_id,
    }
    const r = await fetch(url, {
        method: 'POST',
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-CSRFToken": csrf,
            "html_container": origin
        },
        body: JSON.stringify(payload)
    })
    if (r.ok === true) {
        r.json().then(body => {
            res = body['response']
            if (res == "Friend request declined") {
                onFriendRequestDeclined(origin, body['content']);
            }
            else if (res != null) {
                location.reload()
            }
        })
        return
    }
    throw new Error('Could not DECLINE friend request.')
}

function onFriendRequestDeclined(origin, response_content) {
    var container = document.getElementById(origin);
    container.innerHTML = ""
    id = container.getAttribute("data-id");
    csrf = container.getAttribute("data-csrf");

    if (origin === "header_status_bar") {
        var addFriendBtn = createAddFriendBtn(id, csrf);
        var blockBtn = createBlockUnblockBtn(id, "block");
        container.append(addFriendBtn, blockBtn);
    } else if (origin === 'widget_status_bar') {
        container.innerHTML = response_content
    }
}

////////////////////////////////////////////////////////////////////////////////

async function removeFriend(receiver_user_id, csrf) {
    var url = "/accounts/friend_remove/"
    payload = {
        "csrfmiddlewaretoken": csrf,
        "receiver_user_id": receiver_user_id,
    }
    const r = await fetch(url, {
        method: 'POST',
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-CSRFToken": csrf
        },
        body: JSON.stringify(payload)
    })
    if (r.ok === true) {
        r.json().then(body => {
            res = body['response']
            if (res == "Successfully removed that friend"){
                onFriendRemoved()
            }
            else if (res != null) {
                throw new Error(res)
            }
        })
        return
    }
    throw new Error('Could not REMOVE from friends.')
}

function onFriendRemoved() {
    var status_bar = document.getElementById("header_status_bar");
    status_bar.innerHTML = ""
    id = status_bar.getAttribute("data-id");
    csrf = status_bar.getAttribute("data-csrf")
    
    var add_friend_btn = createAddFriendBtn(id, csrf)
    var block_btn = createBlockUnblockBtn(id, "block");

    status_bar.append(add_friend_btn, block_btn);
}

////////////////////////////////////////////////////////////////////////////////

async function blockUnblock(id, action, fromChat) {
    let csrf = document.getElementById("app-body").getAttribute("data-csrf");
    var url = "/accounts/blocking/"
    payload = {
        "user_id": id,
        "action": action
    }
    const r = await fetch(url, {
        method: 'POST',
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-CSRFToken": csrf
        },
        body: JSON.stringify(payload)
    })
    if (r.ok === true) {
        r.json().then(body => {
            onBlockedUnblocked(action, fromChat, csrf);
        })
        return
    }
    throw new Error('Could not block user.')
}

function onBlockedUnblocked(action, fromChat) {
    if (fromChat === "true") {
        // redirect to chat page
        window.location.href = "/chatapp/";
    }
    var status_bar = document.getElementById("header_status_bar");
    status_bar.innerHTML = ""
    id = status_bar.getAttribute("data-id");
    csrf = status_bar.getAttribute("data-csrf")

    
    if (action === "block") {
        unblock_btn = createBlockUnblockBtn(id, "unblock");
        status_bar.append(unblock_btn);
    } else {
        add_friend_btn = createAddFriendBtn(id, csrf);
        block_btn = createBlockUnblockBtn(id, "block");
        status_bar.append(add_friend_btn, block_btn);
    };
}

////////////////////////////////////////////////////////////////////////////////
//                         CREATING HTML ELEMENTS                             //
////////////////////////////////////////////////////////////////////////////////

function createAddFriendBtn(id, csrf) {
    var btn = document.createElement("button");
    target_url = "/accounts/friend_request/"
    btn.innerHTML = "Add Friend";
    btn.className = "btn_requests"
    btn.id = "id_send_friend_request_btn"
    btn.setAttribute("onclick", `sendFriendRequest('${id}', '${csrf}')`); // this
    btn.setAttribute("data-next-url", "/accounts/cancel_friend_request/");
    return btn;
}

function createCancelFriendRequestBtn(id, csrf) {
    var btn = document.createElement("button");
    btn.innerHTML = "Invitation Sent";
    btn.className = "btn_requests";
    btn.id = "id_cancel_request_btn";
    btn.setAttribute("onclick", `cancelFriendRequest('${id}', '${csrf}')`);
    btn.setAttribute("data-next-url", "/accounts/friend_request/");
    return btn;
}

function createUnfriendBtn(id, csrf) {
    var btn = document.createElement("button")
    btn.innerHTML = "Unfriend";
    btn.id = "id_unfriend_btn";
    btn.className = "btn_requests";
    btn.setAttribute('onclick', `removeFriend('${id}', '${csrf}')`);
    return btn;
}

function createBlockUnblockBtn(id, type) {
    var btn = document.createElement("button");
    btn.innerHTML = capitalize(type)
    btn.className = "btn_requests"
    btn.setAttribute('onclick', `blockUnblock("${id}", "${type}")`)
    return btn
}

function createMessageBtn() {
    var dm_btn = document.createElement("button");
    dm_btn.innerHTML = "Message";
    dm_btn.className = "btn_requests";

    var anchor = document.createElement("a");
    anchor.href = "/chatapp";
    anchor.appendChild(dm_btn);

    return anchor;
}

////////////////////////////////////////////////////////////////////////////////
//                            HELPER FUNCTIONS                                //
////////////////////////////////////////////////////////////////////////////////

function capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
}