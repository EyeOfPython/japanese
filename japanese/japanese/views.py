from pyramid.view import view_config
from japanese import db

@view_config(route_name="home", renderer="home.html")
def home_view(request):
    return {}
    
@view_config(route_name="kanji", renderer="JSON")
def kanji_view(request):
    query = {}
    if 'from' in request.GET and 'to' in request.GET:
        query['freq'] = { '$qte': int(request.GET['from']), '$lte': int(request.GET['to']) }
    return list( db.kanjis.find(query) )