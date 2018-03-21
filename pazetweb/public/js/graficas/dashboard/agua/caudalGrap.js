
// *********************************************************************************************************************
// ************************************** GRAFICO DE CAUDALES **********************************************************
// *********************************************************************************************************************

var optionsCaudal = {
    chart: {
        zoomType: 'xy',
        resetZoomButton: {
            position: {
                align: 'right',
                verticalAlign: 'top',
                x: -10,
                y: 10
            },
            relativeTo: 'chart'
        }
    },
    title: {
        text: ''
    },
    subtitle: { text: 'Plataforma Agroclimatica de Zonificación Espacio Temporal' },
    xAxis: {
        categories:  [],
        labels: {
            rotation: -45
        },
        tickInterval: null
    },
    yAxis: {
        title: {
            text: 'Caudal (m3/s)'
        },
        labels: {
            format: '{value} m3/s'
        }
    },
    legend: { enabled: true },
    tooltip: {
        valueSuffix: ' m3/s',
        /*formatter: function() {
            return  '<b>' + this.series.name +'</b>: '+this.y+'%<br/>Fecha: ' + this.x;
        }*/
        crosshairs: {
            color: '#616161',
            dashStyle: 'solid'
        },
        shared: true
    },
    plotOptions: {
        area: {
            fillColor: {
                linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                stops: [
                    [0, Highcharts.getOptions().colors[3]],
                    [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                ]
            },
            marker: { radius: 2 },
            lineWidth: 1,
            states: {
                hover: { lineWidth: 1 }
            },
            threshold: null
        }
    },
    series: [{
        name: 'Caudal',
        color: '#2196F3',
        data: [],
        type: 'area'
    }]

};


// *********************************************************************************************************************
// ************************************** GRAFICO DE CURVA DE DURACION DE CAUDAL ***************************************
// *********************************************************************************************************************

var optionsCdc = {
    chart: {
        type: 'line',
        reflow: true
    },
    title: { text: 'Grafica curva duración de caudal' },
    subtitle: { text: 'Plataforma Agroclimatica de Zonificación Espacio Temporal' },
    xAxis: {
        //type: 'logarithmic',
        categories: [],
        labels: {
            rotation: -45
        }
    },
    yAxis: {
        title: {
            text: 'Caudal (m3/s)'
        },
        labels: {
            format: '{value} m3/s'
        }
    },
    tooltip: {
        backgroundColor: '#C8E6C9',
        borderColor: 'black',
        borderRadius: 10,
        borderWidth: 1,
        crosshairs: [{
            width: 1,
            dashStyle: 'solid',
            color: '#9E9E9E'
        }, true],
        formatter: function() {
            return 'Duración <b>' + this.x + '(%)</b> <br> '+this.series.name.split("(")[0] +' <b>' + this.y + ' m3/s</b>';
        }
    },
    series: [{
        color: '#3F51B5',
        name: 'Curva de duración de caudal',
        data: [],
        pointStart: 1
    }]


};