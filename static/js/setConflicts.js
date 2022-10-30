
import ky from "https://cdn.skypack.dev/ky"
import { Conflict } from "./Conflict.js";
// Get the modal
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var conflictIcon = document.getElementById("conflictsIcon");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

var classConflictsContainer = document.getElementById("classConflicts")


// var roomsDropDown = document.getElementById("conflictRoomsDropDown");

// var daysTimesDropDown = document.getElementById("conflictDaysTimesDropDown");

// var conflictSave = document.getElementById("conflictSave");

// var conflictEdit = document.getElementById("conflictEdit");

// var roomDayTimeWarning = document.getElementById("roomDayTimeWarning");

// var roomsValue = roomsDropDown.value;

var conflicts = localStorage.hasOwnProperty("conflicts") ? JSON.parse(localStorage.getItem("conflicts")) : [];

const department = "CS"

const emptyRooms = await ky.get(`/empty/rooms?department=${department}`).json()

var selectedRooms = emptyRooms;

var conflictSolutions = []


// When the user clicks the button, open the modal 
conflictIcon.onclick = function () {
  modal.style.display = "block";
  document.body.style.overflow = "hidden";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function () {
  modal.style.display = "none";
  document.body.style.overflow = "auto";
}

// conflictSave.onclick = function () {
//   if (roomsDropDown.value != "" && daysTimesDropDown.value != "") {
//     conflictSave.disabled = true;
//     daysTimesDropDown.disabled = true;
//     roomsDropDown.disabled = true
//     daysTimesDropDown.style.cursor = "context-menu";
//     roomsDropDown.style.cursor = "context-menu"
//     conflictEdit.style.display = "inline";
//     roomDayTimeWarning.style.display = "none";
//   }
//   else {
//     roomDayTimeWarning.style.display = "inline";
//   }
// }

// conflictEdit.onclick = function () {
//   conflictSave.disabled = false;
//   daysTimesDropDown.disabled = false;
//   roomsDropDown.disabled = false
//   conflictEdit.style.display = "none";
//   daysTimesDropDown.style.cursor = "pointer";
//   roomsDropDown.style.cursor = "pointer"
// }

// function listenRoomsDropDown() {
//   // console.log(ev.target.value)
//   if (roomsDropDown.value === "") {
//     daysTimesDropDown.disabled = true;
//     daysTimesDropDown.options[0].selected = 'selected';
//     daysTimesDropDown.style.cursor = "context-menu";
//   }
//   else {
//     daysTimesDropDown.disabled = false
//     daysTimesDropDown.style.cursor = "pointer";

//   }
//   if (roomsDropDown.value != roomsValue) {
//     daysTimesDropDown.options[0].selected = 'selected';
//     roomsValue = roomsDropDown.value
//   }
// }

// roomDayTimeWarning.style.display = "none";
// daysTimesDropDown.style.cursor = "context-menu";
// conflictEdit.style.display = "none";
// daysTimesDropDown.disabled = true;
// roomsDropDown.addEventListener('input', listenRoomsDropDown);
// console.log("conflicts: ", conflicts)
for (const [className, classInfo] of Object.entries(conflicts)) {
  console.log(className, classInfo["Faculty Assignment"])
  conflictSolutions.push(new Conflict(className, classInfo["Faculty Assignment"]))
}
for (const conflict of Object.values(conflictSolutions)) {
  // console.log("item", conflict)
  // for(const room of Object.keys(emptyRooms)){
  conflict.setRoomDropDown(selectedRooms);
  // }

  // var option = document.createElement("option");
  // option.value = "";
  // option.text = "--Select--";
  // conflict.roomsDropDown.add(option);
  // // conflict.dayTimeDropDown.add(option);
  conflict.dayTimeDropDown.options[0].selected = 'selected';
  conflict.roomsDropDown.options[0].selected = 'selected';
  // console.log(conflict.dayTimeDropDown.options.length)


  conflict.conflictSave.onclick = function () {
    if (conflict.roomsDropDown.value != "" && conflict.dayTimeDropDown.value != "") {
      conflict.conflictSave.disabled = true;
      conflict.dayTimeDropDown.disabled = true;
      conflict.roomsDropDown.disabled = true
      conflict.dayTimeDropDown.style.cursor = "context-menu";
      conflict.roomsDropDown.style.cursor = "context-menu"
      conflict.conflictEdit.style.display = "inline";
      conflict.roomDayTimeWarning.style.display = "none";
      conflict.room = conflict.roomsDropDown.value;
      conflict.dayAndTime = conflict.dayTimeDropDown.value;
      removeDaysTimesRooms(conflict.room, conflict.dayAndTime);
    }
    else {
      conflict.roomDayTimeWarning.style.display = "inline";
    }
  }

  conflict.conflictEdit.onclick = function () {
    conflict.conflictSave.disabled = false;
    conflict.dayTimeDropDown.disabled = false;
    conflict.roomsDropDown.disabled = false
    conflict.conflictEdit.style.display = "none";
    conflict.dayTimeDropDown.style.cursor = "pointer";
    conflict.roomsDropDown.style.cursor = "pointer"
    addDayTimesRoomsBack(conflict.room, conflict.dayAndTime)
    conflict.room = "";
    conflict.dayAndTime = "";

  }

  conflict.roomsDropDown.addEventListener('input', function () {
    if (conflict.roomsDropDown.value === "") {
      conflict.dayTimeDropDown.disabled = true;
      conflict.dayTimeDropDown.options[0].selected = 'selected';
      conflict.dayTimeDropDown.style.cursor = "context-menu";
    }
    else {
      conflict.dayTimeDropDown.disabled = false
      conflict.dayTimeDropDown.style.cursor = "pointer";
      conflict.setDayTimeDropDown(selectedRooms[conflict.roomsDropDown.value]);

    }
    if (conflict.roomsDropDown.value != conflict.roomsValue) {
      conflict.dayTimeDropDown.options[0].selected = 'selected';
      conflict.roomsValue = conflict.roomsDropDown.value
    }
  });
}

for (const conflict of Object.values(conflictSolutions)) {
  var className = document.createElement("h6");
  className.textContent = conflict.className;
  className.classList.add("conflictClassName");
  var conflictTeacher = document.createElement("h6");
  conflictTeacher.textContent = conflict.teacher;
  conflictTeacher.classList.add("conflictTeacherName");
  var ConflictDropDown = document.createElement("div");
  ConflictDropDown.classList.add("conflictDropDown");
  ConflictDropDown.appendChild(conflict.roomsDropDownLabel).appendChild(conflict.roomsDropDown);
  ConflictDropDown.appendChild(conflict.dayTimeDropDownLabel).appendChild(conflict.dayTimeDropDown);
  ConflictDropDown.appendChild(conflict.conflictSave);
  ConflictDropDown.appendChild(conflict.conflictEdit);
  ConflictDropDown.appendChild(conflict.roomDayTimeWarning);


  classConflictsContainer.appendChild(className);
  classConflictsContainer.appendChild(conflictTeacher);
  classConflictsContainer.appendChild(ConflictDropDown);
}

function removeDaysTimesRooms(room, dayAndTime) {
  for (let i = 0; i < selectedRooms[room].length; i++) {
    if (selectedRooms[room][i] === dayAndTime) {
      selectedRooms[room].splice(i, 1);
    }
  }
  if (selectedRooms[room].length === 0) {
    delete selectedRooms[room]
    console.log(selectedRooms[room])

    for (const conflict of Object.values(conflictSolutions)) {
      if (conflict.room != room) {
        conflict.setRoomDropDown(selectedRooms)
      }
    }
  }
  else {
    for (const conflict of Object.values(conflictSolutions)) {
      if (conflict.dayAndTime != dayAndTime) {
        conflict.setDayTimeDropDown(selectedRooms[room]);
      }
    }
  }
}

function addDayTimesRoomsBack(room, dayAndTime) {
  if (selectedRooms[room] === undefined) {
    selectedRooms[room] = []
    console.log(selectedRooms[room])
    for (const conflict of Object.values(conflictSolutions)) {
      if (conflict.room != room) {
        conflict.setRoomDropDown(selectedRooms)
      }
    }
  }
  selectedRooms[room].push(dayAndTime)
  console.log("day", selectedRooms[room])
  for (const conflict of Object.values(conflictSolutions)) {
    if (confclit.dayAndTime != dayAndTime) {
      conflict.setDayTimeDropDown(selectedRooms[room]);
    }
  }
}









