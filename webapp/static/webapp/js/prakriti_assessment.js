window.addEventListener("load", function () {
    //var $ = django.jQuery

    $(document).ready(function () {

        $.ajaxSetup({
            headers: {
                "X-CSRFToken": Cookies.get("csrftoken")
            },
        });

        const pqFormXHR = $.ajax({
            url: 'appapi/prakritiquestionnaire.html',
            type: 'GET',
            dataType: 'html',
        });
        pqFormXHR.done(function (html, textStatus, jqXHR) {
            if (html) {
                $('#id_property_types').empty().append(html);
            } else {
                showNewPrakritiQuestionnaire();
            }
        });
        pqFormXHR.fail(function (jqXHR, textStatus, errorThrown) {
            $('#id_property_types').empty();
            $('#id_ajax_error').show();
        });

        function showNewPrakritiQuestionnaire() {
            const pqAddXHR = $.ajax({
                url: 'appapi/prakritiquestionnaire/add.html',
                type: 'GET',
                dataType: 'html',
            });
            pqAddXHR.done(function (propertyTypes, textStatus, jqXHR) {
                $('#id_property_types').empty().append(propertyTypes);
            });
            pqAddXHR.fail(function (jqXHR, textStatus, errorThrown) {
                $('#id_property_types').empty();
                $('#id_ajax_error').show();
            });
        }

    }); // `ready()`
}); // `addEventListener()`