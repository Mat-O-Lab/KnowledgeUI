// Copyright 2021 Observable, Inc.
// Released under the ISC license.
// https://observablehq.com/@d3/sunburst
function Sunburst(data, { // data is either tabular (array of objects) or hierarchy (nested objects)
    path, // as an alternative to id and parentId, returns an array identifier, imputing internal nodes
    id = Array.isArray(data) ? d => d.id : null, // if tabular data, given a d in data, returns a unique identifier (string)
    parentId = Array.isArray(data) ? d => d.parentId : null, // if tabular data, given a node d, returns its parent’s identifier
    children, // if hierarchical data, given a d in data, returns its children
    value, // given a node d, returns a quantitative value (for area encoding; null for count)
    sort = (a, b) => d3.descending(a.value, b.value), // how to sort nodes prior to layout
    label, // given a node d, returns the name to display on the rectangle
    title, // given a node d, returns its hover text
    link, // given a node d, its link (if any)
    linkTarget = "_blank", // the target attribute for links (if any)
    width = 640, // outer width, in pixels
    height = 400, // outer height, in pixels
    margin = 1, // shorthand for margins
    marginTop = margin, // top margin, in pixels
    marginRight = margin, // right margin, in pixels
    marginBottom = margin, // bottom margin, in pixels
    marginLeft = margin, // left margin, in pixels
    padding = 1, // separation between arcs
    radius = Math.min(width - marginLeft - marginRight, height - marginTop - marginBottom) / 2, // outer radius
    color = d3.interpolateRainbow, // color scheme, if any
    fill = "#ccc", // fill for arcs (if no color encoding)
    fillOpacity = 0.6, // fill opacity for arcs
} = {}) {

    // If id and parentId options are specified, or the path option, use d3.stratify
    // to convert tabular data to a hierarchy; otherwise we assume that the data is
    // specified as an object {children} with nested objects (a.k.a. the “flare.json”
    // format), and use d3.hierarchy.
    let root = path != null ? d3.stratify().path(path)(data)
        : id != null || parentId != null ? d3.stratify().id(id).parentId(parentId)(data)
            : d3.hierarchy(data, children);

    // Compute the values of internal nodes by aggregating from the leaves.
    value == null ? root.count() : root.sum(d => Math.max(0, value(d)));

    // Sort the leaves (typically by descending value for a pleasing layout).
    if (sort != null) root.sort(sort);

    // Compute the partition layout. Note polar coordinates: x is angle and y is radius.
    d3.partition().size([2 * Math.PI, radius])(root);

    // Construct a color scale.
    if (color != null) {
        color = d3.scaleSequential([0, 15], color).unknown(fill);
        root.children.forEach((child, i) => child.index = i*2);
    }

    // Construct an arc generator.
    const arc = d3.arc()
        .startAngle(d => d.x0)
        .endAngle(d => d.x1)
        .padAngle(d => Math.min((d.x1 - d.x0) / 2, 2 * padding / radius))
        .padRadius(radius / 2)
        .innerRadius(d => d.y0)
        .outerRadius(d => d.y1 - padding);

    const svg = d3.create("svg")
        .attr("viewBox", [
            marginRight - marginLeft - width / 2,
            marginBottom - marginTop - height / 2,
            width,
            height
        ])
        .attr("width", width)
        .attr("height", height)
        .attr("style", "max-width: 100%; height: auto; height: intrinsic;")
        .attr("font-family", "sans-serif")
        .attr("font-size", 10)
        .attr("text-anchor", "middle");

    const cell = svg
        .selectAll("a")
        .data(root.descendants())
        .join("a")
        .attr("xlink:href", link == null ? null : d => link(d.data, d))
        .attr("target", link == null ? null : linkTarget);

    cell.append("path")
        .attr("d", arc)
        .attr("fill", color ? d => color(d.ancestors().reverse()[1]?.index + d.ancestors().length) : fill)
        .attr("fill-opacity", fillOpacity);

    if (label != null) cell
        .filter(d => (d.y0 + d.y1) / 2 * (d.x1 - d.x0) > 10)
        .append("text")
        .attr("transform", d => {
            if (!d.depth) return;
            const x = (d.x0 + d.x1) / 2 * 180 / Math.PI;
            const y = (d.y0 + d.y1) / 2;
            return `rotate(${x - 90}) translate(${y},0) rotate(${x < 180 ? 0 : 180})`;
        })
        .attr("dy", "0.32em")
        .text(d => label(d.data, d));

    if (title != null) cell.append("title")
        .text(d => title(d.data, d));

    return svg.node();
}

