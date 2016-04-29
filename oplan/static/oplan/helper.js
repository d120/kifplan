
//==>
//==> MessageBar helper

function MessageBar() {
    this.show = function(className, text, interval) {
      var id = "loadingWidget_" + className;
      if ($('#'+id).length == 0)
        $('<div id="'+id+'" class="messageBar"></div>').prependTo("body");
      $('#'+id).text(text).addClass(className).slideDown();
      if (interval) setInterval(function() { messageBar.hide(className); }, interval);
    };
    this.hide = function(className) {
      $("#loadingWidget_"+className).slideUp();
    };
    var loading = $("<div class='progressBar'></div>").prependTo("body").hide();
    
    $(document).ajaxStart(function() {
        loading.show();
    });
    $(document).ajaxStop(function() {
        loading.hide();
    });
    $(document).ajaxError(function(event, jqxhr, settings, thrownError) {
        console.log("ajaxError",event,jqxhr,thrownError);
        if (event.data) {
            messageBar.show("error", "Fehler: " + event.data.error, 3000);
        } else if (jqxhr.status) {
            messageBar.show("error", "Allgemeiner Fehler: " + jqxhr.status + " " + jqxhr.statusText, 3000);
        } else {
            messageBar.show("error", "Exception: " + thrownError, 3000);
        }
    });
    
};

//==>
//==> Context menu helper

function ShowContextMenu(event, menuItems) {
    $(".ddmenu.context").remove();
    var menu = $("<div class='ddmenu context'></div>");
    for(var k in menuItems) {
        var item = $("<div>"+k+"</div>").appendTo(menu);
        item.click(menuItems[k]);
    }
    $(document.body).append(menu);
    var x = event.pageX, y = event.pageY, xx = menu.width(), yy = menu.outerHeight();
    if (x+xx > window.innerWidth) x -= xx;
    if (y+yy > window.innerHeight) y -= yy;
    
    menu.css({ top: y + "px", left: x + "px" }).slideDown();
    setTimeout(function() {
      $(document).one("click", function(e) {
        menu.remove(); e.preventDefault();
      })
      $(document).one("contextmenu", function(e) {
        menu.remove(); e.preventDefault();
      })
    },1)
}
function CloseContextMenu(event, menuItems) {
    $(".ddmenu.context").remove();
}


//==>
//==> Startup Code OPLAN

$(function() {
    window.messageBar = new MessageBar();
    
    $(".menuddlink").mouseenter(function() {
        var targetSel = $(this).attr("data-target");
        if (targetSel == "#raumliste" && !$("#raumliste").length) {
            var $lst = $("<div id=raumliste class=ddmenu></div>").appendTo(this);
            $.get("/plan/api/room/?visible="+oplan.is_staff, function(rooms) {
                rooms.forEach(function(room) {
                    $lst.append(
                        (oplan.is_staff=="True" ? "<a class='right' href='/admin/oplan/room/"+escape(room.id)+"/change/'>(edit)</a> ":"") +
                        "<a href='/plan/roomcalendar/"+escape(room.number)+"'>"+room.number+"</a> " +
                        "");
                });
            });
        }
        $(targetSel).css({'left': $(this).offset().left, 'display': 'block'});
    })
    .mouseleave(function() {
        var targetSel = $(this).attr("data-target");
        $(targetSel).hide();
    });
    
});

function calendarDefaultOptions(extendOptions) {
    return $.extend({
        schedulerLicenseKey: 'GPL-My-Project-Is-Open-Source',
        
        timezone: 'local',
        allDaySlot: false,
        
        lang: 'de',
        views: {
            timelineDay: { titleFormat: 'dddd DD.MM.YYYY' },
            agendaDay: { titleFormat: 'dddd DD.MM.YYYY' },
        },
        buttonText: { timelineDay: 'Tag quer', agendaDay: 'Tag längs' },
        
        defaultDate: localStorage.calendarDate,
        
        editable: true,
        droppable: true, // this allows things to be dropped onto the calendar
        selectable: true,
        selectHelper: true,
        
        firstDay: 1,
        businessHours:{
            start: '08:00', end: '18:00',
            dow: [ 4,5,6,7]
        },
        
        drop: function() {
            $(this).remove();  //  remove the element from the "Draggable Events" list
        },
        
    }, extendOptions);
}

