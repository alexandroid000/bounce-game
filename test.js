var lineData = [{ "x": 1,   "y": 5},  { "x": 20,  "y": 20},
                 { "x": 40,  "y": 10}, { "x": 60,  "y": 40},
                 { "x": 80,  "y": 5},  { "x": 100, "y": 60}];

var polygon = [{"x":250    ,"y":250},
    {"x":0      ,"y":100},
    {"x":-250   ,"y":250},
    {"x":-250   ,"y":-250},
    {"x":250    ,"y":-250},
    {"x":250    ,"y":250} ];

var lineFunction = d3.line()
     .x(function(d) { return d.x+300; })
     .y(function(d) { return d.y+300; });

var svgContainer = d3.select("body").append("svg")
                                    .attr("width", 600)
                                    .attr("height", 600);

//The line SVG Path we draw
var lineGraph = svgContainer.append("path")
                            .attr("d", lineFunction(polygon))
                            .attr("stroke", "black")
                            .attr("stroke-width", 5)
                            .attr("fill", "none");

var slider = d3
    .sliderHorizontal()
    .min(0)
    .max(3.14)
    .step(0.01)
    .width(400)
    .displayValue(false)
    .on('onchange', val => {
      d3.select('#value').text(val.toFixed(2)); // round theta to 2 decimals
    });

d3.select('#slider')
    .append('svg')
    .attr('width', 500)
    .attr('height', 100)
    .append('g')
    .attr('transform', 'translate(30,30)')
    .call(slider);
