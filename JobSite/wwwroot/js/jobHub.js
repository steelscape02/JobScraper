"use strict";

const SORT_TYPE = {
    STR: "STR",
    DATE: "DATE",
    WAGE: "WAGE"
};

const connection = new signalR.HubConnectionBuilder()
    .withUrl("/jobHub")
    .configureLogging(signalR.LogLevel.Information)
    .withAutomaticReconnect()
    .build();

var minDate = Infinity;
var maxDate = -Infinity;
var minWage = Infinity;
var maxWage = -Infinity;
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
    wageCell.id = job.wageRaw;
    tr.appendChild(wageCell);
    minWage = Math.min(minWage, job.wageRaw);
    maxWage = Math.max(maxWage, job.wageRaw);

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
            row.cells[3].id          = job.wageRaw;
            minWage                  = Math.min(minWage, job.wageRaw);
            maxWage                  = Math.max(maxWage, job.wageRaw);
            row.cells[4].textContent = job.postedOn;
            row.cells[4].id          = job.postedOnRaw;
            minDate                  = Math.min(minDate, job.postedOnRaw);
            maxDate                  = Math.max(maxDate, job.postedOnRaw);
            break;
        }
    }
});

document.addEventListener('DOMContentLoaded', function () {
    /* Filter Type (FType) States
    
    0 - None
    1 - Ascending
    2 - Descending
    */

    var titleFType = 0;
    var companyFType = 0;
    var locationFType = 0; //TODO: Location API not implemented
    var wageFType = 0;
    var postedFType = 0;


    if (titleFilter) { //Col 0
        titleFilter.addEventListener('click', function (e) {
            //increment type or reset
            if (titleFType >= 2) {
                titleFType = 0;
            }
            titleFType += 1;
            console.log(titleFType)
            //evaluate sorting action
            switch (titleFType) {
                case 1:
                    sortTableUp(0,SORT_TYPE.STR);
                    break;
                case 2:
                    sortTableDown(0,SORT_TYPE.STR);
                    break;
                default:
                    console.error("titleFType - Invalid Value Reached" + titleFType);
                    break;
            }
        });
    } else {
        console.log("error state reached for titleFilter");
    }
    if (companyFilter) { //Col 1
        companyFilter.addEventListener('click', function (e) {
            //increment type or reset
            if (companyFType >= 2) {
                companyFType = 0;
            }
            companyFType += 1;

            //evaluate sorting action
            switch (companyFType) {
                case 1:
                    sortTableUp(1, SORT_TYPE.STR);
                    break;
                case 2:
                    sortTableDown(1, SORT_TYPE.STR);
                    break;
                default:
                    console.error("companyFType - Invalid Value Reached");
                    break;
            }
        });
    } else {
        console.log("error state reached for companyFilter");
    }
    if (locationFilter) { //Col 2
        locationFilter.addEventListener('click', function (e) {
            //TODO: location api
        });
    } else {
        console.log("error state reached for locationFilter");
    }
    if (wageFilter) { //Col 3
        wageFilter.addEventListener('click', function (e) {
            //increment type or reset
            if (wageFType >= 2) {
                wageFType = 0;
            }
            wageFType += 1;

            //evaluate sorting action
            switch (wageFType) {
                case 1:
                    sortTableUp(3, SORT_TYPE.WAGE);
                    break;
                case 2:
                    sortTableDown(3, SORT_TYPE.WAGE);
                    break;
                default:
                    console.error("wageFType - Invalid Value Reached");
                    break;
            }
        });
    } else {
        console.log("error state reached for wageFilter");
    }
    if (postedFilter) { //Col 4
        postedFilter.addEventListener('click', function (e) {
            //increment type or reset
            if (postedFType == 2) {
                postedFType = 0;
            }
            postedFType += 1;

            //evaluate sorting action
            switch (postedFType) {
                case 1:
                    sortTableUp(4, SORT_TYPE.DATE);
                    break;
                case 2:
                    sortTableDown(4, SORT_TYPE.DATE);
                    break;
                default:
                    console.error("postedFType - Invalid Value Reached");
                    break;
            }
        });
    } else {
        console.log("error state reached for postedFilter");
    }
});

function sortTableDown(column = 0,type) {
    var table, rows;
    table = document.getElementById("tableBody");

    rows = Array.from(table.querySelectorAll('tr'));
    rows.sort((a, b) => {
        switch (type) {
            case SORT_TYPE.STR:
                var aValue = a.cells[column].textContent;
                var bValue = b.cells[column].textContent;
                return bValue.localeCompare(aValue);
            case SORT_TYPE.WAGE:
            case SORT_TYPE.DATE:
                var aValue = a.cells[column].id;
                var bValue = b.cells[column].id;
                console.log("a: " + aValue + " b: " + bValue);
                return bValue - aValue;
            default:
                return null;
        }
    });

    rows.forEach(row => {
        if (row != null) {
            table.appendChild(row);
        }
    });
}

function sortTableUp(column = 0, type) {
    var table, rows;
    table = document.getElementById("tableBody");
    rows = Array.from(table.querySelectorAll('tr'));
    rows.sort((a, b) => {
        switch (type) {
            case SORT_TYPE.STR:
                var aValue = a.cells[column].textContent;
                var bValue = b.cells[column].textContent;
                return aValue.localeCompare(bValue);
            case SORT_TYPE.WAGE:
            case SORT_TYPE.DATE:
                var aValue = a.cells[column].id;
                var bValue = b.cells[column].id;
                return aValue - bValue;
            
            default:
                return null;
        }
    });
    rows.forEach(row => {
        if (row != null) {
            table.appendChild(row);
        }
    });
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