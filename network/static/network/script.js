const views = ['#main_view', '#profile_view'];

$(document).ready(function() {
    setView('#main_view', views);
    setListeners()
    loadAllPosts()
})

function setView(selected_view) {
    $.each(views, function(index, selector) {
        $(selector).hide();  // hides each view
    });
    $(selected_view).show();  // show the selected one
}

function setListeners() {
    const view_button = {
        "#profile_view": "#profile",
    }

    $.each(view_button, function(view, button) {
        $(button).click(function() {
            setView(view)
        })
    })
}

function loadAllPosts() {
    console.log("Loading all posts")
    $.ajax({
        url: '/posts',
        type: 'GET',
        dataType: 'json',
        success: function(data) {
            console.log(data)
            // $('#posts').empty();  // Clear existing posts
            // $.each(data, function(index, post) {
            //     const postElement = $('<div class="post"></div>');
            //     postElement.append('<p>' + post.content + '</p>');
            //     $('#posts').append(postElement);
            // });
        }
    })
}