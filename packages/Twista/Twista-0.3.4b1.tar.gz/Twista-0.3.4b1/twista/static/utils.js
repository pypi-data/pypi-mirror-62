
function loadJson(url, params, callback) {
    var xmlhttp = new XMLHttpRequest();

    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            callback(JSON.parse(this.responseText));
        }
    };
    xmlhttp.open("GET", url + "?" + buildURLQuery(params), true);
    xmlhttp.send();
}

function loadText(url, params, callback) {
    var xmlhttp = new XMLHttpRequest();

    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            callback(this.responseText);
            refreshFilter();
        }
    };
    xmlhttp.open("GET", url + "?" + buildURLQuery(params), true);
    xmlhttp.send();
}

function buildURLQuery(map) {
    return Object.entries(map)
                 .map(pair => pair.map(encodeURIComponent).join('='))
                 .join('&');
}

function plot(into, data) {
    into.querySelector('.mdl-spinner').remove();
    var div = document.createElement('div');
    into.prepend(div);
    Plotly.newPlot(div, data, { }, { 
        'responsive': true 
    });
}

function observeFilter() {
    document.querySelector("#filter #begin").value = localStorage.getItem("begin") || "";
    document.querySelector("#filter #end").value = localStorage.getItem("end") || "";
    document.querySelectorAll("#filter #begin, #filter #end").forEach(e => e.addEventListener('change', () => {
        localStorage.setItem('begin', document.querySelector("#filter #begin").value || "");
        localStorage.setItem('end', document.querySelector("#filter #end").value || "");
        refreshFilter();
    }));
}

function refreshFilter() {
    document.querySelectorAll("a.filtered").forEach(link => {
        const url = new URL(link.getAttribute('href'), window.location.origin)
        url.searchParams.set('begin', localStorage.getItem("begin") || "");
        url.searchParams.set('end', localStorage.getItem("end") || "");
        link.setAttribute('href', url.href);
    });
}

function plotRetweetNetwork(network, container, inspect) {
    console.log("plotting into " + container);
    var base_color = '#66CCFF';
    var highlight_outgoing = '#FF4081';
    var highlight_incoming = 'blue';
    var cy = cytoscape({
        container: container,
        layout: { name: 'random' },
        style: [
            {
                selector: 'node',
                style: {
                    'background-color': base_color,
                    'opacity': 0.5,
                }
            },
            {
                selector: 'node[select = "start"]',
                style: {
                    'content': 'data(screen_name)',
                    'color': highlight_outgoing,
                    'font-size': 24,
                    'background-color': highlight_outgoing,
                }
            },
            {
                selector: 'node.current',
                style: {
                    'content': 'data(screen_name)',
                    'color': highlight_incoming
                }
            },
            {
                selector: 'edge',
                style: {
                    'width': 'data(qty)',
                    'line-color': base_color,
                    'curve-style': 'bezier',
                    'target-arrow-shape': 'triangle',
                    'target-arrow-color': base_color, 
                    'opacity': 0.25
                }
            },
            {
                selector: '.outgoing',
                style: {
                    'background-color': highlight_outgoing,
                    'line-color': highlight_outgoing,
                    'target-arrow-color': highlight_outgoing
                }
            },
            {
                selector: '.incoming, .current',
                style: {
                    'width': 100,
                    'background-color': highlight_incoming,
                    'line-color': highlight_incoming,
                    'target-arrow-color': highlight_incoming,
                    'line-style': 'dashed',
                    'opacity': 1.0
                }
            }
        ],

        elements: network
    });



    const maxSize = Math.max(...cy.elements('node').map(n => n.indegree(false) + 2 * n.outdegree(false)));
    const maxQty = Math.max(...cy.elements('edge').map(e => e.data('qty')));
    cy.elements('node').forEach(n => n.css({
        'width': 50 * (n.indegree(false) + 2 * n.outdegree(false)) / maxSize,
        'height': 50 * (n.indegree(false) + 2 * n.outdegree(false)) / maxSize
    }));

    cy.elements('edge').forEach(e => e.css({'width': Math.max(1, 10 * e.data('qty') / maxQty)}));

    console.log("layouting")
    cy.layout({
        name: 'cose',
        animate: true,
        delayAnimation: 250,
        randomize: true,
        fit: true,
        edgeElasticity: edge => edge.data('qty') * 32,
        nodeRepulsion: node => node.degree() * 2048,
    }).run()
    console.log("layouting finished")

    console.log("registering event handlers")
    cy.on('mouseover', 'edge', ev => ev.target.toggleClass('current'));
    cy.on('mouseout', 'edge', ev => ev.target.toggleClass('current'));
    cy.on('click', 'edge', ev => {
        loadText("/retweets/", {
                'source': ev.target.source().id(),
                'target': ev.target.target().id(), 
                'begin': localStorage.getItem('begin'), 
                'end': localStorage.getItem('end')
            }, 
            response => inspect.innerHTML = response
        );
    });

    cy.on('mouseover', 'node', ev => {
        ev.target.outgoers().forEach(e => e.toggleClass('outgoing'));
        ev.target.toggleClass('current');
        cy.elements()
            .aStar({ root: "[select = 'start']", goal: ev.target, directed: true })
            .path.forEach(e => e.toggleClass('incoming'));
    });
    cy.on('mouseout', 'node', ev => {
        ev.target.outgoers().forEach(e => e.toggleClass('outgoing'));
        ev.target.toggleClass('current');
        cy.elements()
            .aStar({ root: "[select = 'start']", goal: ev.target, directed: true })
            .path.forEach(e => e.toggleClass('incoming'));
    });
    cy.on('click', 'node', ev => {
        loadText("/user/" + ev.target.id() + "/info", { 
                'begin': localStorage.getItem('begin'), 
                'end': localStorage.getItem('end')
            }, 
            response => inspect.innerHTML = response
        );
    });
    console.log("finished");
}