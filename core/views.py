from django.shortcuts import render
from django.views import View
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from core.models import Account
from core.resources.serializers import AccountSerializer


class IndexView(View):
    template_name = "core/index.html"
    accounts = Account.objects.all()

    def get_context_data(self, request, *args, **kwargs):
        context = {"accounts": self.accounts}
        account = self._get_selected_account(request.session)
        if account:
            context.update({"selected_account": account})
        else:
            try:
                del request.session["selected_account_id"]
            except KeyError:
                pass
        return context

    def _get_selected_account(self, session):
        account_id = session.get("selected_account_id")
        try:
            account = self.accounts.prefetch_related(
                "pairs").get(id=account_id)
        except Account.DoesNotExist:
            account = None
        return account

    def get(self, request, *args, **kwargs):
        context_data = self.get_context_data(request, *args, **kwargs)
        return render(request, self.template_name, context=context_data)


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


class SetMainAccountView(View):
    def get_object(self, request, object_id):
        return Account.objects.filter(id=object_id)

    def get(self, request, *args, **kwargs):
        account_id = self.kwargs.get("id")
        if self.get_object(request, account_id).exists():
            request.session["selected_account_id"] = account_id
        return HttpResponseRedirect(reverse("core:index"))
