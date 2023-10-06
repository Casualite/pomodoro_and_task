<template>
    <LineChartGenerator
      :chart-options="chartOptions"
      :chart-data="chartData"
      :chart-id="chartId"
      :dataset-id-key="datasetIdKey"
      :plugins="plugins"
      :css-classes="cssClasses"
      :styles="styles"
      :width="width"
      :height="height"
       />
  </template>
  
  <script>
  import { Line as LineChartGenerator } from 'vue-chartjs/legacy'
  
  import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    LineElement,
    LinearScale,
    CategoryScale,
    PointElement
  } from 'chart.js'
  
  ChartJS.register(
    Title,
    Tooltip,
    Legend,
    LineElement,
    LinearScale,
    CategoryScale,
    PointElement
  )
  
  export default {
    name: 'LineChart',
    components: {
      LineChartGenerator
    },
    props: {
      chartId: {
        type: String,
        default: 'line-chart'
      },
      datasetIdKey: {
        type: String,
        default: 'Date'
      },
      datasetYaxisKey: {
        type: String,
        default: 'Description'
      },
      width: {
        type: Number,
        default: 400
      },
      height: {
        type: Number,
        default: 400
      },
      cssClasses: {
        default: '',
        type: String
      },
      styles: {
        type: Object,
        default: () => {}
      },
      plugins: {
        type: Array,
        default: () => []
      },
      Data_x:{
        type: Array
      },
      Data_y:
      {
        type: Array
      }
    },
    data(){
      return {
        chartData: {
            labels: this.Data_x,
        datasets: [
          {
            label:"Line Graph",
            backgroundColor: '#f87979',
            data: this.Data_y
          }
        ]
        },
        chartOptions: {
          responsive: true,
          maintainAspectRatio: false
        },
        options: {
        scales: {
            xAxes: [{
                type: "string",
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: 'Date'
                },
            }]
        },
        
    }
      }
    },
    watch: { 
        Data_y : function(new_value) { 
            this.chartData.datasets[0].data=new_value
        },
        Data_x : function(new_value) { 
        this.chartData.labels=new_value
        }
    }
  }
  </script>
  