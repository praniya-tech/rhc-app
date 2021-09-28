window.addEventListener("load", function () {
    //var $ = django.jQuery

    $(document).ready(function () {

        $.ajaxSetup({
            headers: {
                "X-CSRFToken": Cookies.get("csrftoken")
            },
        });

        //alert(RHCAPP['CRF_PATIENT_PK']);
        const CRF_PATIENT_PK = RHCAPP['CRF_PATIENT_PK'];

        const sqListXHR = $.ajax({
            url: 'appapi/svasthyaquestionnaire.json', // + CRF_PATIENT_PK,
            type: 'GET',
            dataType: 'json',
        });
        sqListXHR.done(function (data, textStatus, jqXHR) {
            if (Array.isArray(data) && data.length) {
                $('#id_no_questionnaires').hide();
            } else {
                $('#id_no_questionnaires').show();
            }
        });
        sqListXHR.fail(function (jqXHR, textStatus, errorThrown) {
            alert(textStatus);
        });

    }); // `ready()`
}); // `addEventListener()`