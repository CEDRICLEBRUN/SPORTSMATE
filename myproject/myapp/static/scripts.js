function makeDivsClickable(className) {
    var div = document.getElementsByClassName(className);
    var url = div[0].getAttribute('data-url');
    window.location.href = url;
}

function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
}

function filterSearchByNameOrSport() {
    var title = $('#search-title').val();
    $.ajax({
        url: "/events/list",
        data: {
            't': title
        },
        success: function(data) {
            var events = $(data).find("#events-list").html();
            $("#events-list").html(events);
        }
    })
}

function filterSearchByCity() {
    var city = $('#search-city').val();
    $.ajax({
        url: "/events/list",
        data: {
            'c': city
        },
        success: function(data) {
            var events = $(data).find("#events-list").html();
            $("#events-list").html(events);
        }
    })
}

function filterUsers() {
    var input, filter, userList, userItems, i, txtValue, contactBtn;
    input = document.getElementById('user_search');
    filter = input.value.toLoweCase();
    userList = document.getElementById('user-list');
    userItems = userList.getElementsByClassName('user-item');

    if (filter) {
        userList.style.display = 'block';
    } else {
        userList.style.display = 'none';
    }

    for (i = 0; i < userItems.length; i++) {
        txtValue = userItems[i].textContent || userItems[i].innerText;
        if (txtValue.toLoweCase().indexOf(filter) > -1) {
            userItems[i].style.display = '';
        } else {
            userItems[i].style.display = 'none';
        }
    } 
}

function selectUser(userId, username) {
    document.getElementById('user_search').value = username;
    document.getElementById('selected_user_id').value = userId;
    var userList = document.getElementById('user-list');
    var userItems = document.getElementsByClassName('user-item');
    var contactBtn = document.getElementsByClassName('contact-btn')[0];
    contactBtn.style.display = 'flex';

    for (var i = 0; i < userItems.length; i++) {
        userItems[i].style.display = 'none';
    }
}
