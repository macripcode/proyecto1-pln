(function($) {

    $('#btn_ingresar_up').on('click', function(){
            var texto= $('#area_texto1').val();
            $.ajax({
              url: '/process',
              data:{'texto': texto},
              type : 'POST',
              success: function (data) {
                $('#resultados').html(data.salida);
              }

       });

            //event.preventDefault();
    });

})(jQuery); // End of use strict
