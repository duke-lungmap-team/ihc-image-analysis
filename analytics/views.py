from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render


@login_required
def permission_denied(request):
    raise PermissionDenied


# The anchors used by Angular, i.e. any paths starting with '#'
# never make it to the server, so server side re-direction will
# never really be useful, thus we disable 'redirect_field_name'
@login_required(redirect_field_name=None)
def ihc_app(request):
    return render(
        request,
        'ihc_app.html',
        {}
    )
