"use strict";

const delay = ms => new Promise(res => setTimeout(res, ms));

const connection = new signalR.HubConnectionBuilder()
    .withUrl("/jobHub")
    .configureLogging(signalR.LogLevel.Information)
    .withAutomaticReconnect()
    .build();


//TODO: refresh button?
connection.on("ReceiveAdd", function (job) {
    var tableBody = document.getElementById("tableBody");
    if (!tableBody) {
        console.error("Element with id 'tableBody' not found.");
        return;
    }

    var tr = document.createElement("tr");

    tr.setAttribute("id", job.id); 

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
            row.cells[0].textContent = job.title;
            row.cells[1].textContent = job.company;
            row.cells[2].textContent = job.location;
            row.cells[3].textContent = job.wage;
            row.cells[4].textContent = job.postedOn;
            break;
        }
    }
});

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