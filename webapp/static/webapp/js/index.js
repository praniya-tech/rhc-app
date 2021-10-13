window.addEventListener("load", function () {
    //var $ = django.jQuery

    $(document).ready(function () {

        $.ajaxSetup({
            headers: {
                "X-CSRFToken": Cookies.get("csrftoken")
            },
        });

        const lastAssessmentDateXHR = $.ajax({
            url: 'appapi/svasthyaquestionnaire/last_assessment_date.html',
            type: 'GET',
            dataType: 'html',
        });
        lastAssessmentDateXHR.done(function (data, textStatus, jqXHR) {
            $('#id_last_health_assessment').empty().append(data);
        });
        lastAssessmentDateXHR.fail(function (jqXHR, textStatus, errorThrown) {
            $('#id_last_health_assessment').empty();
            $('#id_ajax_error').show();
            // $('#id_ajax_error_message').text(
            //     `${textStatus.toUpperCase()}: ${errorThrown}.`);
        });

    }); // `ready()`
}); // `addEventListener()`