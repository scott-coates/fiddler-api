from django.dispatch import Signal

artist_url_discovered = Signal(providing_args=['url'])
