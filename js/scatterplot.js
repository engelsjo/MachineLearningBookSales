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

// width and height
var w = 400;
var h = 400;
var padding = 60;
var labelPadding = 30;

// scale functions
var xScale = d3.scale.linear()
.domain([0, d3.max(dataset, function(d) { return d[0]; })])
.range([padding, w - padding]);

var yScale = d3.scale.linear()
.domain([0, d3.max(dataset, function(d) { return d[1]; })])
.range([h - padding, padding]);

/* http://alignedleft.com/tutorials/d3/making-a-scatterplot */
/* http://bl.ocks.org/benvandyke/8459843 */
/* http://bl.ocks.org/phil-pedruco/88cb8a51cdce45f13c7e */
/* http://bl.ocks.org/phoebebright/3061203 */
function scatterplot() {

    // create svg element
    var svg = d3.select("body")
    .append("svg")
    .attr("width", w)
    .attr("height", h);

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

    // quadratic
    var quadraticLine = d3.svg.line()
    .x(function(d) {
        return xScale(d[0]);
    })
    .y(function(d) {
        return yScale(quadratic(d[0]));
    });

    svg.append("path")
    .datum(dataset)
    .attr("class", "quad")
    .attr("d", quadraticLine);

    // linear
    var linearLine = d3.svg.line()
    .x(function(d) {
        return xScale(d[0]);
    })
    .y(function(d) {
        return yScale(linear(d[0]));
    });

    svg.append("path")
    .datum(dataset)
    .attr("class", "cubic")
    .attr("d", pathLine(cubic));

    svg.append("path")
    .datum(dataset)
    .attr("class", "linear")
    .attr("d", linearLine);

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
    .attr("r", 3);

    svg.append("text")
    .attr("class", "label")
    .attr("text-anchor", "middle")
    .attr("transform", "translate("+ (w/2) +","+(h-(labelPadding/1.5))+")")
    .text("Time of Download (Hours)");

    svg.append("text")
    .attr("class", "label")
    .attr("text-anchor", "middle")
    .attr("transform", "translate("+ (labelPadding/2) +","+(h/2)+")rotate(-90)")
    .text("Number of Downloads");
}

function pathLine(fn) {
    return d3.svg.line()
    .x(function(d) {
        return xScale(d[0]);
    })
    .y(function(d) {
        return yScale(fn(d[0]));
    });
}

function quadratic(x) {
    return 0.0106160902962 * Math.pow(x, 2) + -5.29438577386 * x + 1974.18190474;
}

function linear(x) {
    return 2.61928481625 * x + 985.846767649;
}

function cubic(x) {
    return 3.07350980198 * Math.pow(10, -5) * Math.pow(x, 3) +
        -0.0237269023042 * Math.pow(x, 2) + 4.95214473622 * x + 1335.36380284;
}
