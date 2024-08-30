document.addEventListener('DOMContentLoaded', function() {
    makeDivsClickable('clickable-div');
});

function makeDivsClickable(className) {
    var divs = document.getElementsByClassName(className);
    for (var i = 0; i < divs.length; i ++) {
        var div = divs[i];
        div.addEventListener('click', function() {
            var url = this.getAttribute('data-url');
            window.location.href = url;
        })
    }
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
