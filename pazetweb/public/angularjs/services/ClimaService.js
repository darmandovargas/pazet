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


   //CONSULTA LAS VARIABLES CLIMATICAS MENSUALES DE UNA ESTACION (PARA GRAFICAR)
   this.clima_month_estn_year_json = function (codigo,anioini){

      var defered = $q.defer();
      var promise = defered.promise;

      $http({
            method: 'GET',
            url: '/clima/clima_month_estn_year_json',
            params: {codigo:codigo,anioini:anioini},
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
   this.clima_day_estn_year_json = function (codigo,anioini){

      var defered = $q.defer();
      var promise = defered.promise;

      $http({
            method: 'GET',
            url: '/clima/clima_day_estn_year_json',
            params: {codigo:codigo,anioini:anioini},
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