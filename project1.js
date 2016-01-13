/* ***************************************************************************
 * @Title Machine Learning Project # 1
 * @Description: program to analyze data from book sales, and make predictions
 * @Authors: Michael Baldwin, Josh Engelsma, Adam Terwilliger
 * @Date: January 13, 2016
 * @Version 1.0
 ****************************************************************************/

function initialize() {
    d3.select("body").selectAll("p")
        .data(dataset)
        .enter()
        .append("p")
        .text(function(d) { return d; })
        .style("color", function(d) {
            if (d > 1) {
                return "red";
            } else {
                return "black";
            }
    });
};

window.onload = function() {
    initialize();
};