function getEventContextMenu(event, jsEvent) {
    var menu = {};
    if (event.view_url) {
        menu["Detailansicht"] = function() {
            location = event.view_url;
        };
    }
    if (event.termin_id) {
        menu["Als interessant markieren"] = function() {
            alert("foobar");
        };
    }
    if (oplan.mode != "akreadonly") {
        menu["Bearbeiten"] = function() {
            window.open(event.edit_url+"?_popup=1", "", "width=800,height=600,scrollbars=yes");
        };
        if (event.termin_id) {
            menu["AK bearbeiten"] = function() {
                window.open(event.edit_ak_url+"?_popup=1", "", "width=800,height=600,scrollbars=yes");
            };
        }
        if (event.editable && event.avail_id) {
            menu["Löschen"] = function() {
                oplan.api.deleteRoomAvailabilityItem(event.avail_id);
            };
        }
        if (event.editable && event.termin_id) {
            menu["Aus Plan entfernen"] = function() {
                oplan.api.saveAkTerminRaw(event.termin_id, {
                    room: null,
                    start_time: null,
                    end_time: null,
                });
            };
        }
    }
    if (event.wikilink) {
        menu["Wikiseite öffnen"] = function() {
            location = event.wikilink;
        };
    }
    return menu;
}

//==>
//==> Model code OPLAN

var oplan = {};

var STATUS = {
    'OK': 1,
    'BLOCKED': 2,
    'SHOULD_RQ': 3,
    'REQUESTED': 4,
    'SLOT': 5
};

