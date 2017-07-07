function loadDoc(page) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
//      document.getElementById("demo").innerHTML =
//      this.responseText;
      var responseText = JSON.parse(this.responseText);
      
      var innerHtml = '';
//      for(key in responseText){
//          console.log('key',key);
//          innerHtml += '<div id="' + key + '"></div>';
//      }
      //document.getElementById("chart").innerHTML = innerHtml;
      var gpositive=0, gnegative=0, gneutral=0, gobj = {}, obj;
      for(key in responseText){
          console.log('key',key,page);
          var positive=0, negative=0, neutral=0;
        for(var i=0; (key==page||page=="dashboard")&&i<responseText[key].length; i++)
        {
            obj = {};
          console.log(positive, negative, neutral);
            if(responseText[key][i].compound>0.5){
                positive++; gpositive++;}
            else if(responseText[key][i].compound<-0.5){
                negative++; gnegative++;}
            else{
                neutral++;  gneutral++;}
            
        obj.positive = positive;
        obj.negative = negative;
        obj.neutral = neutral;
        }
        gobj.positive = gpositive;
        gobj.negative = gnegative;
        gobj.neutral = gneutral;
        //createChart(key, obj)
    }
    if(page === 'dashboard'){
        createChart(page, gobj);
        stackedBar(page, responseText);
        
          }else{
        createChart(page, obj);
        neg_barChart(page, responseText);
    console.log(positive, negative, neutral);
          }
    }};
//    createBar("dashboard");
  xhttp.open("POST", "http://localhost:8084/DbAccessTrial/Dbacc", true);
  xhttp.send();
}
function createChart(site, obj) {
var w =250;
var h = 200; 
var r = h/2; 
var color = ["#87CEFA","#F08080","#DAA520"];
var data = [{"label":"positive", "value":obj.positive}, 
	{"label":"negative", "value":obj.negative}, 
        {"label":"neutral", "value":obj.neutral}];
    console.log(data, obj);
var vis = d3.select('#'+site).append("svg:svg").data([data]).attr("width", w).attr("height", h).append("svg:g").attr("transform", "translate(" + r + "," + r + ")");
var pie = d3.layout.pie().value(function(d){return d.value;});

// declare an arc generator function
var arc = d3.svg.arc().outerRadius(r);
var arcOver = d3.svg.arc()
        .outerRadius(r + 9);

// select paths, use arc generator to draw
var arcs = vis.selectAll("g.slice").data(pie).enter().append("svg:g").attr("class", "slice");
arcs.append("svg:path")
    .attr("fill", function(d, i){
        return color[i];
    })
    .attr("d", function (d) {
        // log the result of the arc generator to show how cool it is :)
        console.log(arc(d));
        return arc(d);
    })
    .on("mouseenter", function(d) {
            d3.select(this)
               .attr("stroke","white")
               .transition()
               .duration(1000)
               .attr("d", arcOver)             
               .attr("stroke-width",6);
        })
        .on("mouseleave", function(d) {
            d3.select(this).transition()            
               .attr("d", arc)
               .attr("stroke","none");
        });
        
    arcs    
    .on("mouseover", function (d) {
    d3.select("#tooltip")
        .style("left", d3.event.pageX + "px")
        .style("top", d3.event.pageY + "px")
        .style("opacity", 1)
        .select("#value")
        .text(d.value);
})
    .on("mouseout", function () {
    // Hide the tooltip
    d3.select("#tooltip")
        .style("opacity", 0);;
})
}
// Setup svg using Bostock's margin convention
function createBar(site, obj) {
    var siteid = site + '_bar';
var margin = {top: 20, right: 160, bottom: 35, left: 30};

var width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

var svg = d3.select("#"+siteid)
  .append("svg")
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom)
  .append("g")
  .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


/* Data in strings like it would be if imported from a csv */

var data = [
  { location: "x", compound: "-1"},
  { location: "y", compound: "-0.75"},
  { location: "z", compound: "-0.5"},
  { location: "a", compound: "-0.25"},
  { location: "b", compound: "0"},
  { location: "c", compound: "0.25"},
  { location: "d", compound: "0.5"},
  { location: "e", compound: "0.75"},
  { location: "f", compound: "1"}
];


// Transpose the data into layers
var dataset = d3.layout.stack()(["compound"].map(function(compound) {
  return data.map(function(d) {
    return {x:d.location, y:d.compound};
  });
}));


// Set x, y and colors
var x = d3.scale.ordinal()
  .domain(dataset[0].map(function(d) { return d.x; }))
  .rangeRoundBands([10, width-10], 0.02);

