function playAudio(type) {
    var audios = {
        "success": new Audio("/static/core/audio/success.mp3"),
        "error": new Audio("/static/core/audio/error.mp3"),
        "info": new Audio("static/core/audio/info.mp3")
    }
    audios[type].play()
}

function ajaxPostOnPostFormSubmit(modal) {
    $("#post-form").on('submit', function(e) {
        e.preventDefault()
        $.ajax({
            url: $(this).attr("action"),
            method: "POST",
            data: $(this).serialize(),
            success: function(response) {
                showNotice(response["message"], "success", "3000")
                playAudio("success")
                modal.close()
            },
            error: function(xhr) {
                console.log(xhr)
                showNotice("Error happened while trying to submit the form", "failure", "3000")
                playAudio("error")
            }
        })
    })
}

function openPostModal() {
    var modal = new jBox('Modal', {
        attach: '#main-post-modal',
        width: 1000,
        height: 340,
        onOpen: function() {
            $.ajax({
                url: "/new_post",
                method: "GET",
                data: $(this).serialize(),
                success: function(response) {
                    modal.setContent(response)
                    ajaxPostOnPostFormSubmit(modal)
                },
                error: function(xhr) {
                    console.log(xhr)
                    showNotice("Error happened while trying to open the form", "failure", "3000")
                    playAudio("error")
                }
            })
        }
    })
}

$(document).ready(function() {
    openPostModal()
})