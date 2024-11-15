$(function () {
  "use strict";

  // set the dimensions and margins of the graph; width should fill the containing div
  const width = document.getElementById("status-treemap").clientWidth;
  const height = 445;

  const svg = d3
    .select("#status-treemap")
    .append("svg")
    .attr("width", width)
    .attr("height", height);

  // read data
  d3.json("data/items-by-status.json", function (data) {
    // Give the data to this cluster layout:
    const root = d3.hierarchy(data).sum(function (d) {
      return d.value;
    }); // Here the size of each leaf is given in the 'value' field in input data

    // Then d3.treemap computes the position of each element of the hierarchy
    d3.treemap().size([width, height]).padding(2)(root);

    const ionaColor = d3
      .scaleOrdinal()
      .domain([
        "Complete",
        "Incomplete",
        "Review",
        "Reviewed",
        "Estimated Remaining",
      ])
      .range([
        "var(--maroon)",
        "var(--gold)",
        "var(--sea-blue)",
        "var(--aqua-green)",
        "var(--medium-gray)",
      ]);

    //remove all leaves that have value less than 1 (aka statuses not currently in use)
    //and set to Iona Colors
    const pruned = root.leaves().filter((d) => d.value > 0);

    // use this information to add rectangles:
    svg
      .selectAll("rect")
      .data(pruned)
      .enter()
      .append("rect")
      .attr("x", (d) => d.x0)
      .attr("y", (d) => d.y0)
      .attr("width", (d) => d.x1 - d.x0)
      .attr("height", (d) => d.y1 - d.y0)
      .style("fill", (d) => ionaColor(d.data.name));

    // and to add the text labels
    svg
      .selectAll("text")
      .data(pruned)
      .enter()
      .append("text")
      .attr("x", (d) => d.x0 + 5) // +5 to adjust position (more right)
      .attr("y", (d) => d.y0 + 50) // +50 to adjust position (lower)
      .text((d) => `${d.data.name} (${d.data.value})`)
      .attr("font-size", "15px")
      .attr("fill", "white");
  });
});
