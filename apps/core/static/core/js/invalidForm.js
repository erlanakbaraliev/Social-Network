// Global function for showing notices
function showNotice(content, response_status, autoClose=true) {
    var status_color_map = {
        "success": "green",
        "failure": "red",
        "notice": "black"
    }

    new jBox('Notice', {
        attributes: {y: "bottom"},
        content: content,
        color: status_color_map[response_status],
        autoClose: autoClose,
        animation: {
            open: "pulse",
            close: "zoomIn"
        },
    })
}

function _handle_json_error(response_object) {
    const autoClose = "3000"
    let response = response_object.responseJSON
    
    showNotice(response["message"], response["status"], autoClose)
}

function ajaxHandleInvalidForm(event, form_id) {
    event.preventDefault()
    let $form_object = form_id ? $(form_id) : $(event.target)
    const url = $form_object.attr("action")
    const method = $form_object.attr("method")
    
    $.ajax({
        url: url,
        type: method,
        data: $form_object.serialize(),
        success: function(response) {
            console.log("Successfull submission")
        },
        error: function(jqXHR) {
            _handle_json_error(jqXHR)
        }
    })
}

// $(document).ready(function() {
//     $('#login-form').on('submit', function(e) {
//         ajaxHandleInvalidForm(e, false)
//     })
// })