var y = d3.scale.linear()
  .domain([0, d3.max(dataset, function(d) {  return d3.max(d, function(d) { return d.y0 + d.y; });  })])
  .range([height, 0]);

var colors = ["#b33040", "#d25c4d", "#f2b447", "#d9d574"];


// Define and draw axes
var yAxis = d3.svg.axis()
  .scale(y)
  .orient("left")
  .ticks(5)
  .tickSize(-width, 0, 0)
  .tickFormat( function(d) { return d } );

var xAxis = d3.svg.axis()
  .scale(x)
  .orient("bottom")
  .tickFormat( function(d) { return d } );

svg.append("g")
  .attr("class", "y axis")
  .call(yAxis);

svg.append("g")
  .attr("class", "x axis")
  .attr("transform", "translate(0," + height + ")")
  .call(xAxis);


// Create groups for each series, rects for each segment 
var groups = svg.selectAll("g.cost")
  .data(dataset)
  .enter().append("g")
  .attr("class", "cost")
  .style("fill", function(d, i) { return colors[i]; });

var rect = groups.selectAll("rect")
  .data(function(d) { return d; })
  .enter()
  .append("rect")
  .attr("x", function(d) { return x(d.x); })
  .attr("y", function(d) { return y(Math.min(0, d.y)); })
  .attr("height", function(d) { return Math.abs(x(d.x)-x(0)); })
  .attr("width", x.rangeBand())
  .on("mouseover", function() { tooltip.style("display", null); })
  .on("mouseout", function() { tooltip.style("display", "none"); })
  .on("mousemove", function(d) {
    var xPosition = d3.mouse(this)[0] - 15;
    var yPosition = d3.mouse(this)[1] - 25;
    tooltip.attr("transform", "translate(" + xPosition + "," + yPosition + ")");
    tooltip.select("text").text(d.y);
  });


// Draw legend
var legend = svg.selectAll(".legend")
  .data(colors)
  .enter().append("g")
  .attr("class", "legend")
  .attr("transform", function(d, i) { return "translate(30," + i * 19 + ")"; });
 
legend.append("rect")
  .attr("x", width - 18)
  .attr("width", 18)
  .attr("height", 18)
  .style("fill", function(d, i) {return colors.slice().reverse()[i];});
 
// Prep the tooltip bits, initial display is hidden
var tooltip = svg.append("g")
  .attr("class", "tooltip")
  .style("display", "none");
    
tooltip.append("rect")
  .attr("width", 30)
  .attr("height", 20)
  .attr("fill", "white")
  .style("opacity", 0.5);

tooltip.append("text")
  .attr("x", 15)
  .attr("dy", "1.2em")
  .style("text-anchor", "middle")
  .attr("font-size", "12px")
  .attr("font-weight", "bold");
}

function stackedBar(site,responseText){
    // Setup svg using Bostock's margin convention

var margin = {top: 20, right: 160, bottom: 35, left: 30};

var width = 800 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

var svg = d3.select("#"+site+"_bar")
  .append("svg")
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom)
  .append("g")
  .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var data = [];
/* Data in strings like it would be if imported from a csv */
          var gpositive=0, gnegative=0, gneutral=0, gobj = {};
    for(key in responseText){
          console.log('key',key);
          var positive=0, negative=0, neutral=0, gobj = {};
        for(var i=0; i<responseText[key].length; i++)
        {
          console.log(positive, negative, neutral);
            if(responseText[key][i].compound>0.5){
                positive++; gpositive++;}
            else if(responseText[key][i].compound<-0.5){
                negative++; gnegative++;}
            else{
                neutral++;  gneutral++;}
            
        }
        
        gobj.positive = positive;
        gobj.negative = negative;
        gobj.neutral = neutral;
        gobj.site = key;
        data.push(gobj)
        //createChart(key, obj)
    }

console.log('data', data);

// Transpose the data into layers
var dataset = d3.layout.stack()(["positive", "negative", "neutral"].map(function(fruit) {
  return data.map(function(d) {
    return {x: d.site, y: +d[fruit]};
  });
}));


// Set x, y and colors
var x = d3.scale.ordinal()
  .domain(dataset[0].map(function(d) { return d.x; }))
  .rangeRoundBands([10, width-10], 0.02);

var y = d3.scale.linear()
  .domain([0, d3.max(dataset, function(d) {  return d3.max(d, function(d) { return d.y0 + d.y; });  })])
  .range([height, 0]);

var colors = ["#008080", "#DC143C", "#FFFF00"];


