"use strict";

const connection = new signalR.HubConnectionBuilder()
    .withUrl("/jobHub")
    .configureLogging(signalR.LogLevel.Information)
    .withAutomaticReconnect()
    .build();

var minDate = Infinity;
var maxDate = -Infinity;
//TODO: refresh button?
connection.on("ReceiveAdd", function (job) {
    var tableBody = document.getElementById("tableBody");
    if (!tableBody) {
        console.error("Element with id 'tableBody' not found.");
        return;
    }

    var tr = document.createElement("tr");

    tr.setAttribute("id", job.id); 

    const link = document.createElement('a');
    link.href = job.url;
    link.textContent = job.title;
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    tr.appendChild(link);

    var companyCell = document.createElement("td");
    companyCell.textContent = job.company;
    tr.appendChild(companyCell);

    var locationCell = document.createElement("td");
    locationCell.textContent = job.location;
    tr.appendChild(locationCell);

    var wageCell = document.createElement("td");
    wageCell.textContent = job.wage;
    tr.appendChild(wageCell);

    var dateCell = document.createElement("td");
    dateCell.textContent = job.postedOn;
    dateCell.id = job.postedOnRaw;
    tr.appendChild(dateCell);
    minDate = Math.min(minDate, job.postedOnRaw);
    maxDate = Math.max(maxDate, job.postedOnRaw);

    tableBody.appendChild(tr);
});

connection.on("ReceiveRemove", function (jobId) {
    var tableBody = document.getElementById("tableBody");
    if (!tableBody) {
        console.error("Element with id 'tableBody' not found.");
        return;
    }
    var rows = tableBody.getElementsByTagName("tr");
    var removedTEST = false;
    console.log("elem to remove: " + jobId);
    for (var i = 0; i < rows.length; i++) {
        var row = rows[i]
        console.log("row id: " + row.id);
        if (row.id === jobId) {
            removedTEST = true;
            tableBody.removeChild(row);
            break;
        }
    }
    console.log("removedTEST: " + removedTEST);
});

connection.on("ReceiveUpdate", function (job) {
    var tableBody = document.getElementById("tableBody");
    if (!tableBody) {
        console.error("Element with id 'tableBody' not found.");
        return;
    }
    var rows = tableBody.getElementsByTagName("tr");
    for (var i = 0; i < rows.length; i++) {
        var row = rows[i]
        if (row.id === job.id) {
            const link = document.createElement('a');
            link.href = job.url;
            link.textContent = job.title;
            link.target = "_blank";
            link.rel = "noopener noreferrer";
            row.cells[0].appendChild(link);
            row.cells[1].textContent = job.company;
            row.cells[2].textContent = job.location;
            row.cells[3].textContent = job.wage;
            row.cells[4].textContent = job.postedOn;
            row.cells[4].id          = job.postedOnRaw;
            break;
        }
    }
});

function sortTableDown() {
    var table, rows, cont, i, x, y, shouldSwitch;
    table = document.getElementById("tableBody");
    cont = true;
    while (cont) {
        cont = false;
        rows = table.rows;
        for (i = 1; i < (rows.length - 1); i++) {
            shouldSwitch = false;
            x = rows[i][4].id;
            y = rows[i + 1][4].id;
            if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                shouldSwitch = true;
                break;
            }
        }
        if (shouldSwitch) {
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            cont = true;
        }
    }
}

function sortTableUp() {
    var table, rows, cont, i, x, y, shouldSwitch;
    table = document.getElementById("myTable");
    cont = true;
    while (cont) {
        cont = false;
        rows = table.rows;
        for (i = 1; i < (rows.length - 1); i++) {
            shouldSwitch = false;
            x = rows[i][4].id;
            y = rows[i+1][4].id;
            if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                shouldSwitch = true;
                break;
            }
        }
        if (shouldSwitch) {
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            cont = true;
        }
    }
}

async function start() {
    try {
        connection.serverTimeoutInMilliseconds = 120000; // 2 minutes
        await connection.start()
        console.log(Date.now());
    } catch (err) {
        console.log(err);
        setTimeout(start, 10000);
    }
};

connection.onclose(async () => {
    await start();
});

start();