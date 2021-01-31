from django.shortcuts import render


def test_view(request):
    print(request)
    return render(request, template_name='base.html')
