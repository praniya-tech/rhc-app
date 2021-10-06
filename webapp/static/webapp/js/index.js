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
            $('#id_last_health_assessment').append(data);
        });
        lastAssessmentDateXHR.fail(function (jqXHR, textStatus, errorThrown) {
            alert(textStatus);
        });

    }); // `ready()`
}); // `addEventListener()`