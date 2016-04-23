
$(function() {
    
    // code für Datums-"Checkboxen" in kiffel_person_changelist
    $("span[data-mark-field]").click(function() {
        var $el = $(this);
        var field_name = $el.attr('data-mark-field');
        
        var data = {};
        if ($el.hasClass("datemark-yes")) {
            if (!confirm("Möchtest du die Markierung \"" + $el.attr("title") + "\" wirklich aufheben?"))
                return;
            data[field_name] = null;
        } else {
            data[field_name] = moment().toISOString();
        }
        $.ajax({
            url: '/api/v1/kiffels/' + $el.attr('data-mark-id') + '/',
            method: 'PATCH',
            data: data,
        }).success(function(ok) {
            $el.removeClass("datemark-yes datemark-no");
            if (ok[field_name]) $el.addClass("datemark-yes"); else $el.addClass("datemark-no");
        });
    });
    
    var filterColors = [ "#555555", "#448844", "#993333" ];
    $("#changelist-filter ul").each(function() {
        var $children = $("li", this);
        if ($children.length == 3)
            $children.css({"display": "inline-block", "margin": "0 10px 0 0", "padding": "3px 10px"})
            .each(function(idx) {
                if ($(this).is(".selected")) $(this).css({"background":filterColors[idx], "border": "0"}).find("a").css("color","white");
            });
    });
    
});
