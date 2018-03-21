var optionsCo2 = {
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
    subtitle: { text: '' },
    xAxis: {
        categories:  [],
        labels: {
            rotation: -45
        }
    },
    yAxis: {
        title: {
            text: 'CO2'
        }
    },
    legend: { enabled: false },
    tooltip: {
        //valueSuffix: '°C',
        formatter: function() {
                return  '<b>' + this.series.name +'</b>: '+this.y+'<br/> <b>Año:</b>' + this.x;
        }
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
        name:'CO2',
        data:  [],
        color:'#D50000'
    }]

};