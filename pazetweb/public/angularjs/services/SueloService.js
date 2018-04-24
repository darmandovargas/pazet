app.service('Suelo',['$http', '$q', function ($http, $q){


    //OPTIENE TODOS LOS PERFILES EN FORMATO GEOJSON
    this.all_perfiles_geojson = function (){

        var defered = $q.defer();
        var promise = defered.promise;

        $http({
            method: 'GET',
            url: '/suelo/all_perfiles_geojson',
            cache: true
        }).then(function (success){
            defered.resolve(success.data);
            //console.log(success.data);
        },function (error){
            defered.reject(error)
        });

        return promise;
    };

    //OPTIENE TODAS LAS MUESTRAS QUE NO PERTENECEN A UN PERFIL
    this.all_muestras_geojson = function (){

        var defered = $q.defer();
        var promise = defered.promise;

        $http({
            method: 'GET',
            url: '/suelo/all_muestras_geojson',
            cache: true
        }).then(function (success){
            defered.resolve(success.data);
            //console.log(success.data);
        },function (error){
            defered.reject(error)
        });

        return promise;
    };

    // OBTIENE LAS MUESTRAS DE SUELO DE EL ZULIA
    // @author Diego Vargas
    this.get_muestras_elzulia_geojson = function (){

        var defered = $q.defer();
        var promise = defered.promise;

        $http({
            method: 'GET',
            url: '/suelo/all_muestras_geojson',
            cache: true
        }).then(function (success){
            defered.resolve(success.data);
            //console.log(success.data);
        },function (error){
            defered.reject(error)
        });

        return promise;
    };

    //OPTIENE LAS MUESTRA DE UN PERFIL
    this.muestras_perfil_with_code_json = function (codigo){

        var defered = $q.defer();
        var promise = defered.promise;

        $http({
            method: 'GET',
            url: '/suelo/muestras_perfil_with_code_json',
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

    //OPTIENE LA INFORMACION DE UNA MUESTRA ESPESIFICA
    this.muestra_with_muesid_json = function (muesid){

        var defered = $q.defer();
        var promise = defered.promise;

        $http({
            method: 'GET',
            url: '/suelo/muestra_with_muesid_json',
            params: {muesid: muesid},
            cache: false
        }).then(function (success){
            defered.resolve(success.data);
            //console.log(success.data);
        },function (error){
            defered.reject(error)
        });

        return promise;
    };



    this.variables_prop_metales_pesados_json = function (){

        var defered = $q.defer();
        var promise = defered.promise;

        $http({
            method: 'GET',
            url: '/suelo/variables_prop_metales_pesados_json',
            params: {},
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