oplan.api = {
    loadUnschedAkTermine: function() {
        var $out = $("#unsched_aktermine").html("");
        $.get("/plan/api/aktermin/?only_unscheduled=True", function(aktermins) {
            aktermins.forEach(function(akt) {
                $("<div class='fc-event'></div>")
                    .text(akt.ak_titel)
                    .appendTo($out)
                    .draggable({ zIndex: 999, revert: true, })
                    .css('background', akt.ak_color)
                    .data('event', {
                        termin_id: akt.id,
                        title: akt.ak_titel,
                        duration: akt.duration,
                    });
            });
        });
    },

    createRoomAvailability: function(start, end, room_id) {
        if (oplan.mode == "slots") {
        
            var desc = prompt("Slot von "+start.format("HH:mm")+" bis "+end.format("HH:mm")+" eintragen?");
            if (desc !== null) {

                $.post("/plan/roomevents/", {
                    start: start.toISOString(),
                    end: end.toISOString(),
                    room: room_id,
                    kommentar: desc,
                    status: 5,
                }, "json")
                .success(function() {
                    $('#calendar').fullCalendar('unselect');
                    $('#calendar').fullCalendar('refetchEvents');
                })
                .error(function(data) {
                    $('#calendar').fullCalendar('unselect');
                });
                return;
            }
        } else if (oplan.mode == "availability") {
            messageBar.show("error", "Not supported...", 1000);
        } else if (oplan.mode == "aktermin") {
            var desc = prompt("Neuen AK mit Termin von "+start.format("HH:mm")+" bis "+end.format("HH:mm")+" eintragen?");
            if (desc !== null) {
                $.post("/plan/api/ak/", {
                    'titel': desc, 'beschreibung': desc, 'leiter': '?',
                }, function(ok) {
                    $.post("/plan/api/aktermin/", {
                        ak: ok.id,
                        room: room_id,
                        start_time: start.toISOString(),
                        end_time: end.toISOString(),
                        duration: 0, status: 4,
                    }, function(ok2) {
                        $('#calendar').fullCalendar('unselect');
                        $('#calendar').fullCalendar('refetchEvents');
                    });
                });
                return;
            }
        }
        $('#calendar').fullCalendar('unselect');
    },
    onCalendarEventChange: function(event, delta, revertFunc, jsEvent, ui, view ) {
        if (oplan.mode == "slots" || oplan.mode == "availability") {
            $.post("/plan/roomevents/", {
                event_id: event.avail_id,
                start: event.start.toISOString(),
                end: event.end.toISOString(),
                room: event.resourceId,
            }, "json")
            .success(function(data) {
                $('#calendar').fullCalendar('unselect');
                $('#calendar').fullCalendar('refetchEvents');
                messageBar.show('success', ''+data.modifications+' Einträge verschoben', 1500);
            })
            .error(function(data) {
                revertFunc();
            });
        } else if (oplan.mode == "aktermin") {
            oplan.api.saveAkTermin(event);
        }
    },
    loadCalendarEvents: function(start, end, room_id, callback) {
        $.ajax({
            url: '/plan/roomevents/',
            dataType: 'json',
            cache: false,
            data: {
                // our hypothetical feed requires UNIX timestamps
                start: start.format('YYYY-MM-DD')+' 00:00:00',
                end: end.format('YYYY-MM-DD')+' 23:59:59',
                room: room_id,
            },
            success: function(doc) {
                var o=[];
                for(var i in doc.events) {
                    var e = doc.events[i];
                    if (e.termin_id) {
                        e.editable = (oplan.mode == "aktermin");
                        e.color = "#000000";
                        if (oplan.mode == "akreadonly") e.url = e.view_url;
                        e.borderColor=e.ak_color+" #000000 #000000 #000000";
                        e.className='bigtop';
                    } else {
                        e.editable = false; e.rendering = "background";
                        
                        switch(e.status) {
                            case STATUS.OK:
                                e.color = "#339933";
                                if (oplan.mode == "availability") {e.rendering="";  }
                                if (oplan.mode == "availability" && !e.mgmt_id) {e.editable=true; }
                                break;
                            case STATUS.BLOCKED:
                                e.color = "#dd2222";
                                if (oplan.mode == "availability") {e.rendering="";  }
                                if (oplan.mode == "availability" && !e.mgmt_id) {e.editable=true; }
                                break;
                            case STATUS.SLOT:
                                e.color = "#113399";
                                //e.rendering="";
                                if (oplan.mode == "slots") {e.rendering=""; e.editable=true;}
                                break;
                            case STATUS.SHOULD_REQUEST: 
                                e.color = "#999933";
                            case STATUS.REQUESTED:
                                e.color = "#66bb33";
                                if (oplan.mode == "availability") {e.rendering=""; }
                                
                                break;
                        }
                    }
                    o.push(e);
                }
                callback(o);
            }
        });
    },

    saveAkTermin: function (event) {
        oplan.api.saveAkTerminRaw(event.termin_id, {
            room: event.resourceId,
            start_time: event.start.toISOString(),
            end_time: event.end.toISOString(),
        });
    },
    saveAkTerminRaw: function(terminId, postData) {
        $.ajax({
            url: "/plan/api/aktermin/"+terminId+"/", 
            data: postData,
            method: "PATCH",
            success: function(ok) {
                $('#calendar').fullCalendar('unselect');
                $('#calendar').fullCalendar('refetchEvents');
                messageBar.show('success', 'Änderungen am AK-Termin '+event.titel+' wurden gespeichert', 1500);
                oplan.api.loadUnschedAkTermine();
            }
        });
    },
    deleteRoomAvailabilityItem: function(terminId) {
        $.ajax({
            url: "/plan/api/slot/"+terminId+"/", 
            data: {},
            method: "DELETE",
            success: function(ok) {
                    $('#calendar').fullCalendar('unselect');
                    $('#calendar').fullCalendar('refetchEvents');
                    messageBar.show('success', 'Raumverfügbarkeitseintrag wurde gelöscht.', 1500);
            }
        });
    },

}; //end oplan.api

//==>
//==> Django CSRF shit

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});