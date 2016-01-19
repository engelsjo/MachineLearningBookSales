/* ***************************************************************************
* @Title Machine Learning Project # 1
* @Description: program to analyze data from book sales, and make predictions
* @Authors: Michael Baldwin, Josh Engelsma, Adam Terwilliger
* @Date: January 13, 2016
* @Version 1.0
****************************************************************************/

window.onload = function() {
    init();
};

function init() {
    scatterplot();
}

/* http://alignedleft.com/tutorials/d3/making-a-scatterplot */
/* http://bl.ocks.org/benvandyke/8459843 */
function scatterplot() {

    // width and height
    var w = 400;
    var h = 400;
    var padding = 50;

    // create svg element
    var svg = d3.select("body")
    .append("svg")
    .attr("width", w)
    .attr("height", h);

    // scale functions
    var xScale = d3.scale.linear()
    .domain([0, d3.max(dataset, function(d) { return d[0]; })])
    .range([padding, w - padding]);

    var yScale = d3.scale.linear()
    .domain([0, d3.max(dataset, function(d) { return d[1]; })])
    .range([h - padding, padding]);

    // create circles
    svg.selectAll("datapoints")
    .data(dataset)
    .enter()
    .append("circle")
    .attr("class", "datapoints")
    .attr("cx", function(d) {
        return xScale(d[0]);
    })
    .attr("cy", function(d) {
        return yScale(d[1]);
    })
    .attr("r", 2);

    // create nan circles
    svg.selectAll("nans")
    .data(nans)
    .enter()
    .append("circle")
    .attr("class", "nans")
    .attr("cx", function(d) {
        return xScale(d[0]);
    })
    .attr("cy", function(d) {
        return yScale(d[1]);
    })
    .attr("r", 3)
    .style("fill", "cyan");

    // define X-axis
    var xAxis = d3.svg.axis()
    .scale(xScale)
    .orient("bottom")
    .ticks(10);

    // define Y-axis
    var yAxis = d3.svg.axis()
    .scale(yScale)
    .orient("left")
    .ticks(5);

    // create X-axis
    svg.append("g")
    .attr("class", "axis")
    .attr("transform", "translate(0," + (h - padding) + ")")
    .call(xAxis);

    // create Y-axis
    svg.append("g")
    .attr("class", "axis")
    .attr("transform", "translate(" + padding + ",0)")
    .call(yAxis);

    // trend line
    svg.append("line")
    .attr("class", "trendLine")
    .attr("x1", xScale(0))
    .attr("y1", yScale(986))
    .attr("x2", xScale(800))
    .attr("y2", yScale(3081));

    // quadratic
    points = [{x: 0, y: 1974}, {x: 186, y: 1356}, {x: 372, y: 1472}, {x: 558, y: 2321}];

    var line = d3.svg.line()
    .x(function(d) {
        return xScale(d.x);
    })
    .y(function(d) {
        return yScale(d.y);
    });

    svg.append("path")
    .datum(points)
    .attr("class", "quad")
    .attr("d", line);
}
