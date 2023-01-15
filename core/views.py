import copy
from decimal import Decimal

from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView
from django.contrib import messages
from django.http import HttpResponseRedirect

from core.models import Account
from core.integrations.binance_futures.integration import Integration
from core.resources.serializers import AccountSerializer, OrderSerializer
from core.resources.service import OrderService, PairService
from core.tasks import get_pairs_task, update_balance_task, set_cross_margin_task, set_leverage_task


class IndexView(View):
    template_name = "core/index.html"
    pair_service = PairService()
    order_service = OrderService()

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

    def post(self, request, *args, **kwargs):
        request_data = copy.deepcopy(request.POST)
        if "buy" in request_data:
            request_data.update({"side": "BUY"})
        else:
            request_data.update({"side": "SELL"})

        serializer = OrderSerializer(data=request_data)
        if not serializer.is_valid():
            for err in serializer.errors:
                messages.add_message(
                    request, messages.WARNING, str(serializer.errors[err]))
            return HttpResponseRedirect(reverse('core:index'))

        order_data = serializer.validated_data
        account = self._get_selected_account(request.session)
        integration = Integration(account)

        pair = self.pair_service.get_pair_object(
            order_data.get("pair"))
        pair_price = integration.run_command(
            "get_pair_price", pair=pair)

        quantity = self.order_service.calculate_quantity(
            balance=account.balance,
            multiplier=order_data.get("multiplier"),
            price=pair_price,
            precision=pair.quantity_precision)

        order_data.update(
            {"symbol": pair.name, "quantity": quantity})

        order_result = integration.run_command(
            "create_order", order_params=order_data)

        if order_result:
            pair = order_result.get("symbol")
            avg_price = order_result.get("avgPrice")
            quantity = order_result.get("executedQty")
            side = order_result.get("side")
            size = Decimal(avg_price) * Decimal(quantity)
            messages.add_message(request, messages.SUCCESS,
                                 f"{size} USDT {side} order executed on {pair}, entry price : {avg_price}")
        else:
            messages.add_message(request, messages.WARNING,
                                 "Unexpected error on order creation")
        return HttpResponseRedirect(reverse('core:index'))


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
                return HttpResponseRedirect(reverse('core:index'))
            except Exception as e:
                messages.add_message(request, messages.WARNING, str(e))
        else:
            for err in serializer.errors:
                messages.add_message(
                    request, messages.WARNING, str(serializer.errors[err]))

        return HttpResponseRedirect(reverse('core:create'))


class SetMainAccountView(View):
    def get_object(self, request, object_id):
        return Account.objects.filter(id=object_id)

    def get(self, request, *args, **kwargs):
        account_id = self.kwargs.get("id")
        if self.get_object(request, account_id).exists():
            request.session["selected_account_id"] = account_id
        return HttpResponseRedirect(reverse("core:index"))


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
                return HttpResponseRedirect(reverse('core:list'))
            except Exception as e:
                messages.add_message(request, messages.WARNING, str(e))
        else:
            for err in serializer.errors:
                messages.add_message(
                    request, messages.WARNING, str(serializer.errors[err]))
                    
        return HttpResponseRedirect(reverse('core:update', kwargs={'id': obj.id}))


class AccountDeleteView(DeleteView):
    model = Account
    success_url = reverse_lazy('core:list')
    template_name = "core/delete.html"
    pk_url_kwarg = "id"
    context_object_name = "account"


class UpdateBalanceView(View):
    def get(self, request, *args, **kwargs):
        update_balance_task()
        return HttpResponseRedirect(reverse('core:index'))


class GetPairsView(View):
    def get(self, request, *args, **kwargs):
        get_pairs_task()
        return HttpResponseRedirect(reverse('core:index'))


class SetCrossMarginView(View):
    def get(self, request, *args, **kwargs):
        set_cross_margin_task()
        return HttpResponseRedirect(reverse('core:index'))


class SetLeverageView(View):
    def get(self, request, *args, **kwargs):
        set_leverage_task()
        return HttpResponseRedirect(reverse('core:index'))
