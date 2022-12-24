from core.models import Account

def accounts_list(request):
    return {
        "accounts": Account.objects.all(),
    }
