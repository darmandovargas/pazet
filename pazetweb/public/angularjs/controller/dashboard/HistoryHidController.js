app.controller('HistoryHidController', ['$scope','Estaciones','Agua', function($scope,Estaciones,Agua) {


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
		 $scope.graficarCDC();

	}).catch(function(err) {
        $('#graficos').toggleClass('loading');
        alertify.error('OOPS! Error consultando información de la estación!');
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
	$scope.escala ='diaria';
	// *****************************************************************************************************************


    // *****************************************************************************************************************
	// ********************************* FUNCION PARA CONSULTA Y CARGA DE DATOS ****************************************
	// *****************************************************************************************************************
    $scope.consultarDatos = function() {

        var codigo = $scope.estacion.estn_codigo;
		var anioini = $scope.yearini;

        alertify.notify('Generando gráfico por favor espere...', 'custom', 2, function(){ });
        $('#graficos').toggleClass('loading');

		Agua.caudal_day_estn_year_json(codigo,anioini).then(function(data) {

            $scope.dataGrap= [];
            $scope.dataGrap = data;

            // ******************************************** GRAFICO DE PRECIPITACION
            optionsCaudal['series'][0].data = [];
            optionsCaudal['xAxis']['categories'] = [];
            optionsCaudal['xAxis'].tickInterval = 15;
            optionsCaudal['title']['text'] = '';

            optionsCaudal['title']['text'] = 'Grafica caudal, Estación: '+codigo+', Año: '+anioini+ ', Escala: '+$scope.escala;
            optionsCaudal['series'][0].data = $scope.dataGrap.caudal;
            optionsCaudal['xAxis']['categories'] = $scope.dataGrap.fecha;
            Highcharts.chart('graph_caudal', optionsCaudal);

            $('#graficos').toggleClass('loading');

		}).catch(function(err) {
		    console.log(err);
            $('#graficos').toggleClass('loading');
            alertify.error('OOPS! Error consultando información de caudales!');
        });


    };
    // *****************************************************************************************************************



    // *****************************************************************************************************************
	// ********************************* CURVA DE DURACIÓN DE CAUDAL ****************************************
	// *****************************************************************************************************************
    $scope.graficarCDC = function() {

        var codigo = $scope.estacion.estn_codigo;

        $('#cdc').toggleClass('loading');

		Agua.cdc_diaria_estn_json(codigo).then(function(data) {

            $scope.dataCdc= [];
            $scope.dataCdc = data;

            // ******************************************** GRAFICO DE PRECIPITACION
            optionsCdc['series'][0].data = [];
            optionsCdc['xAxis']['categories'] = [];
            optionsCdc['title']['text'] = '';

            optionsCdc['title']['text'] = 'Grafica curva duración caudal, Estación: '+codigo;
            optionsCdc['series'][0].data = $scope.dataCdc.caudales;
            optionsCdc['xAxis']['categories'] = $scope.dataCdc.duracion;
            Highcharts.chart('graph_cdc', optionsCdc);

            $('#cdc').toggleClass('loading');

		}).catch(function(err) {
            $('#cdc').toggleClass('loading');
            alertify.error('OOPS! Error generando curva duración caudal!');
        });


    };
    // *****************************************************************************************************************




}]);