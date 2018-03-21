app.service('Agua',['$http', '$q', function ($http, $q){


    //OPTIENE TODOS LOS PERFILES EN FORMATO GEOJSON
    this.caudal_day_estn_year_json = function (codigo,anioini){

        var defered = $q.defer();
        var promise = defered.promise;

        $http({
            method: 'GET',
            url: '/agua/caudal_day_estn_year_json',
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



    this.cdc_diaria_estn_json = function (codigo){

        var defered = $q.defer();
        var promise = defered.promise;

        $http({
            method: 'GET',
            url: '/agua/cdc_diaria_estn_json',
            params: {codigo:codigo},
            cache: false
        }).then(function (success){
            defered.resolve(success.data);
            console.log(success.data);
        },function (error){
            defered.reject(error)
        });

        return promise;
    };




}]);