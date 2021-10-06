window.addEventListener("load", function () {
    //var $ = django.jQuery

    $(document).ready(function () {

        $.ajaxSetup({
            headers: {
                "X-CSRFToken": Cookies.get("csrftoken")
            },
        });

        const sqListXHR = $.ajax({
            url: 'appapi/svasthyaquestionnaire.html',
            type: 'GET',
            dataType: 'html',
        });
        sqListXHR.done(function (data, textStatus, jqXHR) {
            if (data) {
                $('#id_no_questionnaires').hide();
                $('#id_svasthya_questionnaires_card').append(data);
            } else {
                $('#id_no_questionnaires').show();
                $('#id_svasthya_questionnaires_card').append('');
            }
        });
        sqListXHR.fail(function (jqXHR, textStatus, errorThrown) {
            alert(textStatus);
        });

    }); // `ready()`
}); // `addEventListener()`