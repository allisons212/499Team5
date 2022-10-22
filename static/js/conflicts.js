
// Get the modal
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var conflictIcon = document.getElementById("conflictsIcon");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];


var roomsDropDown = document.getElementById("conflictRoomsDropDown");

var daysTimesDropDown = document.getElementById("conflictDaysTimesDropDown");

var conflictSave = document.getElementById("conflictSave");

var conflictEdit = document.getElementById("conflictEdit");

var roomDayTimeWarning = document.getElementById("roomDayTimeWarning");

var roomsValue = daysTimesDropDown.value;


// When the user clicks the button, open the modal 
conflictIcon.onclick = function () {
  modal.style.display = "block";
  document.body.style.overflow = "hidden";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function () {
  modal.style.display = "none";
  document.body.style.overflow = "auto";
  roomDayTimeWarning.style.display = "none";
}

conflictSave.onclick = function () {
  if (roomsDropDown.value != "" && daysTimesDropDown.value != "") {
    conflictSave.disabled = true;
    daysTimesDropDown.disabled = true;
    roomsDropDown.disabled = true
    daysTimesDropDown.style.cursor = "context-menu";
    roomsDropDown.style.cursor = "context-menu"
    conflictEdit.style.display = "inline";
    roomDayTimeWarning.style.display = "none";
  }
  else {
    roomDayTimeWarning.style.display = "inline";
  }
}

conflictEdit.onclick = function () {
  conflictSave.disabled = false;
  daysTimesDropDown.disabled = false;
  roomsDropDown.disabled = false
  conflictEdit.style.display = "none";
  daysTimesDropDown.style.cursor = "pointer";
  roomsDropDown.style.cursor = "pointer"
}

function listenRoomsDropDown() {
  // console.log(ev.target.value)
  if (roomsDropDown.value === "") {
    daysTimesDropDown.disabled = true;
    daysTimesDropDown.options[0].selected = 'selected';
    daysTimesDropDown.style.cursor = "context-menu";
  }
  else {
    daysTimesDropDown.disabled = false
    daysTimesDropDown.style.cursor = "pointer";

  }
  if (roomsDropDown.value != roomsValue) {
    daysTimesDropDown.options[0].selected = 'selected';
    roomsValue = roomsDropDown.value
  }
}

roomDayTimeWarning.style.display = "none";
daysTimesDropDown.style.cursor = "context-menu";
conflictEdit.style.display = "none";
daysTimesDropDown.disabled = true;
roomsDropDown.addEventListener('input', listenRoomsDropDown);

