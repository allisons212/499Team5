// // Import the functions you need from the SDKs you need
// import { initializeApp } from "https://www.gstatic.com/firebasejs/9.10.0/firebase-app.js";
// import {
//     getDatabase,
//     ref,
//     onValue as _onValue,
//     child,
// } from "https://www.gstatic.com/firebasejs/9.10.0/firebase-database.js";

// import { getAnalytics } from "https://www.gstatic.com/firebasejs/9.10.0/firebase-analytics.js";
// // TODO: Add SDKs for Firebase products that you want to use
// // https://firebase.google.com/docs/web/setup#available-libraries

// // Your web app's Firebase configuration
// // For Firebase JS SDK v7.20.0 and later, measurementId is optional
// const firebaseConfig = {
//     apiKey: "AIzaSyDpRnVPxpDY8qXPbe9GPZGOgfPwlSGiTAk",
//     authDomain: "coursescheduler499.firebaseapp.com",
//     databaseURL: "https://coursescheduler499-default-rtdb.firebaseio.com",
//     projectId: "coursescheduler499",
//     storageBucket: "coursescheduler499.appspot.com",
//     messagingSenderId: "499198271274",
//     appId: "1:499198271274:web:3aa01385d66f9759060853",
//     measurementId: "G-8GZ9VBXDJ1",
// };

// function makeNewClass(classroom, dayA, dayP, prof, room, seatNum, time, timeBlock) {
//     var classData = {
//         ClassroomAssignment: classroom,
//         DayAssignment: dayA,
//         DayPreferences: dayP,
//         FacultyAssignment: prof,
//         RoomPreferences: room,
//         SeatsOpen: seatNum,
//         TimeAssignment: time,
//         TimeBlockPreferences: timeBlock,
//     };

//     var newUploadKey = firebase.database().ref().child('Department Courses').push().key;

//     var updates = {};

// }

import ky from "https://cdn.skypack.dev/ky";


const classTextBox = document.getElementById("classTextBox");
const getDBData = await ky.get("/get/DB").json()
const classOverwriteWarning = document.getElementById("classOverwriteWarning");
const department = document.getElementById("department");


classTextBox.addEventListener("input", async (e) => {

    let realClassName = department.value + classTextBox.value;
    for(const className of Object.keys(getDBData)){
        
        if(realClassName === className){
            classOverwriteWarning.style.visibility = "visible";
            break;
        }
        else{
            classOverwriteWarning.style.visibility = "hidden";
        }
    }
});

