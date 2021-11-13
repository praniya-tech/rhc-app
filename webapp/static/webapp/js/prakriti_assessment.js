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
        });
        pqFormXHR.done(function (html, textStatus, jqXHR) {
            if (html) {
                $('#id_prakriti_questionnaire').empty().append(html);
                showRitucharya();
            } else {
                showNewPrakritiQuestionnaire();
            }
        });
        pqFormXHR.fail(function (jqXHR, textStatus, errorThrown) {
            $('#id_prakriti_questionnaire').empty();
            $('#id_ajax_error').show();
        });

        function showRitucharya() {
            const pqRitucharyaXHR = $.ajax({
                url: 'appapi/prakritiquestionnaire/ritucharya.html',
                type: 'GET',
            });
            pqRitucharyaXHR.done(function (html, textStatus, jqXHR) {
                $('#id_ritucharya').empty().append(html);
            });
            pqRitucharyaXHR.fail(function (jqXHR, textStatus, errorThrown) {
                $('#id_ritucharya').empty();
                $('#id_ajax_error').show();
            });
        }

        function showNewPrakritiQuestionnaire() {
            const pqAddXHR = $.ajax({
                url: 'appapi/prakritiquestionnaire/add.html',
                type: 'GET',
            });
            pqAddXHR.done(function (propertyTypes, textStatus, jqXHR) {
                $('#id_prakriti_questionnaire').empty().append(propertyTypes);
            });
            pqAddXHR.fail(function (jqXHR, textStatus, errorThrown) {
                $('#id_prakriti_questionnaire').empty();
                $('#id_ajax_error').show();
            });
        }

    }); // `ready()`
}); // `addEventListener()`