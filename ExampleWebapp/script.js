function server_run_page_script() {
    // commands server to execute script.py at current directory
    
    var xhttp = new XMLHttpRequest();
    body = JSON.stringify({
        request_type: 'run_page_script'
    });
    
    xhttp.open('POST', '', true);
    xhttp.send(body);
}

function insert_sidenav(root_directory) {
    // requests sidenav html and inserts into document
    
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            
            var doc = this.responseText;
            var sidebar = document.createElement('div');
            sidebar.innerHTML = doc;
            sidebar.className = 'sidenav';
            document.body.appendChild(sidebar);
        }
    };
    
    xhttp.open('GET', root_directory + 'sidenav.html', true);
    xhttp.send();
}


function test_post() {
    // performs a test post request
    
    var xhttp = new XMLHttpRequest();
    var body = JSON.stringify({
        request_type: "test"
    });
    
    xhttp.open("POST", "/", true);
    xhttp.send(body);
}


function randgraph_request(int_n, float_p, path) {
    // commands server to create XML data for a random graph with parameters n, p
    // saves file to path
    
    var xhttp = new XMLHttpRequest();
    var body = JSON.stringify({
        request_type: 'random_graph_generation',
        n: int_n,
        p: float_p
    });
    
    xhttp.open('POST', path, true);
    xhttp.send(body);
}


function nearest_xy_vertex(x, y, graph_path, ready_action) {
    // commands server to find nearest vertex in a coordinate graph (XML at path) to (x, y)
    // server responds with vertex name and performs the function ready_action
    
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = ready_action;
    xhttp.responseType = 'text';
    
    var body = JSON.stringify ({
        request_type: 'nearest_xy_vertex',
        graph_path: graph_path,
        x: x,
        y: y
    });
    
    xhttp.open('POST', '', true);
    xhttp.send(body);
}

function shortest_path(v1, v2, graph_path, ready_action) {
    // commands server to find shortest path in a graph (XML at path) from v1 to v2
    // server responds with a JSON list of vertex names in path order
    
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = ready_action;
    xhttp.responseType = 'text';
    
    var body = JSON.stringify ({
        request_type: 'shortest_path',
        graph_path: graph_path,
        v1: v1,
        v2: v2
    });
    
    xhttp.open('POST', '', true);
    xhttp.send(body);
}


function draw_graph_from_xml(xml, canvas) {
    // given an XML coordinate graph, draws graph to canvas
    
    var xmldoc = xml.responseXML;
    var vertices = xmldoc.getElementsByTagName("vertex");
    var n = vertices.length;
    
    // create a hashmap from vertex names (nodevalues) to coordinates
    var vertex_coords = {};
    
    for (var i = 0; i < n; i ++) {
        var vertex_name = vertices[i].childNodes[0].nodeValue;
        var coords = vertices[i].getElementsByTagName("coordinate")[0].childNodes[0].nodeValue;
        var xpos = parse_coordinate(coords, 0);
        var ypos = parse_coordinate(coords, 1);
        
        draw_dot(canvas, xpos, ypos, 10);
        vertex_coords[vertex_name] = [xpos, ypos];
    }
    
    // use hashmap to draw vertices and edges
    for (i = 0; i < n; i ++) {
        var vertex_name = vertices[i].childNodes[0].nodeValue;
        var xpos1 = vertex_coords[vertex_name][0];
        var ypos1 = vertex_coords[vertex_name][1];
        
        var neighbours = vertices[i].getElementsByTagName("neighbour");
        var n2 = neighbours.length;
        
        for (var j = 0; j < n2; j++) {
            var neighbour_name = neighbours[j].childNodes[0].nodeValue;
            var xpos2 = vertex_coords[neighbour_name][0];
            var ypos2 = vertex_coords[neighbour_name][1];
            
            draw_path(canvas, xpos1, ypos1, xpos2, ypos2);
        }
    }
    
}

function add_edge(v1, v2, directory) {
    var xhttp = new XMLHttpRequest();
    var body = JSON.stringify({
        request_type: "add_edge",
        graph_path: directory,
        v1: v1,
        v2: v2
    });
    
    xhttp.open("POST", "", true);
    xhttp.send(body);
}


function load_coordinates_to_object(xml, object) {
    // given a coordinate graph XML, stores a coordinate hashmap to object
    
    var xmldoc = xml.responseXML;
    var vertices = xmldoc.getElementsByTagName("vertex");
    var n = vertices.length;
    
    for (var i = 0; i < n; i ++) {
        var vertex_name = vertices[i].childNodes[0].nodeValue;
        var coords = vertices[i].getElementsByTagName("coordinate")[0].childNodes[0].nodeValue;
        var xpos = parse_coordinate(coords, 0);
        var ypos = parse_coordinate(coords, 1);
        
        object[vertex_name] = [xpos, ypos];
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


function is_connected(graph_path, ready_action) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = ready_action;
    
    var body = JSON.stringify({
        request_type: 'is_connected',
        graph_path: graph_path
    });
    
    xhttp.open('POST', '', true);
    xhttp.send(body);
}


function load_graph_coordinates(directory, coord_object) {
    // requests xml data from directory and stores coordinate hashmap to coord_object upon completion
    
    var xhttp = new XMLHttpRequest();
    
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            load_coordinates_to_object(this, coord_object);
        }
    }
    
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