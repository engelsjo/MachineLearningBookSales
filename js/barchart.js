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
     var h = 100;

     // svg element
     var svg = d3.select("body")
                 .append("svg")
                 .attr("width", w)
                 .attr("height", h);

    // create rectangles
    svg.selectAll("rect")
       .data(dataset)
       .enter()
       .append("rect")
       .attr("x", function(d, i) {
           return i * 21;
       })
       .attr("y", 0)
       .attr("width", 20)
       .attr("height", 100);

/*
       .attr("x", function(d, i) {
           return i * (w / dataset.length);
       })
       .attr("y", function(d) {
           return h - d; // height minus data value
       })
       .attr("width", w / dataset.length - barPadding)
       .attr("height", function(d) {
           return d; // just the data value
       });
       */

/*
     // width and height
     var w = 500;
     var h = 100;
     var padding = 50;

     // scale functions
     var xScale = d3.scale.linear()
                      .domain([0, d3.max(dataset, function(d) { return d[0]; })])
                      .range([padding, w - padding]);

     var yScale = d3.scale.linear()
                     .domain([0, d3.max(dataset, function(d) { return d[1]; })])
                     .range([h - padding, padding]);

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

     // create svg element
     var svg = d3.select("body")
                 .append("svg")
                 .attr("width", w)
                 .attr("height", h);

     // create circles
     svg.selectAll("circle")
         .data(dataset)
         .enter()
         .append("circle")
         .attr("cx", function(d) {
             return xScale(d[0]);
         })
         .attr("cy", function(d) {
             return yScale(d[1]);
         })
         .attr("r", 1);

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

*/
 }

function init() {
    barchart();
}

window.onload = function() {
    init();
}