function updateSunburst(data, { // data is either tabular (array of objects) or hierarchy (nested objects)
    path, // as an alternative to id and parentId, returns an array identifier, imputing internal nodes
    id = Array.isArray(data) ? d => d.id : null, // if tabular data, given a d in data, returns a unique identifier (string)
    parentId = Array.isArray(data) ? d => d.parentId : null, // if tabular data, given a node d, returns its parent’s identifier
    children, // if hierarchical data, given a d in data, returns its children
    value, // given a node d, returns a quantitative value (for area encoding; null for count)
    sort = (a, b) => d3.descending(a.value, b.value), // how to sort nodes prior to layout
    label, // given a node d, returns the name to display on the rectangle
    title, // given a node d, returns its hover texte
    link, // given a node d, its link (if any)
    linkTarget = "_blank", // the target attribute for links (if any)
    width = 640, // outer width, in pixels
    height = 400, // outer height, in pixels
    margin = 1, // shorthand for margins
    marginTop = margin, // top margin, in pixels
    marginRight = margin, // right margin, in pixels
    marginBottom = margin, // bottom margin, in pixels
    marginLeft = margin, // left margin, in pixels
    padding = 1, // separation between arcs
    radius = Math.min(width - marginLeft - marginRight, height - marginTop - marginBottom) / 2, // outer radius
    color = d3.interpolateRainbow, // color scheme, if any
    fill = "#ccc", // fill for arcs (if no color encoding)
    fillOpacity = 0.6, // fill opacity for arcs
} = {}) {
     // If id and parentId options are specified, or the path option, use d3.stratify
    // to convert tabular data to a hierarchy; otherwise we assume that the data is
    // specified as an object {children} with nested objects (a.k.a. the “flare.json”
    // format), and use d3.hierarchy.
    let root = path != null ? d3.stratify().path(path)(data)
        : id != null || parentId != null ? d3.stratify().id(id).parentId(parentId)(data)
            : d3.hierarchy(data, children);

    // Compute the values of internal nodes by aggregating from the leaves.
    value == null ? root.count() : root.sum(d => Math.max(0, value(d)));

    // Sort the leaves (typically by descending value for a pleasing layout).
    if (sort != null) root.sort(sort);

    // Compute the partition layout. Note polar coordinates: x is angle and y is radius.
    d3.partition().size([2 * Math.PI, radius])(root);

    // Construct a color scale.
    if (color != null) {
        color = d3.scaleSequential([0, 15], color).unknown(fill);
        root.children.forEach((child, i) => child.index = i*2);
    }

    const arc = d3.arc()
        .startAngle(d => d.x0)
        .endAngle(d => d.x1)
        .padAngle(d => Math.min((d.x1 - d.x0) / 2, 2 * padding / radius))
        .padRadius(radius / 2)
        .innerRadius(d => d.y0)
        .outerRadius(d => d.y1 - padding);

    const svg = d3.select("svg")
    svg.selectAll('*').remove()
    
    const cell = svg
        .selectAll("a")
        .data(root.descendants())
        .join("a")
        .attr("xlink:href", link == null ? null : d => link(d.data, d))
        .attr("target", link == null ? null : linkTarget);

    cell.append("path")
        .attr("d", arc)
        .attr("fill", color ? d => color(d.ancestors().reverse()[1]?.index + d.ancestors().length) : fill)
        .attr("fill-opacity", fillOpacity);

    if (label != null) cell
        .filter(d => (d.y0 + d.y1) / 2 * (d.x1 - d.x0) > 10)
        .append("text")
        .attr("transform", d => {
            if (!d.depth) return;
            const x = (d.x0 + d.x1) / 2 * 180 / Math.PI;
            const y = (d.y0 + d.y1) / 2;
            return `rotate(${x - 90}) translate(${y},0) rotate(${x < 180 ? 0 : 180})`;
        })
        .attr("dy", "0.32em")
        .text(d => label(d.data, d));

    if (title != null) cell.append("title")
        .text(d => title(d.data, d));


}

async function getNodeData(endpoint) {
    var query = `
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?c (MIN(?label) AS ?label1) ?superclass (count(?x) as ?count) WHERE {
                ?x a ?c.
                OPTIONAL {?c rdfs:label ?label} .
                ?c rdfs:subClassOf ?superclass.
                filter (?c != ?superclass &&
                        !exists {?c rdfs:subClassOf ?othersuper. ?othersuper rdfs:subClassOf ?superclass.
                                filter(?c != ?othersuper && ?othersuper != ?superclass)})
            } group by ?c ?label1 ?superclass HAVING(?count > 1) order by desc(?count)
            `


  //return $.get(endpoint, {query}, d => d, "text/csv")
  return $.ajax({
    url: endpoint,
    type: 'GET',
    data: {query},
    crossDomain: true,
    dataType : 'jsonp'
  })
}

function difference(setA, setB) {
    const _difference = new Set(setA);
    for (const elem of setB) {
      _difference.delete(elem);
    }
    return _difference;
  }

function parseNodeData(jsonp_result) {
    var n = []
    jsonp_result.results.bindings.forEach((e) => n.push({
        c: e.c.value,
        count: e.count.value,
        label1: e.label1?.value? e.c.value : '',
        superclass: e.superclass.value
    }))
    n.columns = jsonp_result.head.vars
    return n
}

function parseNodeDataReverse(jsonp_result) {
    let n = {}
    let parents = new Set()
    let elements = new Set()
    jsonp_result.results.bindings.forEach((e) => {

        // note all encountered parents and nodes to later find all parents that aren't also nodes
        parents.add(e.superclass.value)
        elements.add(e.c.value)
        if (n[e.superclass.value] === undefined) {
            n[e.superclass.value] = [{
                    c: e.c.value,
                    count: e.count.value,
                    label1: e.label1?.value ? e.label1.value : e.c.value,
                }]
        } else {
            n[e.superclass.value].push({
                c: e.c.value,
                count: e.count.value,
                label1: e.label1?.value ? e.label1.value : e.c.value,
            })
        }
    })

    //n.columns = jsonp_result.head.vars
    return {nodes: n, roots: Array.from(difference(parents, elements))}
}

function makeHierarchy(node, reverseDict) {
    let d = {'label1': node.label1, 'c': node.c}
    if (reverseDict[node['c']] !== undefined) {
        d.children = []
        reverseDict[node['c']].forEach((e) => d.children.push(makeHierarchy(e, reverseDict)))
    } else {
        d.count = node.count
    }
    return d
}

