$(function () {
	'use strict'
	
			// set the dimensions and margins of the graph
		var width = 445,
			height = 445;

		// append the svg object to the body of the page
		var svg = d3.select("#status-treemap")
		.append("svg")
			.attr("width", width)
			.attr("height", height);



		// var colors = d3.scaleOrdinal(["var(--maroon)", "var(--gold"], "var(--sea-blue)", "var(--aqua-green)", "var(--light-gray)")

		// read json data
		d3.json("data/items-by-status.json", function(data) {

			// Give the data to this cluster layout:
			var root = d3.hierarchy(data).sum(function(d){ return d.value}) // Here the size of each leaf is given in the 'value' field in input data

			// Then d3.treemap computes the position of each element of the hierarchy
			d3.treemap()
				.size([width, height])
				.padding(2)
				(root)

			var ionaColor = d3.scaleOrdinal()
				.domain(["Complete", "Incomplete", "Review", "Reviewed", "Estimated Remaining"])
				.range(["var(--maroon)", "var(--gold)", "var(--sea-blue)", "var(--aqua-green)", "var(--medium-gray)"])

			//remove all leaves that have value less than 1 (aka statuses not currently in use)
			//and set to Iona Colors
			var pruned = root.leaves().filter( function (d) { return ( d.value > 0 )})

			// use this information to add rectangles:
			svg
			.selectAll("rect")
			.data(pruned)
			.enter()
			.append("rect")
				.attr('x', function (d) { return d.x0; })
				.attr('y', function (d) { return d.y0; })
				.attr('width', function (d) { return d.x1 - d.x0; })
				.attr('height', function (d) { return d.y1 - d.y0; })
				.style("fill", function (d) { return ionaColor(d.data.name) } )

			// and to add the text labels
			svg
			.selectAll("text")
			.data(pruned)
			.enter()
			.append("text")
				.attr("x", function(d){ return d.x0+5})	  // +10 to adjust position (more right)
				.attr("y", function(d){ return d.y0+50})	  // +20 to adjust position (lower)
				.text(function(d){ return d.data.name + " (" + d.data.value + ")" })
				.attr("font-size", "15px")
				.attr("fill", "white")
		});
});