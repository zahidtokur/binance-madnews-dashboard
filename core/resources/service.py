from decimal import Decimal

from core.models import Pair


class PairService():
    def get_pair_object(self, pair):
        if isinstance(pair, Pair):
            pair_obj = pair

        try:
            pair_obj = Pair.objects.get(name=pair)
        except Pair.DoesNotExist:
            pair_obj = None

        return pair_obj

    def delete_pairs(self, all=False, exclude_names=None):
        if all:
            Pair.objects.all().delete()
        elif exclude_names and isinstance(exclude_names, list):
            Pair.objects.exclude(name__in=exclude_names).delete()

    def update_or_create_pair(self, account, name, qty_precision):
        try:
            pair = Pair.objects.get(account=account, name=name)
            pair.quantity_precision = qty_precision
            pair.save()
        except Pair.DoesNotExist:
            pair = Pair.objects.create(
                account=account, name=name,
                quantity_precision=qty_precision)
        return pair


class AccountService():
    def update_balance(self, account, amount):
        account.balance = Decimal(amount).quantize(Decimal('.00'))
        account.save()
        return account.balance


class OrderService():
    def calculate_quantity(self, balance, multiplier, price, precision):
        notional_size = balance * Decimal(multiplier)
        quantity = notional_size / price
        if precision == 0:
            return quantity.quantize(Decimal('0'))
        return quantity.quantize(Decimal('.' + '0' * precision))
