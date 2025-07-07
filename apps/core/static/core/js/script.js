const views = [".main-section", ".profile-section"]

$(document).ready(function() {
    function main() {
        setView(views[0])
        setupNavbarHandlers()
        setupPostModalClosedHandler()
    }
    
    function setView(view) {
        $.each(views, function(k, v) {
            $(v).hide()
        })
        $(view).show()
    }
    
    function setupNavbarHandlers() {
        $("#navbar-logo").click(function() {
            setView(views[0])
        })
        $("#navbar-profile-btn").click(function() {
            setView(views[1])
        })
    }
    
    function setupPostModalClosedHandler() {
        // When the user clicks anywhere outside of the modal, close it
        $(window).on("click", function(event) {
            if ($(event.target).is("#main-post-form-div")) {
                $("#main-post-form-div").hide()
            }
        })
    }

    main()
})
