console.log('Started', self);
self.addEventListener('install', function(event) {
  self.skipWaiting();
  console.log('Installed', event);
});
self.addEventListener('activate', function(event) {
  console.log('Activated', event);
});
self.addEventListener('push', function(event) {
    console.log('Push message received', event);
    event.waitUntil(
        self.registration.pushManager.getSubscription()
        .then(function(subscription) {
            var token = getToken(subscription);
            return fetch('/news/api/notifications/', {
                method: 'post',
                headers: {"Content-Type": "application/x-www-form-urlencoded"},
                body: "token=" +escape( token )
            })
            .then(function(response) { return response.json(); })
            .then(function(data) {
                
                for(var i in data.items) {
                    var d = data.items[i];
                    d.data = d;
                    d.tag = d.identifier;
                    noti = self.registration.showNotification(d.title, d);
                }
                return noti;
            })
        }));
});


function getToken(subscription){
    var token = subscription.endpoint;
    var gcmPrefix = "https://android.googleapis.com/gcm/send/";
    if (token.indexOf(gcmPrefix) === 0) token = token.substring(gcmPrefix.length);
    return token;
}

self.addEventListener('notificationclick', function(event) {
    console.log('Notification click: tag ', event.notification.tag);
    console.log('Notification click: link ', event.notification.data.link);
    event.notification.close();
    var url = event.notification.data.link;
    event.waitUntil(
        clients.matchAll({
            type: 'window'
        })
        .then(function(windowClients) {
            for (var i = 0; i < windowClients.length; i++) {
                var client = windowClients[i];
                if (client.url === url && 'focus' in client) {
                    client.navigate(url);
                    return client.focus();
                }
            }
            if (clients.openWindow) {
                return clients.openWindow(url);
            }
        })
    );
});

