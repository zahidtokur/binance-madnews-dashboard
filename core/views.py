from django.shortcuts import render
from django.views import View
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from core.models import Account
from core.resources.serializers import AccountSerializer


def index(request):
    return render(request, "core/index.html")


class AccountCreateView(View):
    template_name = "core/create.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        request_data = request.POST
        data = AccountSerializer(data=request_data)
        if not data.is_valid():
            for err in data.errors:
                messages.add_message(
                    request, messages.WARNING, str(data.errors[err]))
            return HttpResponseRedirect(reverse('core:create'))
        Account.objects.create(**data.validated_data)
        return HttpResponseRedirect(reverse('core:index'))
