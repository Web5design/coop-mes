# -*- coding: utf-8 -*-
from django.template import RequestContext
from ionyweb.website.rendering.utils import render_view
from .forms import OrgSearch

# from ionyweb.website.rendering.medias import CSSMedia, JSMedia, JSAdminMedia
MEDIAS = (
    # App CSS
    # CSSMedia('plugin_home_search.css'),
    # App JS
    # JSMedia('plugin_home_search.js'),
    # Actions JSAdmin
    # JSAdminMedia('plugin_home_search_actions.js'),
    )

def index_view(request, plugin):
    form = OrgSearch(request.GET)
    return render_view('plugin_home_search/index.html',
                       {'object': plugin, 'form': form},
                       MEDIAS,
                       context_instance=RequestContext(request))
