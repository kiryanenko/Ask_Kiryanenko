from channels.routing import ProtocolTypeRouter, URLRouter

import questions.routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': URLRouter(
            questions.routing.websocket_urlpatterns
    )
})