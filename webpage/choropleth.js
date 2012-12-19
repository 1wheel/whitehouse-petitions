var data; // loaded asynchronously
var counties;
var tooltip;
 //width: 960px;
 //height: 500px;

function drawMap() {
	var path = d3.geo.path();

	var svg = d3.select("#choroplethGraph")
		.append("svg")
		.attr("id", "chosvg")
		.attr("height", xHeight)      
		.attr("viewBox", "0 0 960 500")
	    .attr("width", xWidth)
	    .attr("preserveAspectRatio", "true");

	counties = svg.append("g")
			.attr("id", "counties")
			.attr("class", "Blues");

	var states = svg.append("g")
			.attr("id", "states");

	tooltip = d3.select("body")
		.append("div")
		.attr("id","tooltip")

	d3.json("us-counties.json", function(json) {
		counties.selectAll("path")
				.data(json.features)
			.enter().append("path")
				.attr("class", data ? quantize : null)
				.attr("d", path)
			 	.on("mouseover", function(d){
			 		tooltip.text(d.properties.name + " County: " + data[d.id]['sum'] + " Signers");
			 		d3.select(this).style('stroke-width','4px');
			 		d3.select(this).style('stroke','red');
			 		tooltip.style("visibility", "visible");
			 	})
				.on("mousemove", function(){
					tooltip.style("top", (event.pageY-10)+"px").style("left",(event.pageX+10)+"px");})
				.on("mouseout", function(){
					d3.select(this).style('stroke-width','.25px');
					d3.select(this).style('stroke','grey');
					tooltip.style("visibility", "hidden");});
	;
	});

	d3.json("us-states.json", function(json) {
		states.selectAll("path")
				.data(json.features)
			.enter().append("path")
				.attr("d", path);
	});
}


function quantize(d) {
	return "q" + Math.floor(getCountyNorm(d.id)*10) + "-9";
}

function getCountyNorm(county){
	try{
		return data[county]['normalized'];
	}
	catch(e){
		return 0;
	}
}