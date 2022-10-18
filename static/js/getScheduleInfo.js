// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.10.0/firebase-app.js";
import {
    getDatabase,
    ref,
    onValue as _onValue,
    child,
} from "https://www.gstatic.com/firebasejs/9.10.0/firebase-database.js";

import { getAnalytics } from "https://www.gstatic.com/firebasejs/9.10.0/firebase-analytics.js";
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
                    '<div class="class">' +
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

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const database = getDatabase(app);

// Event that occurs when generate button is pressed
getData.addEventListener("click", async (e) => {
    document.querySelectorAll(".class").forEach((c) => c.remove());
    const dbRef = ref(database, "Department Courses/CS");
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
        console.log(JSON.stringify(course["Day Assignment"]), course["Day Assignment"] === "MW");

        const currentDay = course["Day Assignment"];

        // Checks to make sure that the day blocks are correct
        if (!["MW", "TR"].includes(currentDay)) {
            console.error("An error occurred: incorrect day");
            return;
        }

        const currentTime = course["Time Assignment"];

        // Checks to make sure that the time blocks are correct
        if (!["A", "B", "C", "D", "E", "F", "G"].includes(currentTime)) {
            console.error("An error occurred: incorrect time");
            return;
        }

        dayAssignments[currentDay][currentTime].push(courseName); // Adds courseName to day Assignment in the corresponding spot
    }

    // store dayAssignment in local storage
    localStorage.setItem("dayAssignments", JSON.stringify(dayAssignments));

    renderDayAssignment(dayAssignments, courseData); // Populate the table with the data gotten from the database.
    // }, {
    //     onlyOnce: true
    // });
});