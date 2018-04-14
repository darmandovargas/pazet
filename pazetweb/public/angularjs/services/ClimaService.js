app.service('Clima',['$http', '$q', function ($http, $q){

   // OPTIENE LAS EMISIONES DE UN ESCENARIO CLIMATICO
   this.emisiones_with_escenario_json = function (escenario_id){

      var defered = $q.defer();
      var promise = defered.promise;

      $http({
            method: 'GET',
            url: '/clima/emisiones_with_escenario_json',
            params: {escenario_id: escenario_id},
            cache: false
      }).then(function (success){
            defered.resolve(success.data);
            //console.log(success.data);
      },function (error){
            defered.reject(error)
      });

      return promise;
   };

   //CONSULTA LAS VARIABLES CLIMATICAS ANUALES DE UNA ESTACION (PARA GRAFICAR)
   this.clima_year_estn_year_json = function (codigo, anioini, aniofin, intervalo){

      var defered = $q.defer();
      var promise = defered.promise;

      $http({
            method: 'GET',
            url: '/clima/clima_year_estn_year_json',
            params: {codigo:codigo, anioini:anioini, aniofin:aniofin, intervalo:intervalo},
            cache: false
      }).then(function (success){
            defered.resolve(success.data);
            //console.log(success.data);
      },function (error){
            defered.reject(error)
      });

      return promise;
   };


   //CONSULTA LAS VARIABLES CLIMATICAS MENSUALES DE UNA ESTACION (PARA GRAFICAR)
   this.clima_month_estn_year_json = function (codigo,anioini, aniofin, mesini, mesfin, intervalo){

      var defered = $q.defer();
      var promise = defered.promise;

      $http({
            method: 'GET',
            url: '/clima/clima_month_estn_year_json',
            params: {codigo:codigo, anioini:anioini, aniofin:aniofin, intervalo:intervalo, mesini:mesini, mesfin:mesfin},
            cache: false
      }).then(function (success){
            defered.resolve(success.data);
            //console.log(success.data);
      },function (error){
            defered.reject(error)
      });

      return promise;
   };


   //CONSULTA LAS VARIABLES CLIMATICAS DIARIAS DE UNA ESTACION (PARA GRAFICAR)
   this.clima_day_estn_year_json = function (codigo, anioini, fechaini, fechafin, intervalo){

      var defered = $q.defer();
      var promise = defered.promise;

      $http({
            method: 'GET',
            url: '/clima/clima_day_estn_year_json',
            params: {codigo:codigo, anioini:anioini, fechaini:fechaini, fechafin:fechafin, intervalo:intervalo},
            cache: false
      }).then(function (success){
            defered.resolve(success.data);
            //console.log(success.data);
      },function (error){
            defered.reject(error)
      });

      return promise;
   };







}]);