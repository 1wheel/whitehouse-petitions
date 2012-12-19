var xWidth;
var wHeight;
var scale;
var xHeight;
var petitionSummeries

function resize(){
	xWidth = document.getElementById("right").offsetWidth;
	wHeight = $(window).height();

	if (xWidth > wHeight){
		console.log("wide window");
		xWidth = Math.max((xWidth - 50)/2 - 20, 400);
	}
	else {
		xWidth = xWidth - 60;	
		xWidth = Math.max(xWidth, 400);
	}
	scale = xWidth/960;
	xHeight = 500*scale;
	petitionSummeries;

	d3.select("#chosvg").remove();
	drawMap();

	$("#lineContainer").width(xWidth);
	$("#graphContainer").width(xWidth);
}
resize();

function setup() {
	resize();

	d3.json("data/petitionSummeries.json", function(json, error) {
		petitionSummeries = json;
		setUpTable(petitionSummeries);
		
		var urlPetition = window.location.search.replace('?','').replace('/','').replace(/%20/g, ' ');
		console.log(urlPetition);
		if (petitionSummeries[urlPetition]){
			drawPetition(urlPetition);
		}
		else {
			drawPetition('End War On Coal');
		}

		//extend both divs to the bottom of the page
		pageHeight = Math.max($('#right').height(), $('#left').height());
		$('#right').height(pageHeight);
		$('#left').height($('#right').height());
	});
}

function drawPetition(petition){	
	console.log(petition);
	
	d3.json("data/"+petition+"_countyDisplay.json", function(json) {
		data = json;
		counties.selectAll("path")
				.attr("class", quantize);
	});

	d3.select("#currentLineGraph").remove();
	drawLine(petition);

	history.replaceState(null, null, window.location.pathname + "?" + petition +'/');
	highlightRow(petition);

	document.getElementById('petitionTitle').innerHTML = petition;
	$('#petitionTitle').attr('href', petitionSummeries[petition]['url']);
	$('#petitionLink').attr('href', petitionSummeries[petition]['url']);

	document.getElementById('importedHTML').innerHTML = petitionSummeries[petition][
	'html'];
}

function showfaq(){
	$(function() {
        $( "#faq" ).dialog(
        	{title: "FAQ",
        	minWidth:600,
        	position: [390,80]}
        );
    });
}

window.onload = setup;
window.onresize = setup;