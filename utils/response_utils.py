from rest_framework.response import Response

def success(data=None, status=200):
    return Response(
        {
            "success": True,
            "data": data,
        },
        status=status
    )

def error(message, status=400):
    return Response(
        {
            "success": False,
            "error": message,
        },
        status=status
    )