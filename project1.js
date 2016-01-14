/* ***************************************************************************
 * @Title Machine Learning Project # 1
 * @Description: program to analyze data from book sales, and make predictions
 * @Authors: Michael Baldwin, Josh Engelsma, Adam Terwilliger
 * @Date: January 13, 2016
 * @Version 1.0
 ****************************************************************************/

function init() {

    var w = 1000;
    var h = 1000;

    var svg = d3.select("body")
                .append("svg")
                .attr("width", w)
                .attr("height", h);

    svg.selectAll("circle")
        .data(dataset)
        .enter()
        .append("circle")
        .attr("cx", function(d) {
            return d[0];
        })
        .attr("cy", function(d) {
            /*
            invert to not be graphics programming where origin
            is at top, left, but (0,0) origin at bottom, left
            */
            return h - (d[1] / 10);
        })
        .attr("r", 5);
}

window.onload = function() {
    init();
}
