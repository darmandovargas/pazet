
app.requires.push('checklist-model');
app.controller('SueloThiessenController', ['$scope','$q','$http','Suelo', function($scope, $q, $http, Suelo) {


    $scope.propMetalesPesados = [];
    $scope.nombre = null;
    $scope.poligono = null;
    $scope.radio = null;
    $scope.archivo = 'thiessen';
    $scope.buffer = 0;


    var map = L.map('mapa',{
        zoom: 10,
    }).setView([4.678822, -73.526278], 6);

    var ops = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        attribution: 'Corpoica', updateWhenIdle: true, reuseTiles: true
    }).addTo(map);

    var controlLoader = L.control.loader().addTo(map);
    L.Control.zoomHome({position: 'topleft'}).addTo(map);


    var promesaMultipleObjetos=$q.all({
        AllMuestras : Suelo.all_muestras_geojson(),
        AllPerfiles : Suelo.all_perfiles_geojson(),
        VarPropMetalesP : Suelo.variables_prop_metales_pesados_json()
    });

    controlLoader.show();
    promesaMultipleObjetos.then(function(promesas) {

        //----------------------------------------------- GEOJSON ESTACIONES -------------------------------------------

        geoJsonAllMuestras = L.geoJson(promesas.AllMuestras, {

            pointToLayer: function(feature, latlng) {
               return L.circleMarker(latlng, {
					radius: 5, fillColor: "#009C95", color: "#000", weight: 1, opacity: 1, fillOpacity: 0.8
				});
            }
        });
        //map.addLayer(geoJsonAllMuestras);

        geoJsonAllPerfiles = L.geoJson(promesas.AllPerfiles, {

            pointToLayer: function(feature, latlng) {
               return L.circleMarker(latlng, {
					radius: 5, fillColor: "#ff7800", color: "#000", weight: 1, opacity: 1, fillOpacity: 0.8
				});
            }
        });
        map.addLayer(geoJsonAllPerfiles);



        $scope.propMetalesPesados = promesas.VarPropMetalesP;


        controlLoader.hide();
    }, function(error) {
        controlLoader.hide();
        console.log(error);
    }, function(progreso) {
      console.log(progreso);
    });


    //-----------------------------------HERRAMIENTAS DE DIBUJO (DRAW)--------------------------------------------------
    var drawnItems = new L.FeatureGroup();
    map.addLayer(drawnItems);

    var drawControl = new L.Control.Draw({
        draw: {
            position: 'topleft',
            polygon: {
                title: 'Poligono de referencia',
                allowIntersection: false,
                drawError: {
                    color: '#D50000',
                    timeout: 1000,
                    message: '<strong>OOPS!<strong> Poligono incorrecto'
                },
                shapeOptions: {
                    color: '#1B5E20',
                    message: 'hola'
                },
                showArea: true
            },
            marker: false,
            circle: {
                shapeOptions: {
                    color: '#0D47A1'
                }
            },
            rectangle:{
                shapeOptions: {
                    color: '#E65100'
                }
            },
            polyline: false
        },
        edit: {
            featureGroup: drawnItems,
            edit: false
        }
    });
    var drawControlEditOnly = new L.Control.Draw({
        edit: {
            featureGroup: drawnItems,
            edit: false
        },
        draw: false
    });
    map.addControl(drawControl);

    //FUNCION QUE SE EJECUTA AL CREAR POLIGONO SOBRE EL MAPA (NECESARIA)
    map.on('draw:created', function (e) {
		var type = e.layerType,
		layer = e.layer;

		$scope.nombre = type;
		try{ $scope.radio = layer.getRadius(); } catch (e){}
		try{ $scope.poligono = layer.getLatLng(); } catch (e){ $scope.poligono = layer.getLatLngs(); }

        drawControl.removeFrom(map);
		drawnItems.addLayer(layer);
		drawControlEditOnly.addTo(map);

	});

	map.on("draw:deleted", function(e) {

	    $scope.nombre = null;
        $scope.poligono = null;
        $scope.radio = null;

        drawControlEditOnly.removeFrom(map);
        drawControl.addTo(map);
    });
    //------------------------------------------------------------------------------------------------------------------


    var btn_pefiles = new L.Control.Button(L.DomUtil.get('btn_pefiles'), { toggleButton: 'active' });
    btn_pefiles.addTo(map);

    var btn_muestras = new L.Control.Button(L.DomUtil.get('btn_muestras'), { toggleButton: 'active' });
    btn_muestras.addTo(map);

    btn_pefiles.on('click', function () {
         alertify.message('Capa de perfiles activada');
         map.removeLayer(geoJsonAllMuestras);
         map.addLayer(geoJsonAllPerfiles);
    });

    btn_muestras.on('click', function () {
        alertify.message('Capa de muestras activada');
        map.removeLayer(geoJsonAllPerfiles);
        map.addLayer(geoJsonAllMuestras);
    });





    $scope.pmetalSeleccionado = {};



    $scope.generarThiessen = function (){
        console.log($scope.pmetalSeleccionado);
        console.log($scope.nombre);
        console.log($scope.poligono);
        console.log($scope.radio);
        console.log($scope.archivo);
        console.log($scope.buffer);

        if($scope.nombre == null){
            alertify.warning('Aun no ha seleccionado un area a consultar');
            return false;
        };

        $http({
            method: 'POST',
            url: '/suelo/thiessen',
            params: {},
            cache: false
        }).then(function (success){
            //defered.resolve(success.data);
            //console.log(success.data);
        },function (error){
            //defered.reject(error)
        });

    };


}]);