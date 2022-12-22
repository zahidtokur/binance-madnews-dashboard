from celery import shared_task
from celery.utils.log import get_task_logger

from core.models import Account, Pair
from core.integrations.binance_futures.integration import Integration

logger = get_task_logger(__name__)


@shared_task
def update_balance_task():
    accounts = Account.objects.all()
    for account in accounts:
        try:
            integration = Integration(account, account.conf)
            integration.run_command("update_balance")
        except Exception as e:
            logger.warning(e)
    return True


@shared_task
def get_pairs_task():
    accounts = Account.objects.all()
    for account in accounts:
        try:
            integration = Integration(account, account.conf)
            integration.run_command("get_pairs")
        except Exception as e:
            logger.warning(e)
    return True


@shared_task
def set_cross_margin_task():
    accounts = Account.objects.all()
    for account in accounts:
        try:
            pairs = Pair.objects.filter(account=account)
            integration = Integration(account, account.conf)
            integration.run_command("set_cross_margin", objects=pairs)
        except Exception as e:
            logger.warning(e)
    return True


@shared_task
def set_leverage_task():
    accounts = Account.objects.all()
    for account in accounts:
        try:
            pairs = Pair.objects.filter(account=account)
            integration = Integration(account, account.conf)
            integration.run_command("set_leverage", objects=pairs)
        except Exception as e:
            logger.warning(e)
    return True
