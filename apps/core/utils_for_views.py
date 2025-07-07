from django.http import JsonResponse


def handle_invalid_form(message=None):
    message = message if message else 'Data Validation Error'
    response_msg = {
        'status': 'failure',
        'message': message
    }
    response = JsonResponse(response_msg)
    response.status_code = 400
    return response
