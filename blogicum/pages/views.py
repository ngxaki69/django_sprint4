from django.shortcuts import render


def page_not_found(request, *args, **kwargs):
    return render(request, 'pages/404.html', status=404)


def csrf_failure(request, *args, **kwargs):
    return render(request, 'pages/403csrf.html', status=403)


def internal_error(request, *args, **kwargs):
    return render(request, 'pages/500.html', status=500)
