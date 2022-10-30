const colors = [
    "#277da1",
    "#577590",
    "#4d908e",
    "#43aa8b",
    "#90be6d",
    "#f9c74f",
    "#f9844a",
    "#f8961e",
    "#f3722c",
    "#f94144",
];

const conflictNums = document.getElementById("conflictNums");
conflictNums.style.display = "none";
const noConflicts = document.getElementById("noConflicts");
noConflicts.style.display = "none";
// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.10.0/firebase-app.js";
import ky from "https://cdn.skypack.dev/ky";
import {
    getDatabase,
    ref,
    onValue as _onValue,
    child,
} from "https://www.gstatic.com/firebasejs/9.10.0/firebase-database.js";
import { Conflict } from "./Conflict.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/9.10.0/firebase-analytics.js";
import { getConflictSolutions } from "./setConflicts.js";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

const onValue = (...args) =>
    new Promise((res, rej) => {
        try {
            _onValue(...args, res, {
                onlyOnce: true,
            });
        } catch (e) {
            rej(e);
        }
    });

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
    apiKey: "AIzaSyDpRnVPxpDY8qXPbe9GPZGOgfPwlSGiTAk",
    authDomain: "coursescheduler499.firebaseapp.com",
    databaseURL: "https://coursescheduler499-default-rtdb.firebaseio.com",
    projectId: "coursescheduler499",
    storageBucket: "coursescheduler499.appspot.com",
    messagingSenderId: "499198271274",
    appId: "1:499198271274:web:3aa01385d66f9759060853",
    measurementId: "G-8GZ9VBXDJ1",
};

// Store the information that was gotten from the database in the table
function renderDayAssignment(dayAssignments, courseData) {
    for (const [day, times] of Object.entries(dayAssignments)) {
        for (const [time, classes] of Object.entries(times)) {
            var data = "";

            for (const key of Object.values(classes)) {
                // The string that contains the html code for the table
                data +=
                    '<div class="class" style="border-color: rgba(0, 0, 0, 0.2);">' +
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

// Get the data stored in local storage if it is there so when page is loaded it contains all the data.
if (localStorage.hasOwnProperty("dayAssignments") && localStorage.hasOwnProperty("courseData")) {
    document.querySelectorAll(".class").forEach((c) => c.remove());
    const dayAssignments = JSON.parse(localStorage.getItem("dayAssignments"));
    const courseData = JSON.parse(localStorage.getItem("courseData"));
    renderDayAssignment(dayAssignments, courseData);
}

if (localStorage.hasOwnProperty("conflictSolutions")) {
    const conflictSolutions = JSON.parse(localStorage.getItem("conflictSolutions"));
    conflictNums.textContent = Object.keys(conflictSolutions).length;
    conflictNums.style.display = "inline";
    noConflicts.style.display = "none";
} else {
    noConflicts.style.display = "inline";
}

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const database = getDatabase(app);

// Event that occurs when generate button is pressed
getData.addEventListener("click", async (e) => {

    const conflicts = await ky.post("/assignments/generate", { json: { department: "CS" } }).json(); // run generate_assignments and store the conflicts

    // If there are conflicts store them in local storage and update the conflict page
    if (Object.keys(conflicts).length != 0) {
        conflictNums.textContent = Object.keys(conflicts).length;
        conflictNums.style.display = "inline";

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
        noConflicts.style.display = "inline";
    }

    document.querySelectorAll(".class").forEach((c) => c.remove());
    const dbRef = ref(database, "Department Courses/CS"); // TODO: This is hardcoded right now to only do CS. Need to make it variable depending on which department user is over.
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

    // onValue(dbRef, (snapshot) => {
    //
    const snapshot = await onValue(dbRef);
    // Get all the data from the database
    // let index = 0
    snapshot.forEach((childSnapshot) => {
        const childKey = childSnapshot.key;
        const childData = childSnapshot.val();

        courseData[childKey] = childData;
    });

    // Store the courseData in the local storage.
    localStorage.setItem("courseData", JSON.stringify(courseData));

    // Store the given classes in their corresponding days and times
    for (const [courseName, course] of Object.entries(courseData)) {
        console.log(courseName, course);

        const currentDay = course["Day Assignment"];

        const currentTime = course["Time Assignment"];

        if (["MW", "TR"].includes(currentDay) && ["A", "B", "C", "D", "E", "F", "G"].includes(currentTime))
            dayAssignments[currentDay][currentTime].push(courseName); // Adds courseName to day Assignment in the corresponding spot
    }

    // store dayAssignment in local storage
    localStorage.setItem("dayAssignments", JSON.stringify(dayAssignments));

    renderDayAssignment(dayAssignments, courseData); // Populate the table with the data gotten from the database.
    // }, {
    //     onlyOnce: true
    // });
});

downloadButton.addEventListener("click", async () => {
    const department = "CS";

    var link = document.createElement("a");
    // If you don't know the name or want to use
    // the webserver default set name = ''
    link.setAttribute("download", "Export" + department + "Data.csv");
    link.href = `/csv/export?department=${department}`;
    document.body.appendChild(link);
    link.click();
    link.remove();
});
