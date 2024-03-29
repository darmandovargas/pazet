/**
 * Created by gaspar on 22/sept/15.
 */

//angularJS
var app = angular.module('app',[]);

     app.config(['$interpolateProvider', '$httpProvider',function ($interpolateProvider, $httpProvider) {
        //configuramos los símbolos  
         $interpolateProvider.startSymbol('[[');
         $interpolateProvider.endSymbol(']]');
         //configuramos el CSRFTOKEN para las peticiones con ANGULARJS
         $httpProvider.defaults.xsrfCookieName = 'csrftoken';
         $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
         $httpProvider.defaults.withCredentials = true;
         $httpProvider.defaults.cache=true;
         $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8';

         //función para compatibilidad de transmisión de datos JSON por POST
         var param = function(obj) {
             var query = '', name, value, fullSubName, subName, subValue, innerObj, i;
             for(name in obj) {
                 value = obj[name];
                if(value instanceof Array) {
                    for(i=0; i<value.length; ++i) {
                      subValue = value[i];
                      fullSubName = name + '[' + i + ']';
                      innerObj = {};
                      innerObj[fullSubName] = subValue;
                      query += param(innerObj) + '&';
                    }
                    }
                else if(value instanceof Object) {
                    for(subName in value) {
                      subValue = value[subName];
                      fullSubName = name + '[' + subName + ']';
                      innerObj = {};
                      innerObj[fullSubName] = subValue;
                      query += param(innerObj) + '&';
                    }
                }
                else if(value !== undefined && value !== null)
                    query += encodeURIComponent(name) + '=' + encodeURIComponent(value) + '&';
                }
             return query.length ? query.substr(0, query.length - 1) : query;
         };

         // Override $http service's default transformRequest
         $httpProvider.defaults.transformRequest = [function(data) {
             return angular.isObject(data) && String(data) !== '[object File]' ? param(data) : data;
         }];
     }]);
