from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView
from django.contrib import messages

from core.models import Account
from core.resources.serializers import AccountSerializer


class IndexView(View):
    template_name = "core/index.html"

    def get_context_data(self, request, *args, **kwargs):
        account = self._get_selected_account(request.session)
        if account:
            context = {"selected_account": account}
        else:
            try:
                del request.session["selected_account_id"]
            except KeyError:
                pass
        return context

    def _get_selected_account(self, session):
        account_id = session.get("selected_account_id")
        try:
            account = Account.objects.prefetch_related(
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
        serializer = AccountSerializer(data=request_data)
        if serializer.is_valid():
            try:
                serializer.create(serializer.validated_data)
                return reverse_lazy('core:index')
            except Exception as e:
                messages.add_message(request, messages.WARNING, str(e))
        else:
            for err in serializer.errors:
                messages.add_message(
                    request, messages.WARNING, str(serializer.errors[err]))

        return reverse_lazy('core:create')


class SetMainAccountView(View):
    def get_object(self, request, object_id):
        return Account.objects.filter(id=object_id)

    def get(self, request, *args, **kwargs):
        account_id = self.kwargs.get("id")
        if self.get_object(request, account_id).exists():
            request.session["selected_account_id"] = account_id
        return reverse_lazy("core:index")


class AccountListView(ListView):
    model = Account
    template_name = "core/list.html"


class AccountUpdateView(View):
    template_name = "core/update.html"
    model = Account

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(self.model, id=self.kwargs.get("id"))
        return render(request, self.template_name, {"account": obj})

    def post(self, request, *args, **kwargs):
        obj = get_object_or_404(self.model, id=self.kwargs.get("id"))
        request_data = request.POST
        serializer = AccountSerializer(data=request_data)
        if serializer.is_valid():
            try:
                serializer.update(obj, serializer.validated_data)
                return reverse_lazy('core:list')
            except Exception as e:
                messages.add_message(request, messages.WARNING, str(e))
        else:
            for err in serializer.errors:
                messages.add_message(
                    request, messages.WARNING, str(serializer.errors[err]))
                    
        return reverse_lazy('core:update', kwargs={'id': obj.id})


class AccountDeleteView(DeleteView):
    model = Account
    success_url = reverse_lazy('core:list')
    template_name = "core/delete.html"
    pk_url_kwarg = "id"
