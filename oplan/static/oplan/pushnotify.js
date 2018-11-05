if(!window.oplan) window.oplan = {};

oplan.isPushEnabled = false;

function sendSubscriptionToServer(subscription) {
    
    console.log("sending subscription to server", subscription, window.localStorage.pushID);
    if (window.localStorage.pushID) {
        return $.post( "/news/api/push/", {
            "type": "WebPush",
            "pushID" : window.localStorage.pushID,
            "subscription" : JSON.stringify(subscription.toJSON())
        });
    } else {
        return $.post( "/news/api/push/", {
            "type": "WebPush",
            "subscription": JSON.stringify(subscription.toJSON())
        }, function(r,s,t) {
            console.log("push subscription result",r,s,t);
            window.localStorage.pushID = r.pushID;

        }, "json");
    }
    window.localStorage.pushID = token;
}
function subscribeToTermin() {
    $.post( "/news/api/push/", {
        "type": "WebPush",
        "pushID" : window.localStorage.pushID,
        "ak_id": oplan.current_ak_id
    }, function(success) {
        $("#bookmark_btn").attr("disabled",true);
    });
}

var STATE_REGISTERED=1, STATE_UNREGISTERED=2, STATE_NOT_SUPPORTED=3, STATE_LOADING=4;
function updateUiState(state) {
    console.log("pushbutton state",state);
    var pushButton = document.querySelector('.js-push-button');
    if (pushButton) {
        pushButton.disabled = state == STATE_NOT_SUPPORTED || state == STATE_LOADING;
        
        if(state != STATE_NOT_SUPPORTED)pushButton.style.display="inherit";
        if (state == STATE_REGISTERED) pushButton.textContent = 'Push-Nachrichten ausschalten';
        if (state == STATE_UNREGISTERED) pushButton.textContent = 'Push-Nachrichten einschalten';
        
    }
    var $bm = $("#bookmark_btn");
    if ($bm) {
        $bm.attr("disabled", state == STATE_NOT_SUPPORTED || state == STATE_LOADING);
    }
    
}


//==>
//==> dealing with push api
// boilerplate stuff from the internet
// https://github.com/GoogleChrome/samples/blob/gh-pages/push-messaging-and-notifications/main.js

$(function() {
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/service_worker.js')
        .then(initialiseState);
        $(".js-push-button").click(function() {
            if (oplan.isPushEnabled) unsubscribe();
            else subscribe();
        });
        $("#bookmark_btn").click(function() {
            
            if (!oplan.isPushEnabled) subscribe().then(subscribeToTermin);
            else subscribeToTermin();
            
        });
    } else {
        console.warn('Service workers aren\'t supported in this browser.');
    }
});

// Once the service worker is registered set the initial state
function initialiseState() {
  // Are Notifications supported in the service worker?
  if (!('showNotification' in ServiceWorkerRegistration.prototype)) {
    console.warn('Notifications aren\'t supported.');
    return;
  }

  // Check the current Notification permission.
  // If its denied, it's a permanent block until the
  // user changes the permission
  if (Notification.permission === 'denied') {
    console.warn('The user has blocked notifications.');
    return;
  }

  // Check if push messaging is supported
  if (!('PushManager' in window)) {
    console.warn('Push messaging isn\'t supported.');
    return;
  }

  // We need the service worker registration to check for a subscription
  navigator.serviceWorker.ready.then(function(serviceWorkerRegistration) {
    // Do we already have a push message subscription?
    serviceWorkerRegistration.pushManager.getSubscription()
      .then(function(subscription) {
        // Enable any UI which subscribes / unsubscribes from
        // push messages.

        if (!subscription) {
          // We aren’t subscribed to push, so set UI
          // to allow the user to enable push
          updateUiState(STATE_UNREGISTERED);
          return;
        }

        // Keep your server in sync with the latest subscription
        sendSubscriptionToServer(subscription);

        // Set your UI to show they have subscribed for
        // push messages
        updateUiState(STATE_REGISTERED);
        oplan.isPushEnabled = true;
      })
      .catch(function(err) {
        console.warn('Error during getSubscription()', err);
      });
  });
}


function unsubscribe() {
  updateUiState(STATE_LOADING);

  navigator.serviceWorker.ready.then(function(serviceWorkerRegistration) {
    // To unsubscribe from push messaging, you need get the
    // subcription object, which you can call unsubscribe() on.
    serviceWorkerRegistration.pushManager.getSubscription().then(
      function(pushSubscription) {
        // Check we have a subscription to unsubscribe
        if (!pushSubscription) {
          // No subscription object, so set the state
          // to allow the user to subscribe to push
          oplan.isPushEnabled = false;
          updateUiState(STATE_UNREGISTERED);
          return;
        }

        // TODO: Make a request to your server to remove
        // the users data from your data store so you
        // don't attempt to send them push messages anymore

        // We have a subcription, so call unsubscribe on it
        pushSubscription.unsubscribe().then(function() {
          updateUiState(STATE_REGISTERED);
          oplan.isPushEnabled = false;
          $.ajax({
            url:"/news/api/push/?pushID="+window.localStorage.pushID,
            method:"DELETE",
            success:function(r) {delete window.localStorage["pushID"];}
          });
        }).catch(function(e) {
          // We failed to unsubscribe, this can lead to
          // an unusual state, so may be best to remove
          // the subscription id from your data store and
          // inform the user that you disabled push

          window.Demo.debug.log('Unsubscription error: ', e);
          pushButton.disabled = false;
        });
      }).catch(function(e) {
        window.Demo.debug.log('Error thrown while unsubscribing from ' +
          'push messaging.', e);
      });
  });
}

function subscribe() {
  // Disable the button so it can't be changed while
  // we process the permission request
  updateUiState(STATE_LOADING);

  return navigator.serviceWorker.ready.then(function(serviceWorkerRegistration) {
    return serviceWorkerRegistration.pushManager.subscribe({userVisibleOnly: true})
      .then(function(subscription) {
        // The subscription was successful
        oplan.isPushEnabled = true;
        updateUiState(STATE_REGISTERED);

        // TODO: Send the subscription subscription.endpoint
        // to your server and save it to send a push message
        // at a later date
        return sendSubscriptionToServer(subscription);
      })
      .catch(function(e) {
        if (Notification.permission === 'denied') {
          // The user denied the notification permission which
          // means we failed to subscribe and the user will need
          // to manually change the notification permission to
          // subscribe to push messages
          console.warn('Permission for Notifications was denied');
          updateUiState(STATE_NOT_SUPPORTED);
        } else {
          // A problem occurred with the subscription, this can
          // often be down to an issue or lack of the gcm_sender_id
          // and / or gcm_user_visible_only
          console.warn('Unable to subscribe to push.', e);
          updateUiState(STATE_UNREGISTERED);
        }
      });
  });
}