// Define and draw axes
var yAxis = d3.svg.axis()
  .scale(y)
  .orient("left")
  .ticks(5)
  .tickSize(-width, 0, 0)
  .tickFormat( function(d) { return d } );

var xAxis = d3.svg.axis()
  .scale(x)
  .orient("bottom")
  .tickFormat(function(d) { return d });

svg.append("g")
  .attr("class", "y axis")
  .call(yAxis);

svg.append("g")
  .attr("class", "x axis")
  .attr("transform", "translate(0," + height + ")")
  .call(xAxis);


// Create groups for each series, rects for each segment 
var groups = svg.selectAll("g.cost")
  .data(dataset)
  .enter().append("g")
  .attr("class", "cost")
  .style("fill", function(d, i) { return colors[i]; });

var rect = groups.selectAll("rect")
  .data(function(d) { return d; })
  .enter()
  .append("rect")
  .attr("x", function(d) { return x(d.x); })
  .attr("y", function(d) { return y(d.y0 + d.y); })
  .attr("height", function(d) { return y(d.y0) - y(d.y0 + d.y); })
  .attr("width", x.rangeBand())
  .on("mouseover", function() { tooltip.style("display", null); })
  .on("mouseout", function() { tooltip.style("display", "none"); })
  .on("mousemove", function(d) {
    var xPosition = d3.mouse(this)[0] - 15;
    var yPosition = d3.mouse(this)[1] - 25;
    tooltip.attr("transform", "translate(" + xPosition + "," + yPosition + ")");
    tooltip.select("text").text(d.y);
  });


// Draw legend
var legend = svg.selectAll(".legend")
  .data(colors)
  .enter().append("g")
  .attr("class", "legend")
  .attr("transform", function(d, i) { return "translate(30," + i * 19 + ")"; });
 
legend.append("rect")
  .attr("x", width - 18)
  .attr("width", 18)
  .attr("height", 18)
  .style("fill", function(d, i) {return colors.slice()[i];});
 
legend.append("text")
  .attr("x", width + 5)
  .attr("y", 9)
  .attr("dy", ".35em")
  .style("text-anchor", "start")
  .text(function(d, i) { 
    switch (i) {
      case 0: return "positive";
      case 1: return "negative";
      case 2: return "neutral";
    }
  });


// Prep the tooltip bits, initial display is hidden
var tooltip = svg.append("g")
  .attr("class", "tooltip")
  .style("display", "none");
    
tooltip.append("rect")
  .attr("width", 30)
  .attr("height", 20)
  .attr("fill", "white")
  .style("opacity", 0.5);

tooltip.append("text")
  .attr("x", 15)
  .attr("dy", "1.2em")
  .style("text-anchor", "middle")
  .attr("font-size", "12px")
  .attr("font-weight", "bold");

}

