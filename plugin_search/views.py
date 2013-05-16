# -*- coding: utf-8 -*-
from django.template import RequestContext
from ionyweb.website.rendering.utils import render_view
from .forms import OrgSearch
from coop_local.models import Organization
from coop_local.models.local_models import ORGANIZATION_STATUSES
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# from ionyweb.website.rendering.medias import CSSMedia, JSMedia, JSAdminMedia
MEDIAS = (
    # App CSS
    # CSSMedia('plugin_search.css'),
    # App JS
    # JSMedia('plugin_search.js'),
    # Actions JSAdmin
    # JSAdminMedia('plugin_search_actions.js'),
    )

def index_view(request, plugin):
    form = OrgSearch(request.POST)
    if form.is_valid():
        orgs = Organization.objects.filter(status=ORGANIZATION_STATUSES.VALIDATED)
        orgs = orgs.filter(title__icontains=form.cleaned_data['q'])
        if form.cleaned_data['org_type'] == 'fournisseur':
            orgs = orgs.filter(is_provider=True)
            if form.cleaned_data['prov_type']:
                orgs = orgs.filter(agreement_iae=form.cleaned_data['prov_type'])
        if form.cleaned_data['org_type'] == 'acheteur-public':
            orgs = orgs.filter(is_customer=True, customer_type=1)
        if form.cleaned_data['org_type'] == 'acheteur-prive':
            orgs = orgs.filter(is_customer=True, customer_type=2)
        sector = form.cleaned_data['sector']
        if sector:
            descendants = sector.get_descendants(include_self=True)
            orgs = orgs.filter(offer__activity__in=descendants)
    else:
        orgs = Organization.objects.none()
    paginator = Paginator(orgs, 10)
    page = request.GET.get('page')
    try:
        orgs_page = paginator.page(page)
    except PageNotAnInteger:
        orgs_page = paginator.page(1)
    except EmptyPage:
        orgs_page = paginator.page(paginator.num_pages)
    return render_view('plugin_search/index.html',
                       {'object': plugin, 'form': form, 'orgs': orgs_page},
                       MEDIAS,
                       context_instance=RequestContext(request))