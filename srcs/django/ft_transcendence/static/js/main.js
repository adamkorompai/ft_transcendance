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

// window.onload = function() {
//     // Fetch the announcement content from Django template
//     var announcementContent = "{{ announcement.content }}";

//     // Check if there is an announcement
//     if (announcementContent) {
//         // Display the announcement as a pop-up window
//         alert(announcementContent);
//     }
// };

function generateRoom(userId) {
    var formId = "create-room-form-" + userId;
    var name = "Room " + Math.floor(Math.random() * 1000);
    var slug = name.toLowerCase().replace(/\s+/g, '-');

    document.getElementById(formId).querySelector("input[name='name']").value = name;
    document.getElementById(formId).querySelector("input[name='slug']").value = slug;

    document.getElementById(formId).submit();
}

// herrrrrrr

function initChat(slug, room_name, username) {
    
}