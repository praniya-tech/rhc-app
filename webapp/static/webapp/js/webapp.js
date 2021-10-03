window.addEventListener("load", function () {
    //var $ = django.jQuery

    $(document).ready(function () {

        $.ajaxSetup({
            headers: {
                "X-CSRFToken": Cookies.get("csrftoken")
            },
        });

        var removeActive = function () {
            $(".nav-sidebar a").removeClass("active");
        };
        $(".nav-sidebar li a").click(function () {
            // removeActive();
            // $(this).addClass('active');
        });
        removeActive();
        $(".nav-sidebar li a[href='" + location.pathname + "']").addClass("active");
        $("a[href='" + location.pathname + "']").parents(
            "li#id_assessments_menu").addClass("menu-open");
    }); // `ready()`
}); // `addEventListener()`