/* ***************************************************************************
 * @Title Machine Learning Project # 1
 * @Description: program to analyze data from book sales, and make predictions
 * @Authors: Michael Baldwin, Josh Engelsma, Adam Terwilliger
 * @Date: January 13, 2016
 * @Version 1.0
 ****************************************************************************/

 /* http://alignedleft.com/tutorials/d3/making-a-bar-chart */
 function barchart() {

    // width and height
    var w = 500;
    var h = 500;
    var barHeight = 20;

    var svg = d3.select("body")
    .append("svg")
    .attr("width", w)
    .attr("height", h)
    .attr("class", "chart");

    var chart = d3.select(".chart")
    .attr("width", w)
    .attr("height", barHeight * dataset.length);

    var x = d3.scale.linear()
    .domain([0, d3.max(dataset)])
    .range([0, w]);

    var bar = chart.selectAll("g")
    .data(dataset)
    .enter().append("g")
    .attr("transform", function(d, i) { return "translate(0," + i * barHeight + ")"; });

    bar.append("rect")
    .attr("width", w)
    .attr("height", barHeight - 1);
 }

function init() {
    barchart();
}

window.onload = function() {
    init();
};
