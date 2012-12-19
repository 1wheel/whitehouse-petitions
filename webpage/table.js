function setUpTable(petitionJSON){
	var chart = document.getElementById("chart");
	var width = chart.offsetWidth;
	var height = chart.offsetHeight;
	 
	var dataArray = [];
	$.each(petitionJSON, function(index, value){
		dataArray[dataArray.length] = value;
	});
	 
	var columns = ["name", "total", "delta", "gender", "party", "age"];
	var columnNames = ["NAME", "DELTA", "GENDER", "TOTAL", "PARTY"]

	drawTable(dataArray, "#chart", { width: width, height: height }, columns);
}

function drawTable(data, tableid, dimensions, columns) {

	var ascending = true;

	var width = dimensions.width + "px";
	var height = dimensions.height + "px";
	var twidth = (dimensions.width - 25) + "px";
	var divHeight = (dimensions.height - 60) + "px";

	var tbody = d3.select(tableid).append("table").attr("width", width);
	// Create a row for each object in the data and perform an intial sort.
	var rows = tbody.selectAll("tr")
		.data(data).enter()
		.append("tr").sort(function(a,b){return a['total'] - b['total']})
		.attr("id", function(d){
			return d.name;
		});

	// Create a cell in each row for each column
	var cells = rows.selectAll("td")		
		.attr("id", function(d, i){
			return i;
		})	
		.data(function (d) {
			return columns.map(function (column) {
				return { column: column, data: d};
			});
		}).enter()
		.append("td")
		.html(function (d) {
			return tableElement(d);
		})
		.on("click", function (d) {
			drawPetition(d.data['name']);
		});

	//adds onclick even to each coumn image to sort the table
	for (var i = 0; i < columns.length; i++){
		document.getElementById(columns[i]).onclick = function (event) {
			d = event.target.id;
			//d = d.toLowerCase();
			ascending = !ascending;
			var sort = function(a, b){
				var value = (typeof a[d] == 'string') ? a[d].localeCompare(b[d]) : a[d] - b[d];
				return ((ascending) ? -1 : 1)*value;
			}
			var rows = tbody.selectAll("tr").sort(sort);
			hightlightColumn(d);
		};
	}

}

function tableElement(d){
	var tag = '<div class="' + d.column + ' ' + d.data.name.replace(/ /g, '') + ' tableElement">';
	return tag + d.data[d.column] + '</div>';
}

var oldRow = "nothing";
function highlightRow(row){
	$('.' + oldRow).css('background-color', '');
	oldRow = row.replace(/ /g, '');	
	console.log("highlight row called " + oldRow);
	highlight();
}

var oldColumn = "nothing";
function hightlightColumn(column){
	$('.' + oldColumn).css('background-color', '');
	oldColumn = column;
	highlight();
}

function highlight(){
	$('.' + oldRow).css('background-color', 'lightgrey');
	$('.' + oldColumn).css('background-color', 'lightgrey');
}