function neg_barChart(site, responseText){	

		//Set width and height as fixed variables
		var w = 520;
		var h = 500;
		var padding = 25;
var dataset=[]
    for(key in responseText){
          console.log('key',key);
          var positive=0, negative=0, neutral=0;
          for(var i=0; (key==site)&&i<responseText[key].length; i++)
          {
              if(site==="dermalogica")
               obj = {'dr_change': responseText[key][i].compound,'name': responseText[key][i].loc, 'bus_change':0};
   
                  else
            obj = {'dr_change': responseText[key][i].compound,'name': responseText[key][i].name, 'bus_change':0};
            
        dataset.push(obj)
          }
 
      }
      console.log(dataset)
	
		var yScale = d3.scale.linear()
						.domain(d3.extent(dataset, function(d){return d.dr_change;}))
						.range([w+padding,padding]);

		var xScale = d3.scale.ordinal()
						.domain(dataset.map(function(d){ return d.name;}))
						.rangeRoundBands([padding,h+padding],.5);

		//To format axis as a percent
		var formatPercent = d3.format("%1");

		//Create y axis
		var yAxis = d3.svg.axis().scale(yScale).orient("left").ticks(5).tickFormat(function(d) { return d });

		//Define key function
		var key = function(d){return d.name};

		//Define tooltip for hover-over info windows
		var div = d3.select("body").append("div")   
  							.attr("class", "tooltip")               
  							.style("opacity", 0);

		//Create svg element
		var svg = d3.select("#"+site+'_bar').append("svg")
				.attr("width", w).attr("height", h)
				.attr("id", "chart")
				.attr("viewBox", "0 0 "+w+ " "+h)
				.attr("preserveAspectRatio", "xMinYMin");
		
		//Resizing function to maintain aspect ratio (uses jquery)
		var aspect = w / h;
		var chart = $("#chart");
			$(window).on("resize", function() {
			    var targetWidth = $("body").width();
			   	
	    		if(targetWidth<w){
	    			chart.attr("width", targetWidth); 
	    			chart.attr("height", targetWidth / aspect); 			
	    		}
	    		else{
	    			chart.attr("width", w);  
	    			chart.attr("height", w / aspect);	
	    		}

			});


		//Initialize state of chart according to drop down menu
		var state = d3.selectAll("option");

		//Create barchart
		svg.selectAll("rect")
			.data(dataset, key)
			.enter()
		  	.append("rect")
		    .attr("class", function(d){return d.dr_change < 0 ? "negative" : "positive";})
		    .attr({
		    	x: function(d){
		    		return xScale(d.name);
		    	},
		    	y: function(d){
		    		return yScale(Math.max(0, d.dr_change)); 
		    	},
		    	width: xScale.rangeBand(),
		    	height: function(d){
		    		return Math.abs(yScale(d.dr_change) - yScale(0)); 
		    	}
		    })
		    .on('mouseover', function(d){
							d3.select(this)
							    .style("opacity", 0.2)
							    .style("stroke", "black")
					
					var info = div
							    .style("opacity", 1)
							    .style("left", (d3.event.pageX+10) + "px")
							    .style("top", (d3.event.pageY-30) + "px")
							    .text(d.name);

					if(state[0][0].selected){
						info.append("p")
							    .text(formatPercent(d.dr_change));

					}
					else if(state[0][1].selected){
						info.append("p")
							    .text(formatPercent(d.bus_change));
					}



						})
        				.on('mouseout', function(d){
        					d3.select(this)
							.style({'stroke-opacity':0.5,'stroke':'#a8a8a8'})
							.style("opacity",1);

							div
	    						.style("opacity", 0);
        				});

		//Add y-axis
		svg.append("g")
				.attr("class", "y axis")
				.attr("transform", "translate(40,0)")
				.call(yAxis);

		//Sort data when sort is checked
		d3.selectAll(".checkbox").
		on("change", function(){
			var x0 = xScale.domain(dataset.sort(sortChoice())
			.map(function(d){return d.name}))
			.copy();

			var transition = svg.transition().duration(750);
			var delay = function(d, i){return i*10;};

			transition.selectAll("rect")
			.delay(delay)
			.attr("x", function(d){return x0(d.name);});

		})

		//Function to sort data when sort box is checked
		function sortChoice(){
				var state = d3.selectAll("option");
				var sort = d3.selectAll(".checkbox");

				if(sort[0][0].checked && state[0][0].selected){
					var out = function(a,b){return b.dr_change - a.dr_change;}
					return out;
				}
				else if(sort[0][0].checked && state[0][1].selected){
					var out = function(a,b){return b.bus_change - a.bus_change;}
					return out;
				}
				else{
					var out = function(a,b){return d3.ascending(a.name, b.name);}
					return out;
				}
		};

		//Change data to correct values on input change
			d3.selectAll("select").
			on("change", function() {
			
				var value= this.value;

				if(value=="bus"){
					var x_value = function(d){return d.bus_change;};
					var color = function(d){return d.bus_change < 0 ? "negative" : "positive";};
					var y_value = function(d){
			    		return yScale(Math.max(0, d.bus_change)); 
			    	};
			    	var height_value = function(d){
			    		return Math.abs(yScale(d.bus_change) - yScale(0));
			    	};	
				}
				else if(value=="demand"){
					var x_value = function(d){return d.dr_change;};
					var color = function(d){return d.dr_change < 0 ? "negative" : "positive";};
					var y_value = function(d){
			    		return yScale(Math.max(0, d.dr_change)); 
			    	};
			    	var height_value = function(d){
			    		return Math.abs(yScale(d.dr_change) - yScale(0)); 
			    	};	
				}

				//Update y scale
				yScale.domain(d3.extent(dataset, x_value));

				//Update with correct data
				var rect = svg.selectAll("rect").data(dataset, key);
				rect.exit().remove();

				//Transition chart to new data
				rect
				.transition()
				.duration(2000)
				.ease("linear")
				.each("start", function(){
					d3.select(this)
					.attr("width", "0.2")
					.attr("class", color)
				})
				.attr({
			    	x: function(d){
			    		return xScale(d.name);
			    	},
			    	y: y_value,
			    	width: xScale.rangeBand(),
			    	height: height_value
							
				});

				//Update y-axis
				svg.select(".y.axis")
					.transition()
					.duration(1000)
					.ease("linear")
					.call(yAxis);
			});
		
	};


