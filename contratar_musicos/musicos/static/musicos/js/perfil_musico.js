/**
 * Created by h3dx0 on 2/25/17.
 */
$(function () {
    $(".owl-carousel").owlCarousel(
        {
            animateOut: 'slideOutDown',
            animateIn: 'flipInX',
            loop: true,
            margin: 10,
            items:1

        }
    );
    $('#datos-contacto').hide();
    $('#btn-datos-contacto').on('click', function () {
        var musico = $(this).data('musico');
        var currentdate = new Date();
        var datetime = currentdate.getMinutes();
        var current_hora = currentdate.getHours();
        var musico_visto = sessionStorage.getItem('musico-visto');
        var minuto_guardado = sessionStorage.getItem('min-inicio-detalle');
        var hora_guardada = sessionStorage.getItem('hora-inicio-detalle');
        var resta = datetime - minuto_guardado;
        if (musico_visto != musico) {
            sessionStorage.setItem('min-inicio-detalle', datetime);
            sessionStorage.setItem('hora-inicio-detalle', current_hora);
            sessionStorage.setItem('musico-visto', musico);
            $.ajax({
                url: '/registro/visita/',
                method: 'GET',
                data: {'musico': musico},
                success: function (response) {
                    if (response.rc != 0) {
                        alert(response.msg);
                    }
                }
            });
        } else {
            if (resta >= 2 || hora_guardada != current_hora) {
                sessionStorage.setItem('min-inicio-detalle', datetime);
                sessionStorage.setItem('hora-inicio-detalle', current_hora);
                sessionStorage.setItem('musico-visto', musico);
                $.ajax({
                    url: '/registro/visita/',
                    method: 'GET',
                    data: {'musico': musico},
                    success: function (response) {
                        if (response.rc != 0) {
                            alert(response.msg);
                        }
                    }
                });

            }
        }
    })
});