app.controller('HistoryMetController', ['$scope','Estaciones','Clima', function($scope,Estaciones,Clima) {


    //SE CONSULTA LA INFORMACION DE LA ESTACION Y SE CONSTRUYE EL MAPA DE UBICACION
	Estaciones.estacion_get_with_codigo($('#codigo').val()).then(function(data) {

		$scope.estacion = data;

		//CREANDO EL MAPA DE UBICACIÓN DE LA ESTACIÓN
		var map = L.map('mapa',{
			zoomControl: false,
			scrollWheelZoom: false
		}).setView([$scope.estacion.estn_lat, $scope.estacion.estn_lng], 12);
		L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {attribution: 'Corpoica'}).addTo(map);

		//CREAMOS UN ICONO Y UBICAMOS UN MARCADOR EN EL LUGAR DE REFERENCIA DE LA ESTACION
		var pulsingIcon = L.icon.pulse({iconSize:[20,20],color:'blue'});
		L.marker([$scope.estacion.estn_lat, $scope.estacion.estn_lng], {icon:pulsingIcon}).addTo(map);

		 $scope.consultarDatos();

	}).catch(function(err) {
        $('#graficos').toggleClass('loading');
        alertify.error('OOPS! Error consultando información!');
    });



	// *****************************************************************************************************************
	// ******************************************** MANEJO DE FECHAS ***************************************************
	// *****************************************************************************************************************

	//FECHAS ACTUALES CON MOMENTJS
	var m = moment();
	$scope.currentYear = m.year(); //AÑO ACTUAL EJ 2017

	//LISTA DE AÑOS DESDE 1900 AL AÑO ACTUAL
	$scope.listYear = [];
	for (i = new Date().getFullYear(); i >= 1900; i--){ $scope.listYear.push(i); }

	// *****************************************************************************************************************

	// *****************************************************************************************************************
	// ******************************************** VALORES INCIALES ***************************************************
	// *****************************************************************************************************************

	$scope.yearini = $scope.currentYear;
	$scope.escala ='mensual';

	// *****************************************************************************************************************



    // *****************************************************************************************************************
	// ********************************* FUNCION PARA CONSULTA Y CARGA DE DATOS ****************************************
	// *****************************************************************************************************************
    $scope.consultarDatos = function() {

        var codigo = $scope.estacion.estn_codigo;
		var anioini = $scope.yearini;

        alertify.notify('Generando gráfico por favor espere...', 'custom', 2, function(){ });
        $('#graficos').toggleClass('loading');

        if ($scope.escala=='mensual') {

			Clima.clima_month_estn_year_json(codigo,anioini).then(function(data) {

                 $scope.dataGrap= [];
                 $scope.dataGrap = data;

                 // ******************************************** GRAFICO DE PRECIPITACION
                 optionsPpt['series'][0].data = [];
                 optionsPpt['xAxis']['categories'] = [];
                 optionsPpt['xAxis'].tickInterval = 0;
                 optionsPpt['title']['text'] = '';

                 optionsPpt['title']['text'] = 'Grafica precipitación, Año: '+anioini+', Estación: '+codigo+ ', Escala: '+$scope.escala;
                 optionsPpt['series'][0].data = $scope.dataGrap.ppt;
                 optionsPpt['xAxis']['categories'] = $scope.dataGrap.fecha;
                 Highcharts.chart('graph_ppt', optionsPpt);


                 // ******************************************** GRAFICO DE TEMPERATURA MAXIMA, MINIMA Y MEDIA
                 optionsTemp['series'][0].data = [];
                 optionsTemp['xAxis']['categories'] = [];
                 optionsTemp['xAxis'].tickInterval = 0;
                 optionsTemp['title']['text'] = '';

                 optionsTemp['xAxis']['categories'] = $scope.dataGrap.fecha;
                 optionsTemp['title']['text'] = 'Grafica precipitación, Año: '+anioini+', Estación: '+codigo+ ', Escala: '+$scope.escala;
                 optionsTemp['series'][0].data = $scope.dataGrap.temp_med;
                 optionsTemp['series'][1].data = $scope.dataGrap.temp_max;
                 optionsTemp['series'][2].data = $scope.dataGrap.temp_min;
                 Highcharts.chart('graph_temp', optionsTemp);


                 // ******************************************** GRAFICO DE HUMEDAD
                 optionsHum['series'][0].data = [];
                 optionsHum['xAxis']['categories'] = [];
                 optionsHum['xAxis'].tickInterval = 0;
                 optionsHum['title']['text'] = '';

                 optionsHum['xAxis']['categories'] = $scope.dataGrap.fecha;
                 optionsHum['title']['text'] = 'Grafica humedad, Año: '+anioini+', Estación: '+codigo+ ', Escala: '+$scope.escala;
                 optionsHum['series'][0].data = $scope.dataGrap.hum;
                 Highcharts.chart('graph_hum', optionsHum);


                 // ******************************************** GRAFICO DE BRILLO SOLAR
                 optionsBs['series'][0].data = [];
                 optionsBs['xAxis']['categories'] = [];
                 optionsBs['xAxis'].tickInterval = 0;
                 optionsBs['title']['text'] = '';

                 optionsBs['xAxis']['categories'] = $scope.dataGrap.fecha;
                 optionsBs['title']['text'] = 'Grafica brillo solar, Año: '+anioini+', Estación: '+codigo+ ', Escala: '+$scope.escala;
                 optionsBs['series'][0].data = $scope.dataGrap.hum;
                 Highcharts.chart('graph_bs', optionsBs);


                 $('#graficos').toggleClass('loading');

			}).catch(function(err) {
                $('#graficos').toggleClass('loading');
                alertify.error('OOPS! Error consultando información!');
            });

		}else if ($scope.escala=='diaria') {

		    Clima.clima_day_estn_year_json(codigo,anioini).then(function(data) {

                 $scope.dataGrap= [];
                 $scope.dataGrap = data;

                 // ******************************************** GRAFICO DE PRECIPITACION
                 optionsPpt['series'][0].data = [];
                 optionsPpt['xAxis']['categories'] = [];
                 optionsPpt['title']['text'] = '';
                 optionsPpt['xAxis'].tickInterval = 15;

                 optionsPpt['title']['text'] = 'Grafica precipitación, Año: '+anioini+', Estación: '+codigo+ ', Escala: '+$scope.escala;
                 optionsPpt['series'][0].data = $scope.dataGrap.ppt;
                 optionsPpt['xAxis']['categories'] = $scope.dataGrap.fecha;
                 Highcharts.chart('graph_ppt', optionsPpt);


                 // ******************************************** GRAFICO DE TEMPERATURA MAXIMA, MINIMA Y MEDIA
                 optionsTemp['series'][0].data = [];
                 optionsTemp['xAxis']['categories'] = [];
                 optionsTemp['xAxis'].tickInterval = 15;
                 optionsTemp['title']['text'] = '';

                 optionsTemp['xAxis']['categories'] = $scope.dataGrap.fecha;
                 optionsTemp['title']['text'] = 'Grafica temperatura, Año: '+anioini+', Estación: '+codigo+ ', Escala: '+$scope.escala;
                 optionsTemp['series'][0].data = $scope.dataGrap.temp_med;
                 optionsTemp['series'][1].data = $scope.dataGrap.temp_max;
                 optionsTemp['series'][2].data = $scope.dataGrap.temp_min;
                 Highcharts.chart('graph_temp', optionsTemp);


                 // ******************************************** GRAFICO DE HUMEDAD
                 optionsHum['series'][0].data = [];
                 optionsHum['xAxis']['categories'] = [];
                 optionsHum['xAxis'].tickInterval = 15;
                 optionsHum['title']['text'] = '';

                 optionsHum['xAxis']['categories'] = $scope.dataGrap.fecha;
                 optionsHum['title']['text'] = 'Grafica humedad, Año: '+anioini+', Estación: '+codigo+ ', Escala: '+$scope.escala;
                 optionsHum['series'][0].data = $scope.dataGrap.hum;
                 Highcharts.chart('graph_hum', optionsHum);

                 // ******************************************** GRAFICO DE BRILLO SOLAR
                 optionsBs['series'][0].data = [];
                 optionsBs['xAxis']['categories'] = [];
                 optionsBs['xAxis'].tickInterval = 15;
                 optionsBs['title']['text'] = '';

                 optionsBs['xAxis']['categories'] = $scope.dataGrap.fecha;
                 optionsBs['title']['text'] = 'Grafica brillo solar, Año: '+anioini+', Estación: '+codigo+ ', Escala: '+$scope.escala;
                 optionsBs['series'][0].data = $scope.dataGrap.bs;
                 Highcharts.chart('graph_bs', optionsBs);

                 $('#graficos').toggleClass('loading');

			}).catch(function(err) {
                //console.log(err);
                $('#graficos').toggleClass('loading');
                alertify.error('OOPS! Error consultando información!');
            });

		}

    };
    // *****************************************************************************************************************



}]);