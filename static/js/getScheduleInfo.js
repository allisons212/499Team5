import ky from "https://cdn.skypack.dev/ky";
import { getConflictSolutions } from "./setConflicts.js";

const delay = (ms) => new Promise((res) => setTimeout(res, ms)); // Add delay to make change in schedule GUI more obvious

const conflictNums = document.getElementById("conflictNums"); // Number of conflicts that appear next to conflict icon
conflictNums.style.display = "none"; // Set it to display none by default so it does not show up when page is immediately loaded
const noConflicts = document.getElementById("noConflicts"); // Text that displays when there are no conflicts
noConflicts.style.display = "none"; // Set no conflict text to display none by default

const updateGenerateButton = document.getElementById("updateGenerateButton"); // Warning that changes have been made to the schedule and the generate button needs to be pressed to update it

// Store the information that was gotten from the database in the table
async function renderDayAssignment(dayAssignments, courseData) {
    clearTable(dayAssignments); // Clear the table of all classes before generating it again
    await delay(100);
    for (const [day, times] of Object.entries(dayAssignments)) {
        for (const [time, classes] of Object.entries(times)) {
            var data = "";

            for (const key of Object.values(classes)) {
                // The string that contains the html code for the table
                data +=
                    '<div class="class' +
                    day +
                    time +
                    '" style="border-color: rgba(0, 0, 0, 0.2);">' +
                    key +
                    "<br>" +
                    courseData[key]["Faculty Assignment"] +
                    "<br>" +
                    courseData[key]["Classroom Assignment"] +
                    "</div>";
            }
            // Input the info into the table for both days (MW or TR)
            var id = day + time + "0";
            document.getElementById(id).innerHTML = data;
            id = day + time + "1";
            document.getElementById(id).innerHTML = data;
        }
    }
}

// Clears the table of all classes that may be on it
function clearTable(dayAssignments) {
    for (const [day, times] of Object.entries(dayAssignments)) {
        for (const [time] of Object.keys(times)) {
            var id = day + time + "0";
            document.getElementById(id).innerHTML = "";
            id = day + time + "1";
            document.getElementById(id).innerHTML = "";
        }
    }
}

// Get the data stored in local storage if it is there so when page is loaded it contains all the data.
if (localStorage.hasOwnProperty("dayAssignments") && localStorage.hasOwnProperty("courseData")) {
    document.querySelectorAll(".class").forEach((c) => c.remove());
    const dayAssignments = JSON.parse(localStorage.getItem("dayAssignments"));
    const courseData = JSON.parse(localStorage.getItem("courseData"));
    renderDayAssignment(dayAssignments, courseData);
}

// Get the conflictSolutions from local storage to display the number of conflicts next to the conflict icon
if (localStorage.hasOwnProperty("conflictSolutions")) {
    const conflictSolutions = JSON.parse(localStorage.getItem("conflictSolutions"));
    conflictNums.textContent = Object.keys(conflictSolutions).length;
    conflictNums.style.display = "inline";
    noConflicts.style.display = "none";
} else {
    getConflictSolutions(); // set conflictSolutions in SetConflicts.js to null
    noConflicts.style.display = "inline"; // Display that there are no conflicts
}

// Check to see if there have been changes to the schedule where the schedule has to be reloaded
if (localStorage.hasOwnProperty("updateGenerateButton") && localStorage.getItem("updateGenerateButton")) {
    updateGenerateButton.style.visibility = "visible"; // Set 
}

// Event that occurs when generate button is pressed
getData.addEventListener("click", async (e) => {
    localStorage.removeItem("updateGenerateButton"); // Remove boolean stored in local storage that indicates if generate button needs to be updated or not
    updateGenerateButton.style.visibility = "hidden"; // Hide the update to schedule warning because button has been pressed
    const conflicts = await ky.post("/assignments/generate", { json: { department: "CS" } }).json(); // run generate_assignments and store the conflicts
    const getDBData = await ky.get("/get/DB").json(); // After all the info has been pushed to the database, get said info from the database

    // If there are conflicts store them in local storage and update the conflict page
    if (Object.keys(conflicts).length != 0) {
        conflictNums.textContent = Object.keys(conflicts).length;
        conflictNums.style.display = "inline";

        // Generate conflict solutions to be pushed to local storage
        const conflictSolutions = Object.entries(conflicts).map(([className, classInfo]) => ({
            className,
            teacher: classInfo["Faculty Assignment"],
            room: "",
            dayAndTime: "",
        }));

        localStorage.setItem("conflictSolutions", JSON.stringify(conflictSolutions));
        getConflictSolutions();
        noConflicts.style.display = "none";
    } else {
        if (localStorage.hasOwnProperty("conflictSolutions")) {
            localStorage.removeItem("conflictSolutions"); // If there are conflicts in local storage, but no conflicts currently delete said conflicts from storage
        }
        getConflictSolutions(); // Set conflictSolutions in setConflicts.js to null
        noConflicts.style.display = "inline"; // Display the no conflict text
        conflictNums.style.display = "none"; // Get rid of the number of conflicts ntext to the conflict icon
    }

    document.querySelectorAll(".class").forEach((c) => c.remove());
    // const dbRef = ref(database, "Department Courses/CS"); // TODO: This is hardcoded right now to only do CS. Need to make it variable depending on which department user is over.
    var courseData = {}; // All the data stored
    // The day and time assignments for the class. The course name is stored in the arrays.
    var dayAssignments = {
        MW: {
            A: [],
            B: [],
            C: [],
            D: [],
            E: [],
            F: [],
            G: [],
        },
        TR: {
            A: [],
            B: [],
            C: [],
            D: [],
            E: [],
            F: [],
            G: [],
        },
    };

    for (const [className, classInfo] of Object.entries(getDBData)) {
        courseData[className] = classInfo;
    }

    // Store the courseData in the local storage.
    localStorage.setItem("courseData", JSON.stringify(courseData));

    // Store the given classes in their corresponding days and times
    for (const [courseName, course] of Object.entries(courseData)) {

        const currentDay = course["Day Assignment"];

        const currentTime = course["Time Assignment"];

        if (["MW", "TR"].includes(currentDay) && ["A", "B", "C", "D", "E", "F", "G"].includes(currentTime))
            dayAssignments[currentDay][currentTime].push(courseName); // Adds courseName to day Assignment in the corresponding spot
    }

    // store dayAssignment in local storage
    localStorage.setItem("dayAssignments", JSON.stringify(dayAssignments));

    renderDayAssignment(dayAssignments, courseData); // Populate the table with the data gotten from the database.
});

// Call the export_csv function and download the generate file when the download icon is clicked
downloadButton.addEventListener("click", async () => {
    const department = "CS";

    var link = document.createElement("a");
    link.setAttribute("download", "Export" + department + "Data.csv");
    link.href = `/csv/export?department=${department}`;
    document.body.appendChild(link);
    link.click();
    link.remove();
});
