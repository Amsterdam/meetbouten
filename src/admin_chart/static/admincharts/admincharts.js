window.addEventListener("DOMContentLoaded", function(event) {
    const configScript = document.getElementById("adminchart-chartjs-config");
    if (!configScript) return;
    const chartConfig = JSON.parse(configScript.textContent);
    chartConfig.options = {
        "aspectRatio": 6,
        "spanGaps": true,
        "autoSkip": true,
        "line": {"tension": 0.1},
        "scales": {
            "xAxes": [
                {
                    "type": "time",
                    "time": {"unit": "month"},
                }
            ]
        },
        "tooltips": {
            "callbacks": {
                "label": function(tooltipItem, data) {
                    return data.labels[tooltipItem.datasetIndex];
                }
            }
        }
    }
    if (!chartConfig) return;
    var container = document.getElementById('admincharts')
    var canvas = document.createElement("canvas")
    container.appendChild(canvas)
    var ctx = canvas.getContext('2d');
    var chart = new Chart(ctx, chartConfig);
});
