function draw_graph_from_xml(xml, canvas) {
    var xmldoc = xml.responseXML;
    var vertices = xmldoc.getElementsByTagName("vertex");
    var n = vertices.length;
    
    // create a hashmap from vertex names (nodevalues) to coordinates
    let vertex_coords = {};
    
    for (i = 0; i < n; i ++) {
        var vertex_name = vertices[i].childNodes[0].nodeValue;
        var coords = vertices[i].getElementsByTagName("coordinate")[0].childNodes[0].nodeValue;
        var xpos = parse_coordinate(coords, 0);
        var ypos = parse_coordinate(coords, 1);
        
        draw_dot(canvas, xpos, ypos, 10);
        vertex_coords[vertex_name] = [xpos, ypos];
    }
    
    for (i = 0; i < n; i ++) {
        var vertex_name = vertices[i].childNodes[0].nodeValue;
        var xpos1 = vertex_coords[vertex_name][0];
        var ypos1 = vertex_coords[vertex_name][1];
        
        var neighbours = vertices[i].getElementsByTagName("neighbour");
        var n2 = neighbours.length;
        console.log(n2);
        
        for (j = 0; j < n2; j++) {
            var neighbour_name = neighbours[j].childNodes[0].nodeValue;
            var xpos2 = vertex_coords[neighbour_name][0];
            var ypos2 = vertex_coords[neighbour_name][1];
            
            draw_path(canvas, xpos1, ypos1, xpos2, ypos2);
        }
    }
    
}


function load_xml_doc(directory, canvas) {
    var xhttp = new XMLHttpRequest();
    
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            draw_graph_from_xml(this, canvas);
        }
    };
    
    xhttp.open("GET", directory, true);
    xhttp.send();
    
}


function draw_path(canvas, x1, y1, x2, y2) {
    canvas.moveTo(x1, y1);
    canvas.lineTo(x2, y2);
    canvas.stroke();
}


function draw_dot(canvas, x, y, radius) {
    canvas.beginPath();
    canvas.arc(x, y, radius, 0, 2 * Math.PI, false);
    canvas.fill();
}


function parse_coordinate(string, pos){
    // returns the coordinate value at pos in the string
    // string should be a bracketed coordinate format e.g. (1, 2)
    var newstring = string.replace("(", "").replace(")", "");
    var arr = newstring.split(", ");
    return parseFloat(arr[pos]);
    
}