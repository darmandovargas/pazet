app.service('Estaciones',['$http', '$q', function ($http, $q){

   // OPTIENE TODAS LAS ESTACIONES QUE CONTIENEN DATOS (Climaticos y Caudales) MENSUALES Y DIARIOS PARA DESPLIEGUE EN EL MAPA
   this.all_stations_geojson = function (){

      var defered = $q.defer();
      var promise = defered.promise;

      $http({
            method: 'GET',
            url: '/estaciones/all_stations_geojson',
            cache: true
      }).then(function (success){
            defered.resolve(success.data);
            //console.log(success.data);
      },function (error){
            defered.reject(error)
      });

      return promise;
   };

   //OPTIENE TODA LA INFORMACION DE UNA ESTACION POR SU CODIGO
   this.estacion_get_with_codigo = function (codigo){

      var defered = $q.defer();
      var promise = defered.promise;

      $http({
            method: 'GET',
            url: '/estaciones/estacion_get_with_codigo',
            params: {codigo: codigo},
            cache: false
      }).then(function (success){
            defered.resolve(success.data);
            //console.log(success.data);
      },function (error){
            defered.reject(error)
      });

      return promise;
   };


   // ******************************************************************************************************************
   // ***************************************** CLIMA MENSUAL **********************************************************
   // ******************************************************************************************************************

   //OPTIENE TODAS LAS ESTACIONES PRESENTES EN INFORMACION DE CLIMA MENSUALES (GEOJSON)
   this.all_estn_clima_month_geojson = function (){
      var defered = $q.defer();
      var promise = defered.promise;

      $http({
            method: 'GET',
            url: '/estaciones/all_estn_clima_month_geojson',
            cache: true
      }).then(function (success){
            defered.resolve(success.data);
            //console.log(success.data);
      },function (error){
            defered.reject(error);
      });

      return promise;
   };

   //OPTIENE TODAS LAS ESTACIONES QUIE INSIDEN EN UN POLIGONO Y CLIMA MENSUAL
   this.filtro_estn_in_poligon_cmonth_json = function (type,data,radio){

        var defered = $q.defer();
        var promise = defered.promise;

        $http({
            method: 'GET',
            url: '/estaciones/filtro_estn_in_poligon_cmonth_json',
            params: { tipo:type, puntos:data, radio:radio },
            cache: false
        }).then(function (success){
            defered.resolve(success.data);
            //console.log(success.data);
        },function (error){
            defered.reject(error)
        });

        return promise;
   };

   //OPTIENE TODAS LAS ESTACIONES PRESENTES EN INFORMACION DE CLIMA MENSUALES Y PERTENECEN A UN DEPARTAMENTO (JSON)
   this.estn_clima_month_depto_json = function (codane){

      var defered = $q.defer();
      var promise = defered.promise;

      $http({
            method: 'GET',
            url: '/estaciones/estn_clima_month_depto_json',
            params: {codane: codane},
            cache: false
      }).then(function (success){
            defered.resolve(success.data);
            //console.log(success.data);
      },function (error){
            defered.reject(error);
      });

      return promise;
   };

   //OPTIENE TODAS LAS ESTACIONES PRESENTES EN INFORMACION DE CLIMA MENSUALES Y PERTENECEN A UN MUNICIPIO (JSON)
   this.estn_clima_month_mun_json = function (munid){

      var defered = $q.defer();
      var promise = defered.promise;

      $http({
            method: 'GET',
            url: '/estaciones/estn_clima_month_mun_json',
            params: {munid: munid},
            cache: false
      }).then(function (success){
            defered.resolve(success.data);
            //console.log(success.data);
      },function (error){
            defered.reject(error);
      });

      return promise;
   };

   //BUSCA UNA ESTACION POR CODIGO Y QUE ADEMAS CONTENGA INFORMACION CLIMATICA MENSUAL (JSON)
   this.estn_codigo_clima_month_json = function (codigo){

      var defered = $q.defer();
      var promise = defered.promise;

      $http({
            method: 'GET',
            url: '/estaciones/estn_codigo_clima_month_json',
            params: {codigo: codigo},
            cache: false
      }).then(function (success){
            defered.resolve(success.data);
            //console.log(success.data);
      },function (error){
            defered.reject(error);
      });

      return promise;
   };

   //BUSCA UNA ESTACIÓN POR PARTE DEL NOMBRE Y QUE ADEMAS CONTENGA INFORMACIÓN CLIMATICA MENSUAL (JSON)
   this.estn_name_clima_month_json = function (nombre){

      var defered = $q.defer();
      var promise = defered.promise;

      $http({
            method: 'GET',
            url: '/estaciones/estn_name_clima_month_json',
            params: {nombre: nombre},
            cache: false
      }).then(function (success){
            defered.resolve(success.data);
            //console.log(success.data);
      },function (error){
            defered.reject(error);
      });

      return promise;
   };
   // ******************************************************************************************************************



   // ******************************************************************************************************************
   // ****************************************** CLIMA DIARIO **********************************************************
   // ******************************************************************************************************************

   //OPTIENE TODAS LAS ESTACIONES PRESENTES EN INFORMACION DE CLIMA DIARIA (GEOJSON)
   this.all_estn_clima_day_geojson = function (){
      var defered = $q.defer();
      var promise = defered.promise;

      $http({
            method: 'GET',
            url: '/estaciones/all_estn_clima_day_geojson',
            cache: true
      }).then(function (success){
            defered.resolve(success.data);
            //console.log(success.data);
      },function (error){
            defered.reject(error);
      });

      return promise;
   };

   //OPTIENE TODAS LAS ESTACIONES QUIE INSIDEN EN UN POLIGONO Y CLIMA DIARIO
   this.filtro_estn_in_poligon_cday_json = function (type,data,radio){

        var defered = $q.defer();
        var promise = defered.promise;

        $http({
            method: 'GET',
            url: '/estaciones/filtro_estn_in_poligon_cday_json',
            params: { tipo:type, puntos:data, radio:radio },
            cache: false
        }).then(function (success){
            defered.resolve(success.data);
            //console.log(success.data);
        },function (error){
            defered.reject(error)
        });

        return promise;
   };

   //OPTIENE TODAS LAS ESTACIONES PRESENTES EN INFORMACION DE CLIMA DIARIO Y PERTENECEN A UN DEPARTAMENTO (JSON)
   this.estn_clima_day_depto_json = function (codane){

      var defered = $q.defer();
      var promise = defered.promise;

      $http({
            method: 'GET',
            url: '/estaciones/estn_clima_day_depto_json',
            params: {codane: codane},
            cache: false
      }).then(function (success){
            defered.resolve(success.data);
            //console.log(success.data);
      },function (error){
            defered.reject(error);
      });

      return promise;
   };

   //OPTIENE TODAS LAS ESTACIONES PRESENTES EN INFORMACION DE CLIMA DIARIO Y PERTENECEN A UN MUNICIPIO (JSON)
   this.estn_clima_day_mun_json = function (munid){

      var defered = $q.defer();
      var promise = defered.promise;

      $http({
            method: 'GET',
            url: '/estaciones/estn_clima_day_mun_json',
            params: {munid: munid},
            cache: false
      }).then(function (success){
            defered.resolve(success.data);
            //console.log(success.data);
      },function (error){
            defered.reject(error);
      });

      return promise;
   };

   //BUSCA UNA ESTACION POR CODIGO Y QUE ADEMAS CONTENGA INFORMACION CLIMATICA MENSUAL (JSON)
   this.estn_codigo_clima_day_json = function (codigo){

      var defered = $q.defer();
      var promise = defered.promise;

      $http({
            method: 'GET',
            url: '/estaciones/estn_codigo_clima_day_json',
            params: {codigo: codigo},
            cache: false
      }).then(function (success){
            defered.resolve(success.data);
            //console.log(success.data);
      },function (error){
            defered.reject(error);
      });

      return promise;
   };

   //BUSCA UNA ESTACIÓN POR PARTE DEL NOMBRE Y QUE ADEMAS CONTENGA INFORMACIÓN CLIMATICA MENSUAL (JSON)
   this.estn_name_clima_day_json = function (nombre){

      var defered = $q.defer();
      var promise = defered.promise;

      $http({
            method: 'GET',
            url: '/estaciones/estn_name_clima_day_json',
            params: {nombre: nombre},
            cache: false
      }).then(function (success){
            defered.resolve(success.data);
            //console.log(success.data);
      },function (error){
            defered.reject(error);
      });

      return promise;
   };

   // ******************************************************************************************************************


   // ******************************************************************************************************************
   // ****************************************** CAUDAL DIARIO *********************************************************
   // ******************************************************************************************************************

   //OPTIENE TODAS LAS ESTACIONES PRESENTES EN INFORMACION DE CLIMA DIARIO (GEOJSON)
   this.all_estn_caudal_diario_geojson = function (){

        var defered = $q.defer();
        var promise = defered.promise;

        $http({
            method: 'GET',
            url: '/estaciones/all_estn_caudal_diario_geojson',
            cache: true
        }).then(function (success){
            defered.resolve(success.data);
            //console.log(success.data);
        },function (error){
            defered.reject(error)
        });

        return promise;
   };


   //OPTIENE TODAS LAS ESTACIONES QUIE INSIDEN EN UN POLIGONO Y CLIMA DIARIO
   this.filtro_estn_in_poligon_cauday_json = function (type,data,radio){

        var defered = $q.defer();
        var promise = defered.promise;

        $http({
            method: 'GET',
            url: '/estaciones/filtro_estn_in_poligon_cauday_json',
            params: { tipo:type, puntos:data, radio:radio },
            cache: false
        }).then(function (success){
            defered.resolve(success.data);
            //console.log(success.data);
        },function (error){
            defered.reject(error)
        });

        return promise;
   };

   //OPTIENE TODAS LAS ESTACIONES PRESENTES EN INFORMACION DE CLIMA DIARIO Y PERTENECEN A UN DEPARTAMENTO (JSON)
   this.estn_caudal_day_depto_json = function (codane){

      var defered = $q.defer();
      var promise = defered.promise;

      $http({
            method: 'GET',
            url: '/estaciones/estn_caudal_day_depto_json',
            params: {codane: codane},
            cache: false
      }).then(function (success){
            defered.resolve(success.data);
            //console.log(success.data);
      },function (error){
            defered.reject(error);
      });

      return promise;
   };

   //OPTIENE TODAS LAS ESTACIONES PRESENTES EN INFORMACION DE CLIMA DIARIO Y PERTENECEN A UN MUNICIPIO (JSON)
   this.estn_caudal_day_mun_json = function (munid){

      var defered = $q.defer();
      var promise = defered.promise;

      $http({
            method: 'GET',
            url: '/estaciones/estn_caudal_day_mun_json',
            params: {munid: munid},
            cache: false
      }).then(function (success){
            defered.resolve(success.data);
            //console.log(success.data);
      },function (error){
            defered.reject(error);
      });

      return promise;
   };

   //BUSCA UNA ESTACION POR CODIGO Y QUE ADEMAS CONTENGA INFORMACION CLIMATICA MENSUAL (JSON)
   this.estn_codigo_caudal_day_json = function (codigo){

      var defered = $q.defer();
      var promise = defered.promise;

      $http({
            method: 'GET',
            url: '/estaciones/estn_codigo_caudal_day_json',
            params: {codigo: codigo},
            cache: false
      }).then(function (success){
            defered.resolve(success.data);
            //console.log(success.data);
      },function (error){
            defered.reject(error);
      });

      return promise;
   };

   //BUSCA UNA ESTACIÓN POR PARTE DEL NOMBRE Y QUE ADEMAS CONTENGA INFORMACIÓN CLIMATICA MENSUAL (JSON)
   this.estn_name_caudal_day_json = function (nombre){

      var defered = $q.defer();
      var promise = defered.promise;

      $http({
            method: 'GET',
            url: '/estaciones/estn_name_caudal_day_json',
            params: {nombre: nombre},
            cache: false
      }).then(function (success){
            defered.resolve(success.data);
            //console.log(success.data);
      },function (error){
            defered.reject(error);
      });

      return promise;
   };



}]);