
// *********************************************************************************************************************
// ************************************* GRAFICO DE PRECIPITACIÓN ******************************************************
// *********************************************************************************************************************
var optionsPpt = {
    chart: {
    type: 'column',
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
        title: { text: 'Precipitación' },
        labels: { format: '{value} mm' }
    },
    legend: { enabled: true },
    tooltip: {
        valueSuffix: 'mm',
        formatter: function() {
                return  '<b>' + this.series.name +'</b>: '+this.y+'<br/> <b>Fecha: </b>' + this.x;
        }
    },
    series: [{
        name:'Precipitación',
        data:  [],
        color:'#4FC3F7'
    }]

};



// *********************************************************************************************************************
// ************************************** GRAFICO DE TEMPERATURAS ******************************************************
// *********************************************************************************************************************

var optionsTemp = {
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
        },

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
        title: { text: 'Temperatura' },
        labels: { format: '{value} °C' }
    },
    legend: { enabled: true },
    tooltip: {
        valueSuffix: '°C',
        /*formatter: function() {
                return  '<b>' + this.series.name +'</b>: '+this.y+' °C<br/> <b>Fecha: </b>' + this.x;
        },*/
        crosshairs: {
            color: '#616161',
            dashStyle: 'solid'
        },
        shared: true
    },

    series: [{
        name:'Temp maxima',
        type: 'spline',
        data:  [],
        color:'#D50000'
    },{
        name:'Temp media',
        type: 'spline',
        data:  [],
        color:'#FF9800'
    },{
        name:'Temp minima',
        type: 'spline',
        data:  [],
        color:'#607D8B'
    }]

};


// *********************************************************************************************************************
// ************************************** GRAFICO DE HUMEDAD ******************************************************
// *********************************************************************************************************************

var optionsHum = {
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
            text: 'Humedad (%)'
        },
        labels: {
            format: '{value}%'
        }
    },
    legend: { enabled: true },
    tooltip: {
        valueSuffix: '%',
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
                    [0, Highcharts.getOptions().colors[0]],
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
        name: 'Humedad',
        color: '#2196F3',
        data: [],
        type: 'area'
    }]


};


// *********************************************************************************************************************
// ************************************** GRAFICO DE BRILLO SOLAR ******************************************************
// *********************************************************************************************************************
var optionsBs = {
    chart: {
    type: 'column',
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
        title: { text: 'Brillo solar' },
        labels: { format: '{value}' }
    },
    legend: { enabled: true },
    tooltip: {
        valueSuffix: '?',
        formatter: function() {
                return  '<b>' + this.series.name +'</b>: '+this.y+'<br/> <b>Fecha: </b>' + this.x;
        }
    },
    series: [{
        name:'Brillo solar',
        data:  [],
        color:'#FFD600'
    }]

};