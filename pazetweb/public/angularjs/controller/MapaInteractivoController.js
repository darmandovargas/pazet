$("#map").height($(window).height()-50).width($(window).width());

app.controller('MapaInteractivoController', ['$scope','$q','Estaciones','Suelo', '$location', '$timeout', function($scope, $q, Estaciones, Suelo, $location, $timeout) {
    //console.log($location.absUrl().split('/')[5]=="voronoi");

    d3.json('../../suelo/all_muestras_geojson', function(geojson){
        console.log("After");
        mapDraw(geojson);
    });

    function mapDraw(geojson){

        /* --------------------------------CONFIGURACION BASICA PARA EL MAPA DE ESTACIONES -------------------------------*/
        /*var map = L.map('map',{
            zoom: 10,
            crs: L.CRS.EPSG4326,
            maxZoom: 25,
            zoomControl: false,
            fullscreenControl: true,
            fullscreenControlOptions: { position: 'topleft' }
        }).setView([4.678822, -73.526278], 6);
*/


        var pointdata = geojson.features;

        //leaflet初期設定
        var map = L.map('map',{
            zoom: 10,
            crs: L.CRS.EPSG4326,
            maxZoom: 25,
            zoomControl: true,
            fullscreenControl: true,
            fullscreenControlOptions: { position: 'topleft' }
        }).setView([4.678822, -73.526278], 6);
        //var map = L.map('map');
        //map.setView([36.3894816, 139.0634281], 14);

        if($location.absUrl().split('/')[5]=="voronoi"){

            map.on("viewreset moveend", update);

            var mapLink = '<a href="http://openstreetmap.org">OpenStreetMap</a>';

            L.tileLayer(
                'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
                {
                    attribution: 'Map data &copy; ' + mapLink,
                    maxZoom: 18
                }
            ).addTo(map);


            // オーバーレイレイヤ追加
            map._initPathRoot();
            var svg = d3.select("#map").select("svg");
            var g = svg.append("g").attr("class", "leaflet-zoom-hide");


            //ボロノイジェネレーター
            var voronoi = d3.geom.voronoi()
                .x(function(d) { return d.x; })
                .y(function(d) { return d.y; });



            update();
            map.setView({lat: 8.23593, lng: -72.469341}, 11, {animation: true});
        }

        function update() {

            //ピクセルポジション情報保存用
            var positions = [];

            //位置情報→ピクセルポジション変換
            pointdata.forEach(function(d) {
                var latlng = new L.LatLng(d.geometry.coordinates[1], d.geometry.coordinates[0]);
                positions.push({
                    x :map.latLngToLayerPoint(latlng).x,
                    y :map.latLngToLayerPoint(latlng).y
                });
            });


            //前サークルを削除
            d3.selectAll('.AEDpoint').remove();
            //サークル要素を追加
            var circle = g.selectAll("circle")
                .data(positions)
                .enter()
                .append("circle")
                .attr("class", "AEDpoint")
                .attr({
                    "cx":function(d, i) { return d.x; },
                    "cy":function(d, i) { return d.y; },
                    "r":2,
                    fill:"brown"
                });

            //ボロノイ変換関数
            var polygons = voronoi(positions);
            polygons.forEach(function(v) { v.cell = v; });

            //前ボロノイPathを削除
            svg.selectAll(".volonoi").remove();
            //path要素を追加
            svg.selectAll("path")
                .data(polygons)
                .enter()
                .append("svg:path")
                .attr("class", "volonoi")
                .attr({
                    "d": function(d) {
                    if(!d) return null;
                        return "M" + d.cell.join("L") + "Z";
                    },
                    stroke:"black",
                    fill:"none"
                });
            //$('.volonoi').toggle();
            //$('.AEDpoint').toggle();

        }




         //SE CENTRA LA ESTACION EN EL MAPA

        L.Control.zoomHome({position: 'topleft'}).addTo(map); //BOTON HOME DE RESET
        L.control.scale({metric:true}).addTo(map); //PARA MOSTRAR UNA ESCALA EN EL MAPA
        L.Control.measureControl({title:'Medir distancias'}).addTo(map); //FUNCIONA COMO REGLA PARA MEDIR DISTANCIAS
        var controlLoader = L.control.loader().addTo(map); //PLUGIN DE LOADING SOBRE EL MAPA

        var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
        var osm2 = new L.TileLayer(osmUrl, {minZoom: 0, maxZoom: 13, attribution: 'Minimap'});
        var miniMap = new L.Control.MiniMap(osm2, {position:'bottomleft'}).addTo(map);

        /* ------------------------------------------------- ICONOS ------------------------------------------------------*/
        //TIPOS DE ICONOS PARA LOS MARCADORES
        var icon_meteorologica = L.icon({iconUrl: '/public/images/iconos_mapa/icon_meteorologica.png', iconSize: [50, 50] });
        //var icon_hidroclimatica = L.icon({iconUrl: '/public/images/mapainteractivo/icon_hidroclimatica.png', iconSize: [50, 50] });
        var icon_hidrologica = L.icon({iconUrl: '/public/images/iconos_mapa/icon_hidrologica.png', iconSize: [50, 50] });
        //var icon_incognito = L.icon({iconUrl: '/public/images/mapainteractivo/icon_incognito.png', iconSize: [50, 50] });
        //var icon_waypoint = L.icon({iconUrl: '/public/images/mapainteractivo/flag_waypoin.png', iconSize: [50, 50] });
        var icon_suelo = L.icon({iconUrl: '/public/images/iconos_mapa/icon_suelo.png', iconSize: [50, 50] });
        var icon_muestra = L.icon({iconUrl: '/public/images/iconos_mapa/icon_muestra.png', iconSize: [50, 50] });


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
                polyline: {
                    shapeOptions: {
                        color: '#000000'
                    }
                }
            },
            edit: {
                featureGroup: drawnItems
            }
        });
        map.addControl(drawControl);

        //FUNCION QUE SE EJECUTA AL UTILIZAR LAS HERRAMIENTAS DE POLIGONO SOBRE EL MAPA (NECESARIA)
        map.on('draw:created', function (e) {
            var type = e.layerType,
            layer = e.layer;
            if (type === 'marker') {
                layer.bindPopup('Marcador de referencia!');
            }
            drawnItems.addLayer(layer);
        });
        //------------------------------------------------------------------------------------------------------------------

        //--------------------------------------HERRAMIENTAS DE GPS-----------------------------------------------------
        L.Control.FileLayerLoad.LABEL = '<i class="fa fa-folder-open"></i>';
        var controla = L.Control.fileLayerLoad({
            fitBounds: true,
            layerOptions: {
                style: {color:'red', opacity: 1.0, fillOpacity: 1.0, weight: 0.5, clickable: false},
                pointToLayer: function (data, latlng) {
                    return L.marker(latlng, {icon: icon_waypoint});
                }
            },
        }).addTo(map);

        controla.loader.on('data:loaded', function (e) { controlLoader.hide(); });

        controla.loader.on('data:loading', function(e){ controlLoader.show(); });

        controla.loader.on('data:error', function(e){ controlLoader.hide(); alert(e.error+": "+e.message) });
        //--------------------------------------------------------------------------------------------------------------


        /* ------------------------------------------- DESPLIEGUE DE INFORMACIÓN -----------------------------------------*/

        var promesaMultipleObjetos=$q.all({
            AllEstaciones : Estaciones.all_stations_geojson(),
            AllPerfiles: Suelo.all_perfiles_geojson(),
            AllMuestras: Suelo.all_muestras_geojson(),
            MuestrasSuelosElZulia: Suelo.all_muestras_geojson()
        });

        controlLoader.show(); //ANIMACION LOADING SOBRE EL MAPA
        promesaMultipleObjetos.then(function(promesas) {


            //----------------------------------------------- GEOJSON ESTACIONES -------------------------------------------
            var geoJsonLayerEstn = null;
            var markersEstn = L.markerClusterGroup();
            geoJsonLayerEstn = L.geoJson(promesas.AllEstaciones, {
                pointToLayer: function(feature, latlng) {
                    var icono = null;
                    switch(feature.properties.clase) {
                        case "HID": icono = icon_hidrologica; break;
                        case "MET": icono = icon_meteorologica; break;
                        case "HMT": icono = icon_hidroclimatica; break;
                        default: icono = icon_incognito;
                    }
                    var marcador = L.marker(latlng, {icon: icono, title: feature.properties.name})
                    .bindLabel(feature.properties.name, { direction: 'auto' }).on('click', onClickMarkerEstn);
                    marcador.myCustomID = feature.properties.codigo;
                    return marcador;
                },
                onEachFeature: function (feature, layer) {
                   //layer.bindPopup(feature.properties.name);
                }
            });
            markersEstn.addLayer(geoJsonLayerEstn);
            //map.addLayer(markers);
            //--------------------------------------------------------------------------------------------------------------


            //-------------------------------------------------MUESTRAS-----------------------------------------------------
            var markersMues = L.markerClusterGroup();
            var geoJsonLayerMuestras  = L.geoJson(promesas.AllMuestras, {
                pointToLayer: function(feature, latlng) {

                    var marcador = L.marker(latlng, {icon: icon_muestra, title: feature.properties.muesid})
                    .on('click', onClickMarkerMuestra);
                    marcador.myCustomID = feature.properties.muesid;
                    return marcador;
                }
            });
            markersMues.addLayer(geoJsonLayerMuestras);
            //--------------------------------------------------------------------------------------------------------------

            //-------------------------------------------------POLÍGONO DE THIESSEN-----------------------------------------------------
            var markersPoligonoThiessen = L.markerClusterGroup();
            var geoJsonLayerPoligonoThiessen  = L.geoJson(promesas.MuestrasSuelosElZulia, {
                pointToLayer: function(feature, latlng) {
                    //console.log(latlng);
                    var marcador = L.marker(latlng, {icon: icon_muestra, title: feature.properties.muesid})
                    .on('click', onClickMarkerVoronoiPolygon);
                    marcador.myCustomID = feature.properties.muesid;
                    return marcador;
                }
            });
            markersPoligonoThiessen.addLayer(geoJsonLayerPoligonoThiessen);


            //--------------------------------------------------------------------------------------------------------------


            //--------------------------------------- GEOJSON PERFILES DE SUELO --------------------------------------------
            var markersPerfiles = L.markerClusterGroup();
            var geoJsonPerfiles = L.geoJson(promesas.AllPerfiles, {
                pointToLayer: function(feature, latlng) {
                    var marcador = L.marker(latlng, {icon: icon_suelo, title: feature.properties.codigo})
                    .bindLabel(feature.properties.estudio +" ("+feature.properties.pub+")", { direction: 'auto' })
                    .on('click',  onClickMarkerSuelo);
                    marcador.myCustomID = feature.properties.codigo;
                    return marcador;
                }
            });
            markersPerfiles.addLayer(geoJsonPerfiles);
            //map.addLayer(markers);
            //--------------------------------------------------------------------------------------------------------------




            //---------------------------------------------BUSCADOR DE ESTACIONES-------------------------------------------
            var buscador = new L.Control.Search({
                layer: markersEstn,
                position:'topleft',
                initial: false,
                text:'Buscar',
                /*buildTip: function(text, val) {
                    //console.log(val);
                    var codigo = val.layer.feature.properties.codigo;
                    return '<a class="ui mini label"><i class="marker icon"></i>'+text+'</a>';

                },*/
                moveToLocation: function(latlng, title, map) { map.setView(latlng, 15); }
            });
            map.addControl(buscador);
            //--------------------------------------------------------------------------------------------------------------




            // ------------------------------------------------- CAPAS (layers) --------------------------------------------
            var ops = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="http://osm.org/copyright" target="_blank">OpenStreetMap</a> <a href="http://www.corpoica.org.co/" target="_blank">© Corpoica</a>',
                updateWhenIdle: true,
                reuseTiles: true
            });
            var roadmap = new L.Google('ROADMAP'); //MAPAS DE GOOGLE
            var satellite = new L.Google('SATELLITE'); //MAPAS DE GOOGLE
            var hybrid = new L.Google('HYBRID '); //MAPAS DE GOOGLE
            var terrain = new L.Google('TERRAIN'); //MAPAS DE GOOGLE

            var esri_img = L.tileLayer.provider('Esri.WorldImagery');


            //SATELLITE GOES
            var imageUrl = 'http://api.wunderground.com/api/931d8915c8957f89/satellite/image.png?maxlat=12.650418&maxlon=-68.12544&minlat=-3.712216&minlon=-81.22655&width=640&height=480&key=sat_ir4_bottom>t=107&timelabel=1&timelabel.x=470&timelabel.y=41&proj=me',
            imageBounds = [[-3.712216, -81.22655], [12.650418, -68.12544]];
            var goes = L.imageOverlay(imageUrl, imageBounds);

            var divisionPolitica = L.tileLayer.wms('http://localhost:8080/geoserver/PAZET/wms?', {
                layers: 'PAZET:division_politica',
                transparent: true,
                opacity:0.7,
                format: 'image/png',
                updateWhenIdle: true,
                reuseTiles: true,
                attribution: '© Corpoica'
            });

            var divisionRegional = L.tileLayer.wms('http://localhost:8080/geoserver/PAZET/wms?', {
                layers: 'PAZET:division_regional',
                transparent: true,
                opacity:0.7,
                format: 'image/png',
                updateWhenIdle: true,
                reuseTiles: true,
                attribution: '© Corpoica'
            });

            var limiteAzosulia= L.tileLayer.wms('http://localhost:8080/geoserver/PAZET/wms?', {
                layers: 'PAZET:limites_azosulia',
                transparent: true,
                opacity:0.7,
                format: 'image/png',
                updateWhenIdle: true,
                reuseTiles: true,
                attribution: '© Corpoica'
            });

            var catalogo_estaciones = L.tileLayer.wms('http://localhost:8080/geoserver/PAZET/wms?', {
                layers: 'PAZET:all_estaciones',
                transparent: true,
                opacity:0.7,
                format: 'image/png',
                updateWhenIdle: true,
                reuseTiles: true,
                attribution: '© Corpoica'
            });

            var catalogo_perfiles = L.tileLayer.wms('http://localhost:8080/geoserver/PAZET/wms?', {
                layers: 'PAZET:all_perfiles',
                transparent: true,
                opacity:0.7,
                format: 'image/png',
                updateWhenIdle: true,
                reuseTiles: true,
                attribution: '© Corpoica'
            });

            var catalogo_muestras = L.tileLayer.wms('http://localhost:8080/geoserver/PAZET/wms?', {
                layers: 'PAZET:all_muestras',
                transparent: true,
                opacity:0.7,
                format: 'image/png',
                updateWhenIdle: true,
                reuseTiles: true,
                attribution: '© Corpoica'
            });

            L.control.panelLayers(
                [
                    {
                        group: "OSM Mapas",
                        collapsed: false,
                        layers: [
                            {
                                name: "Open Street Map",
                                active:true,
                                layer: ops
                            },{
                                name: "Esri",
                                active:false,
                                layer: esri_img
                            }
                        ]
                    },
                    {
                        group: "Google Mapas",
                        collapsed: false,
                        layers: [
                            {
                                name: "Satellite",
                                layer: satellite
                            },{
                                name: "RoadMap",
                                layer: roadmap
                            },{
                                name: "Terrain",
                                layer: terrain
                            },{
                                name: "Hybrid",
                                layer: hybrid
                            }
                        ]
                    }
                ],
                [
                    {
                        group: "Marcadores de consulta",
                        collapsed: false,
                        layers: [
                            {
                                name: 'Estaciones',
                                icon: '<i class="map pin icon orange"></i>',
                                layer: markersEstn
                            },{
                                name: 'Perfiles de suelo',
                                icon: '<i class="braille icon brown"></i>',
                                layer: markersPerfiles
                            },{
                                name: 'Muestras de suelo',
                                icon: '<i class="braille icon brown"></i>',
                                layer: markersMues
                            }/*,{
                                name: 'Polygono de Voronoi',
                                icon: '<i class="braille icon brown"></i>',
                                layer: markersPoligonoThiessen
                            }*/
                        ]
                    },
                    {
                        group: "Servicios WMS",
                        collapsed: false,
                        layers: [
                            {
                                name: 'División politica',
                                icon: '<i class="map outline blue icon"></i>',
                                layer: divisionPolitica
                            },{
                                name: 'División Regional',
                                icon: '<i class="map outline blue icon"></i>',
                                layer: divisionRegional
                            },{
                                name: 'Asozulia',
                                icon: '<i class="map outline blue icon"></i>',
                                layer: limiteAzosulia
                            },{
                                name: 'Catalogo estaciones',
                                icon: '<i class="fa fa-object-group"></i>',
                                layer: catalogo_estaciones
                            },{
                                name: 'Catalogo perfiles (Suelo)',
                                icon: '<i class="fa fa-object-group"></i>',
                                layer: catalogo_perfiles
                            },{
                                name: 'Catalogo muestras (Suelo)',
                                icon: '<i class="fa fa-object-group"></i>',
                                layer: catalogo_muestras
                            }
                        ]
                    },
                    {
                        group: "Satelites",
                        collapsed: false,
                        layers: [
                            {
                                name: 'Satelite Goes (Canal infrarrojo)',
                                icon:'<i class="rss icon"></i>',
                                layer: goes
                            }
                        ]
                    }
                ], {collapsibleGroups: true}).addTo(map);



            controlLoader.hide();
        }, function(error) {
            controlLoader.hide();
            console.log('Error');

        }, function(progreso) {
          //$scope.progresoMultipleObjetos = progreso+"%";
        });




        //FUNCION QUE SE EJECUTA AL DAR CLICK EN UN MARCADOR DE UNA ESTACIÓN
        function onClickMarkerEstn(e) {

            controlLoader.show(); //SE MUESTRA LA NIMACION DE LOADING SOBRE EL MAPA
            var codigo = e.target.myCustomID; //SE OBTIENE EL CODIGO DE LA ESTACION
            map.setView(this.getLatLng(), 13, {animation: true}); //SE CENTRA LA ESTACION EN EL MAPA

            //SE CONSULTA EL SERVICIO DE DATOS DE UNA ESTACION
            Estaciones.estacion_get_with_codigo(codigo).then(function(data) {

                $scope.estacion = [];
                $scope.estacion = data;

                $scope.LinkData = "/estaciones/data_history/"+$scope.estacion.estn_codigo;

                controlLoader.hide();
                $('#modal_estaciones').modal({ blurring: true,  transition: 'vertical flip' }).modal('show');

            },$scope).catch(function(err) {
                alertify.error('OOPS! Error consultando información de la estación!');
            });

        }

        //FUNCION QUE SE EJECUTA AL DAR CLICK EN UN ICONO DE SUELO
        function onClickMarkerSuelo(e){

            var codigo = e.target.myCustomID; //SE OBTIENE EL CODIGO DE LA ESTACION
            map.setView(this.getLatLng(), 13, {animation: true}); //SE CENTRA LA ESTACION EN EL MAPA

            controlLoader.show();
            Suelo.muestras_perfil_with_code_json(codigo).then(function(data) {



                $scope.perfil = [];

                $scope.perfil = data.perfil;
                $scope.muestras = data.muestras;
                console.log($scope.muestras);

                controlLoader.hide();
                $('#modal_suelos').modal('setting', { detachable:false, allowMultiple: false }).modal('show');

            },$scope);

        }

        //FUNCION QUE SE EJECUTA AL DAR CLICK SOBRE UN ICONO DE MUESTRA
        function onClickMarkerMuestra(e){
            var muesid = e.target.myCustomID;

            map.setView(this.getLatLng(), 14, {animation: true}); //SE CENTRA LA ESTACION EN EL MAPA

            controlLoader.show();
            Suelo.muestra_with_muesid_json(muesid).then(function(data) {

                $scope.one_muestra = data.muestra;

                controlLoader.hide();
                $('#modal_muestras').modal('setting', { detachable:false, allowMultiple: false }).modal('show');

            },$scope);

        }

        //FUNCION QUE SE EJECUTA AL DAR CLICK SOBRE UN ICONO DE MUESTRA
        function onClickMarkerVoronoiPolygon(e){
            map.setView({lat: 8.23593, lng: -72.469341}, 11, {animation: true});

        }

        map.invalidateSize(); //ESTA LINEA DE CODIGO APLICA UN REFRESCO PARA REDIMENCIONAR EL MAPA

    }
}]);