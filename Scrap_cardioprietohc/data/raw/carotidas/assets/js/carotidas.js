$(document).ready(function() {

	$('.btnSubmit').click(function(){
		$('#formCarotidas').submit();
	});
	
	// Submit del form para guardar los datos en BD
	$('#formCarotidas').submit(function(){

		var action   = $(this).attr('action');
		var idHC	 = $('#idHC').val();
		$('.divBtns .btn').attr('disabled', 'disabeld');
		$('#spnGuardar').html('Guardando...');
		$('#ldgGuardar').css('display', 'inline-block');

		$.ajax({
			   
		    type: "POST",
		    url: action,
		    data: $(this).serialize(),
		    dataType: "json",
		    async: false, 
		    success: function(data) {

		    	if( data.exito ){
		    		$('#idEstudio').val(data.id);
		    	} else {
		    		$('#msj').val('Se produjo un error, inténtelo más tarde.');
		    	}

		    	var url = action.substr(0, action.lastIndexOf('/')) + '/imprimirEstudio/' + data.id + "/" + idHC;
				window.open(url);

				$('#ldgGuardar').hide();
				$('#spnGuardar').html('Guardar').show();
				$('.divBtns .btn').removeAttr('disabled');
		    },
		    error: function(){
		    	$('#msjPaciente').show();
				$('#ldgGuardar').hide();
				$('#spnGuardar').html('Guardar').show();
				$('.divBtns .btn').removeAttr('disabled');
		    }
		});

		return false;
	});

	// Para habilitar el box de comentarios y generar el pre informe solo para los combobox
	$('.boxInforme select.form-control').change(function(){

		var nodo = $( this ).parent().next();

		if( $(this).val() == '-1'){
			
			nodo.show();
		} else {
			nodo.hide();
		}

		var orden = $(this).attr('data-id');
		// Si tengo algún valor lo muestro en el pre informe
		if( $(this).val() != '' ){

			// Obtengo el contenido seleccionado
			var contenido = $( 'select[data-id="' + orden + '"] option:selected' ).text();
			
			// Obtengo el nombre del label
			var label = $(this).parent().prev().text();
			$('.orden_' + orden).html('<b>' + label + '</b>' + ' ' + contenido);

		} else {
			// Si no elijo nada quito el elemento del pre informe.
			$('.orden_' + orden).html(' ');
		}
	});

	// Comentarios del pre informe
	$('.boxComentario textarea').change(function(){

		if( $(this).val() ){
			var orden = $(this).attr('data-id');
			$('.orden_' + orden).html($('.orden_' + orden).html() + ' ' + $(this).val());
		}
	});

	$('.carIntDer, .carExtDer, .carIntIzq, .carExtIzq, .artVertebrales, .sugerencias').click(function(){

		if( $(this).val() == '0' || $(this).attr('class') == 'sugerencias'){

			var nodo = $(this).parent().next();
			$(nodo).children().find('.inputBox').attr('checked', false);

			// Cargo el valor al pre informe
			var orden = $(this).parent().parent().attr('data-id');
			var contenido = $( this ).next().text();

			// Obtengo el nombre del label
			var label = $(this).parent().parent().prev().text();
			$('.orden_' + orden).html('<b>' + label + '</b>' + ' ' + contenido);
		}

	});

	$('.boxLesiones .inputBox').click(function(){
		var nodo = $(this).parent().parent().prev();
		$(nodo).children().first().attr('checked', false);
		$(nodo).children().eq(3).prop('checked', true);

		// Obtengo el nombre del label
		var label = $(this).parent().parent().parent().prev().text();

		// Obtengo el subtítulo 
		var subtitulo = $(this).parent().parent().prev().children().eq(4).text();

		// Cargo el valor al pre informe
		var contenido = '';
		var hijos = $(this).parent().parent().children().find('input:checked');
		var nombre = $(this).attr('name');

		hijos.each(function(){
			contenido += $(this).next().text() + '. ' ;
		});
		
		var orden = $(this).parent().parent().parent().attr('data-id');
		$('.orden_' + orden).html('<b>' + label + '</b>' + ' ' + subtitulo +  ' ' + contenido);
	});

	// Limpio los datos de los campos radio button
	$('.clearData').click(function(){
		$(this).parent().prev().find('input').attr('checked', false);
		var orden = $(this).parent().prev().attr('data-id');
		$('.boxPreInforme .orden_' + orden).html('');
	});

	// Triggers
	$('.boxInforme select.form-control').trigger('change');
	$('.boxComentario textarea').trigger('change');
	$('.carIntDer:checked, .carExtDer:checked, .carIntIzq:checked, .carExtIzq:checked, .artVertebrales:checked').trigger('click');
	$('.sugerencias:checked').trigger('click');
	$('.boxLesiones input:checked').trigger('click');


	// Footer
	var height = $('body').height();
	var hWindow = $(window).height();

	if( height < hWindow)
		$('.footer').addClass('bottom');
	
  //Control de solo numeros para los campos espesor intima media
  $('.campoNumerico').keydown(function(e){
      if(e.keyCode == 8 || e.keyCode == 9 || e.keyCode ==46 || e.keyCode == 37 || e.keyCode == 39 
          || e.keyCode == 110 || e.keyCode == 190 || e.keyCode == 188 ){
        return true; //Solo permitimos: backspace, tab, delete, arrow left, arrow right,  punto (110,190) y coma
      }
      
      if(e.keyCode>=48 && e.keyCode<=57){//Numeros en la barra de teclas
        return true;
      }
      
      if(e.keyCode>=96 && e.keyCode<=106){//Numeros del numpad
        return true;
      }
      return false;
      
  }); 
  
  $('#espIntMedDer').focusout(
    function() {
        var valor = $('#espIntMedDer').val();
        valor = valor.replace(',','.'); 
        $('#espIntMedDer').val(valor);
        
        var expr = /^\d{1,2}$|^\d{1,2}\.\d{1,2}$/;
        if(expr.test(valor) == false){
          alert("Por favor, escriba un número válido.");
          $('#espIntMedDer').val('');
        }
   });
  
    $('#espIntMedIzq').focusout(
    function() {
        var valor = $('#espIntMedIzq').val();
        valor = valor.replace(',','.'); 
        $('#espIntMedIzq').val(valor);
        
        var expr = /^\d{1,2}$|^\d{1,2}\.\d{1,2}$/;
        if(expr.test(valor) == false){
          alert("Por favor, escriba un número válido.");
          $('#espIntMedIzq').val('');
        }
   });
  
});