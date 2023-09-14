
from django.shortcuts import render, redirect
from wellcome.forms import SubscriberForm


def wellcome(request):
    form = SubscriberForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect(request.META['HTTP_REFERER'])
    else:
        return render(request, 'wellcome/wellcome.html', locals())