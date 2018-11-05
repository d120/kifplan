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

    var item = event.data.json()
    
    event.waitUntil(
        self.registration.showNotification(item.title, {
        body: item.body,
        icon: item.icon,
        link: item.link
        })
    );
/*
    event.waitUntil(
        self.registration.pushManager.getSubscription()
        .then(function(subscription) {
            
            return fetch('/news/api/notifications/', {
                method: 'post',
                headers: {"Content-Type": "application/x-www-form-urlencoded"},
                body: "pushID=" +escape( localStorage.pushID )+"&subscription="+escape(JSON.stringify(subscription.toJSON()))
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
        }));*/
});



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

