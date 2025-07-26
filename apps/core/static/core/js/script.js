const views = [".main-section", ".profile-section"]

$(document).ready(function() {
    function main() {
        setView(views[0])
        setupNavbarHandlers()
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

    main()
})
