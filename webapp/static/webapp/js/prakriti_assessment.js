window.addEventListener("load", function () {
    //var $ = django.jQuery

    $(document).ready(function () {

        $.ajaxSetup({
            headers: {
                "X-CSRFToken": Cookies.get("csrftoken")
            },
        });

        const pqFormXHR = $.ajax({
            url: 'appapi/prakritipropertytype.html',
            type: 'GET',
            dataType: 'html',
        });
        pqFormXHR.done(function (data, textStatus, jqXHR) {
            $('#id_property_types').append(data);
        });
        pqFormXHR.fail(function (jqXHR, textStatus, errorThrown) {
            alert(textStatus);
        });

    }); // `ready()`
}); // `addEventListener()`