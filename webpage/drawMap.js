function drawMap(petition){
	var width = 900;
	var height = 500;

	var quantize = d3.scale.quantize()
			.domain([0, 1])
			.range(d3.range(9).map(function(i) { return "q" + i + "-9"; }));

	var path = d3.geo.path();

	var svg = d3.select("svg")
			.attr("width", width)
			.attr("height", height)
			.attr("class", "Blues");

	queue()
			.defer(d3.json, "us-counties.json")
			.defer(d3.json, "us-states.json")
			.defer(d3.tsv, "unemployment.tsv")
			.defer(d3.json, "data\\"+petition+"_countyDisplay.json")
			.await(ready);

	function ready(error, counties, states, unemployment, countyDisplay) {
		dC = [];
		c = counties;
		svg.append('g')
				.attr('class', 'counties')
			.selectAll('path')
				.data(counties.features)
			.enter().append('path')
				.attr('class', function(d) { 
					console.log(d);
					dC[dC.length] = d.id;
					return "q0-9";
					//return quantize(getCountyNorm(countyDisplay[d.id])); 
				})
				.attr('d', path)
		 		.on('mouseover', function(d){
		 			console.log(d);
		 			displayMouseOver(d.properties.name, countyDisplay[d.id]['sum']);
		 		});
        
		svg.append("path")
				.datum(states)
				.attr("class", "states")
				.attr("d", path);
	}

	function getCountyNorm(county){
		try{
			return county['normalized'];
		}
		catch(e){
			return 0;
		}
	}

	function displayMouseOver(name, sum){
		document.getElementById('mouseOver').innerHTML = name + " County: " + sum + " Signers";
	}
}

drawMap('ImpeachObama');