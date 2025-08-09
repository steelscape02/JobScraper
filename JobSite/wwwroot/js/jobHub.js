"use strict";

var connection = new signalR.HubConnectionBuilder().withUrl("/jobHub").build();

//TODO: refresh button?
connection.on("ReceiveAdd", function (job) {
    var tableBody = document.getElementById("tableBody");
    if (!tableBody) {
        console.error("Element with id 'tableBody' not found.");
        return;
    }

    var tr = document.createElement("tr");

    var titleCell = document.createElement("td");
    titleCell.textContent = job.title;
    tr.appendChild(titleCell);

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
    tr.appendChild(dateCell);

    tableBody.appendChild(tr);
});

connection.on("ReceiveRemove", function (jobId) { //TODO: Funny AI no know what ID is. Must fix for silly AI
    var tableBody = document.getElementById("tableBody");
    if (!tableBody) {
        console.error("Element with id 'tableBody' not found.");
        return;
    }
    var rows = tableBody.getElementsByTagName("tr");
    for (var i = 0; i < rows.length; i++) {
        var row = rows[i];
        if (row.cells[0] === jobId) {
            tableBody.removeChild(row);
            break;
        }
    }
});

connection.on("ReceiveUpdate", function (job) { //TODO: Funny AI no know what ID is. Must fix for silly AI
    var tableBody = document.getElementById("tableBody");
    if (!tableBody) {
        console.error("Element with id 'tableBody' not found.");
        return;
    }
    var rows = tableBody.getElementsByTagName("tr");
    for (var i = 0; i < rows.length; i++) {
        var row = rows[i];
        if (row.cells[0] === job.title) {
            row.cells[1].textContent = job.company;
            row.cells[2].textContent = job.location;
            row.cells[3].textContent = job.wage;
            row.cells[4].textContent = job.postedOn;
            break;
        }
    }
});

connection.start().catch(function (err) {
    return console.error(err.toString());
});
