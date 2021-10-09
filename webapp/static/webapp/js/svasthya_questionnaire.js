window.addEventListener("load", function () {
    //var $ = django.jQuery

    $(document).ready(function () {

        $.ajaxSetup({
            headers: {
                "X-CSRFToken": Cookies.get("csrftoken")
            },
        });

        let url = '';
        if (questionnairePK) {
            url += '/appapi/svasthyaquestionnaire/' + questionnairePK + '.html';
        } else {
            url += '/appapi/svasthyaquestiontype.html';
        }
        const sqXHR = $.ajax({
            url: url,
            type: 'GET',
            dataType: 'html',
        });
        sqXHR.done(function (data, textStatus, jqXHR) {
            if (data) {
                $('#id_svasthya_questionnaire').append(data);
            } else {
                $('#id_svasthya_questionnaire').append('');
            }
        });
        sqXHR.fail(function (jqXHR, textStatus, errorThrown) {
            $('#id_ajax_error').show();
        });

    }); // `ready()`
}); // `addEventListener()`