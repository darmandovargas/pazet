app.controller('ClimaCo2Controller', ['$scope','Clima', function($scope,Clima) {


    $('.ui.styled.accordion').accordion({
        onOpening: function () {
            var emision_id = this.attr('id');
            var emision = this.data('escenario');
            //console.log(this.index(".content"));

            alertify.notify('Generando gráfico por favor espere...', 'custom', 2, function(){ });
            Clima.emisiones_with_escenario_json(emision_id).then(function(data) {

                 $scope.dataGrap = data;

                 optionsCo2['series'][0].data = [];
                 optionsCo2['xAxis']['categories'] = [];
                 optionsCo2['title']['text'] = '';

                 optionsCo2['title']['text'] = 'Gráfico Emisión CO2 Escenario '+emision;
                 optionsCo2['series'][0].data = $scope.dataGrap.emisiones;
                 optionsCo2['xAxis']['categories'] = $scope.dataGrap.yearemi;
                 Highcharts.chart('graph_dia_co2', optionsCo2);

            }).catch(function(err) {
                console.log(err);
                alertify.error('OOPS! Error consultando información!');
            });

        }
    });




}]);