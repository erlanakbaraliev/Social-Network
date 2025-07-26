function openPostModal() {
    $.ajax({
        url: "/new_post",
        method: "GET",
        success: function(response) {
            var modal = new jBox('Modal', {
                width: 1000,
                height: 340,
                attach: '#main-post-modal',
                content: response.html,
                onOpen: function() {
                    $("#post-form").on('submit', function(e) {
                        e.preventDefault()
                        $.ajax({
                            url: $(this).attr("action"),
                            method: "POST",
                            data: $(this).serialize(),
                            success: function(response) {
                                console.log(response)
                                modal.close()
                                // render Successfull submission notice
                            },
                            error: function(xhr) {
                                console.log("Submission failed", xhr)
                                // render RenderingError
                            }

                        })
                    })
                }
            });
        },
        error: function(xhr) {
            console.log("Request failed", xhr)
            // implement jbox notice saying that error happened while trying to render the template
        }
    })
}

$(document).ready(function() {
    openPostModal()
})