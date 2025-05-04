const views = ['#main_view', '#profile_view'];

$(document).ready(function() {
    setView('#main_view', views);
    setListeners()
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