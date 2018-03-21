
app.controller('AguaCauDayController', ['$scope','Estaciones', function($scope,Estaciones) {

	$scope.listEstaciones = [];
	$scope.listSeleccionados = [];

	var map = L.map('mapa_cauday',{

	}).setView([4.678822, -73.526278], 6);
	L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {attribution: 'Corpoica'}).addTo(map);

    var controlLoader = L.control.loader().addTo(map); //PLUGIN DE LOADING SOBRE EL MAPA


    /* ---------------- RENDERIZACIÓN DE LAS ESTACIONES CON DATOS CLIMATICOS MENSUALES SOBRE EL MAPA -----------------*/
	controlLoader.show();
	Estaciones.all_estn_caudal_diario_geojson().then(function(data) {

		var geoJsonLayer = L.geoJson(data, {
			pointToLayer: function(feature, latlng) {
				return L.circleMarker(latlng, {
					radius: 5,
					fillColor: "#2196F3",
					color: "#000",
					weight: 1,
					opacity: 1,
					fillOpacity: 0.8
				}).bindLabel(feature.properties.name, { direction: 'auto' });
			}
	    });

		map.addLayer(geoJsonLayer);
		map.addControl( new L.Control.Search({
			layer: geoJsonLayer,
			propertyName: 'name',
			position:'topright',
			initial: false,
			moveToLocation: function(latlng, title, map) { map.setView(latlng, 11); }
		}));

        controlLoader.hide();
	});

    /* ---------------------------------------------------------------------------------------------------------------*/

    /* ---------------------------------------------------------------------------------------------------------------*/
    /* ------------------------------ FUNCIONES DE SELECCION UTILIZANDO POLIGONOS ------------------------------------*/
    /* ---------------------------------------------------------------------------------------------------------------*/
	var drawnItems = new L.FeatureGroup();
	map.addLayer(drawnItems);

	var drawControl = new L.Control.Draw({
		draw: { marker: false, polyline: false },
		edit: {
			featureGroup: drawnItems,
			remove: true
		}
	});
	map.addControl(drawControl);

	map.on('draw:created', function (e) {
		var type = e.layerType,
		layer = e.layer;

		var radio = null;
		var nombre = null;

		if (type === 'rectangle' ) {
			puntos = layer.getLatLngs();
			nombre = 'rectangulo';
		}

		if (type === 'polygon' ) {
			puntos = layer.getLatLngs();
			nombre = 'polígono';
		}

		if (type === 'circle') {
			puntos = layer.getLatLng();
			radio = layer.getRadius();
			nombre = 'circulo';
		}

		drawnItems.addLayer(layer);

		alertify.confirm('Consultar área', 'Se consultaran las estaciones presentes en el '+nombre+' trazado', function(){
		     filtro(puntos, radio, type);
		}, function(){
            map.removeLayer(layer);
		});


	});

	map.on('draw:edited', function (e) {
		var layers = e.layers;
		layers.eachLayer(function (layer) {

			var radio = null;
			var nombre = null;
			var type = null;

			if (layer instanceof L.Circle) {
				puntos = layer.getLatLng();
				radio = layer.getRadius();
				nombre = 'circulo';
				type = 'circle';
			}

			if ((layer instanceof L.Polygon) && ! (layer instanceof L.Rectangle)) {
				puntos = layer.getLatLngs();
				nombre = 'polígono';
				type = 'polygon';
			}

			if (layer instanceof L.Rectangle) {
				puntos = layer.getLatLngs();
				nombre = 'rectangulo';
				type = 'rectangle';
			}

			drawnItems.addLayer(layer);


			alertify.confirm('Consultar área', 'Se consultara las estaciones presentes en el '+nombre+' trazado', function(){
		        filtro(puntos, radio, type);
            }, function(){
                map.removeLayer(layer);
            });


		});
	});

	//ESTE METODO FILTRA LAS ESTACIONES SEGUN LA GEOMETRIA DIBUJADA EN EL FILTRO DE AREA
    function filtro(data, radio, type){

    	$('#filter').toggleClass('loading');
    	alertify.notify('Consultando estaciones espere...', 'custom', 2, function(){ });

    	Estaciones.filtro_estn_in_poligon_cauday_json(type,data,radio).then(function(data) {

    	    if (data.length <= 0){
                alertify.warning('Su consulta no arrojo información!');
                $('#filter').toggleClass('loading');
            }else{
                $scope.listEstaciones = data;
                $('html,body').animate({ scrollTop: $("#resultado").offset().top }, 2000);
                $('#filter').toggleClass('loading');
            }

    	}).catch(function(err) {
            console.log(err);
            $( "#filter" ).toggleClass('loading');
            alertify.error('OOPS! Error consultando información!');
        });

    };
    /* ---------------------------------------------------------------------------------------------------------------*/

	//FILTRO DE ESTACIONES POR DEPARTAMENTOS Y CLIMA MENSUAL
	$scope.searchWithDepto = function(){

        $('#filter').toggleClass('loading');
	    var codane = $('#departamento_id').find(":selected").val();

		if( codane == null || codane == '' ) {

		    alertify.alert('OOPS! Departamento no seleccionado',
            'No ha seleccionado ningun departamento, para continuar por favor seleccione uno!');
            $('#filter').toggleClass('loading');

		}else{

            alertify.notify('Consultando estaciones espere...', 'custom', 2, function(){ });
			$('#filter').addClass('loading');
			$scope.listEstaciones = null;

			Estaciones.estn_caudal_day_depto_json(codane).then(function(data) {

                if (data.length <= 0){
                    alertify.warning('Su consulta no arrojo información!');
                    $('#filter').toggleClass('loading');
                }else{
                    $scope.listEstaciones = data;
                    $('html,body').animate({ scrollTop: $("#resultado").offset().top }, 2000);
                    $('#filter').toggleClass('loading');
                }

            }).catch(function(err) {
                alertify.error('OOPS! Error consultando información!');
                $('#filter').toggleClass('loading');
            });

		}

	};

	//FILTRO DE ESTACIONES POR MUNICIPIO Y CLIMA MENSUAL
	$scope.searchWithMun = function(){

	    $('#filter').toggleClass('loading');
	    var munid = $('#municipio_id').find(":selected").val();

		if( munid == null || munid == '' ) {

			alertify.alert('OOPS! Municipio no seleccionado',
            'No ha seleccionado ningun municipio, para continuar por favor seleccione uno!');
            $('#filter').toggleClass('loading');

		}else{

            alertify.notify('Consultando estaciones espere...', 'custom', 2, function(){ });
			$('#filter').addClass('loading');
			$scope.listEstaciones = null;

			Estaciones.estn_caudal_day_mun_json(munid).then(function(data) {

                if (data.length <= 0){
                    alertify.warning('Su consulta no arrojo información!');
                    $('#filter').toggleClass('loading');
                }else{
                    $scope.listEstaciones = data;
                    $('html,body').animate({ scrollTop: $("#resultado").offset().top }, 2000);
                    $('#filter').toggleClass('loading');
                }

            }).catch(function(err) {
                alertify.error('OOPS! Error consultando información!');
                $('#filter').toggleClass('loading');
            });

		}

	};

	//FILTRO DE ESTACIONES POR CODIGO DE ESTACION Y CLIMA MENSUAL
	$scope.searchWithCodigo = function(){

	    $('#filter').toggleClass('loading');
	    var codigo = $('#est_codigo').val();

		if( codigo == null || codigo == '' ) {

			alertify.alert('OOPS! Código de estación no digitado',
            'No ha digitado ningún código de estación, para continuar por favor digite un código de estación valido!');
            $('#filter').toggleClass('loading');

		}else{

            alertify.notify('Consultando estaciones espere...', 'custom', 2, function(){ });
			$('#filter').addClass('loading');
			$scope.listEstaciones = null;

			Estaciones.estn_codigo_caudal_day_json(codigo).then(function(data) {

                if (data.length <= 0){
                    alertify.warning('Su consulta no arrojo información!');
                    $('#filter').toggleClass('loading');
                }else{
                    $scope.listEstaciones = data;
                    $('html,body').animate({ scrollTop: $("#resultado").offset().top }, 2000);
                    $('#filter').toggleClass('loading');
                }

            }).catch(function(err) {
                alertify.error('OOPS! Error consultando información!');
                $('#filter').toggleClass('loading');
            });
		}

	};

	//FILTRO DE ESTACIONES POR NOMBRE Y CLIMA MENSUAL
	$scope.searchWithName = function(){

		$('#filter').toggleClass('loading');
	    var nombre = $('#est_nombre').val();

		if( nombre == null || nombre == '' ) {

			alertify.alert('OOPS! Nombre de estación no digitado',
            'No ha digitado ningún nombre de estación, para continuar por favor digite el nombre de una estación!');
            $('#filter').toggleClass('loading');

		}else{

            alertify.notify('Consultando estaciones espere...', 'custom', 2, function(){ });
			$('#filter').addClass('loading');
			$scope.listEstaciones = null;

			Estaciones.estn_name_caudal_day_json(nombre).then(function(data) {

                if (data.length <= 0){
                    alertify.warning('Su consulta no arrojo información!');
                    $('#filter').toggleClass('loading');
                }else{
                    $scope.listEstaciones = data;
                    $('html,body').animate({ scrollTop: $("#resultado").offset().top }, 2000);
                    $('#filter').toggleClass('loading');
                }

            }).catch(function(err) {
                alertify.error('OOPS! Error consultando información!');
                $('#filter').toggleClass('loading');
            });

		}

	};
    /* ---------------------------------------------------------------------------------------------------------------*/
    /* ---------------------------------------------------------------------------------------------------------------*/


    /* ---------------------------------------------------------------------------------------------------------------*/
    /* -----------------------FUNCIONES DE SELECCION, REMOCION DE ESTACIONES FILTRADAS -------------------------------*/
    /* ---------------------------------------------------------------------------------------------------------------*/
    //ESTE METODO AGREGA UNA ESTACION AL LISTADO DE ESTACIONES SELECCIONADAS
	$scope.addEstacion = function(estacion){
		$scope.listSeleccionados.push(estacion);
		var index = $scope.listEstaciones.indexOf(estacion);
		$scope.listEstaciones.splice(index, 1);
	};

	//ESTE METODO DEVUELVE UNA ESTACION SELECCIONADA AL LISTADO GENERAL DE ESTACIONES FILTRADAS
	$scope.delEstacion = function(etcn){
		$scope.listEstaciones.push(etcn);
		var index = $scope.listSeleccionados.indexOf(etcn);
		$scope.listSeleccionados.splice(index, 1);
	};

	//ESTE METODO CONVIERTE EN SELECCIONADAS TODAS LAS ESTACIONES ANTERIORMENTE FILTRADAS
	$scope.allEstacion = function(){
		$scope.listSeleccionados = $scope.listEstaciones;
		$scope.listEstaciones = [];
	};
	/* ---------------------------------------------------------------------------------------------------------------*/

}]);