from django.contrib.auth.decorators import user_passes_test

def landlord_required(view_func):
    return user_passes_test(
        lambda u: u.is_authenticated and u.is_landlord()
    )(view_func)

def caretaker_required(view_func):
    return user_passes_test(
        lambda u: u.is_authenticated and u.is_caretaker()
    )(view_func)
