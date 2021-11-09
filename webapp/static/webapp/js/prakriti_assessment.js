window.addEventListener("load", function () {
    //var $ = django.jQuery

    $(document).ready(function () {

        $.ajaxSetup({
            headers: {
                "X-CSRFToken": Cookies.get("csrftoken")
            },
        });

        const pqFormXHR = $.ajax({
            url: 'appapi/prakritiquestionnaire.json',
            type: 'GET',
            dataType: 'json',
        });
        pqFormXHR.done(function (questionnaires, textStatus, jqXHR) {
            if (questionnaires.length > 0) {
                $('#id_property_types').empty().append(data);
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