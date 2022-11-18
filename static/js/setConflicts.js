import ky from "https://cdn.skypack.dev/ky";
import { Conflict } from "./Conflict.js";
// Get the modal
const modal = document.getElementById("myModal"); // Class Conflict modal

// Get the button that opens the modal
const conflictIcon = document.getElementById("conflictsIcon");

// Get the <span> element that closes the modal
const closeIcon = document.getElementsByClassName("close")[0];

const classConflictsContainer = document.getElementById("classConflicts"); // The div that holds all the dynamically created conflicts

const submitWarning = document.getElementById("submitWarning"); // The warning attached to the submit button in generateSchedule.html

submitWarning.style.display = "none"; // Set submit warning to none by default if there are no conflicts avaliable

const submitButton = document.getElementById("submitConflictSolutions"); // The submit button in generateSchedule.html

let _selectedRooms = null; // Holds all the empty rooms that are gotten from the emptyRooms() Function

let _selectedFaculty = null;

const noConflicts = document.getElementById("noConflicts"); // The no conflicts text that appears when there are no conflicts

const conflictNums = document.getElementById("conflictNums"); // The number of conflicts that appears next to the conflict icon

const updateGenerateButton = document.getElementById("updateGenerateButton"); // The warning that appears when changes have been made to the schedule and it needs to be updated

updateGenerateButton.style.visibility = "hidden"; // Set this warning to hidden to start off with

// Get the empty rooms from the getEmptyRooms() python function
const getSelectedRooms = async (reset = false) => {
    if (reset || _selectedRooms === null) _selectedRooms = await ky.get(`/empty/rooms`).json();

    return _selectedRooms;
};

const getSelectedFaculty = async (reset = false) => {
    if (reset || _selectedFaculty === null) _selectedFaculty = await ky.get(`/empty/faculty`).json();

    return _selectedFaculty;
};


// Get the conflicts that were generated from the generate_assignments() python function which is in local storage
const updateConflictSolution = (conflict) => {
    const current = JSON.parse(localStorage.getItem("conflictSolutions"));
    const conflictIndex = current.findIndex((c) => c.className === conflict.className);
    current[conflictIndex] = conflict.toLocal();

    localStorage.setItem("conflictSolutions", JSON.stringify(current));
};

// Save the day and time and room that is selected for the dropdown menu
function saveConflict(conflictSolutions, conflict) {
    if (conflict.roomsDropDown.value !== "" && conflict.dayTimeDropDown.value !== "") {
        // Disable the dropdown menus, save button, and warning attached to the save button and enable the edit icon
        conflict.conflictSave.disabled = true;
        conflict.dayTimeDropDown.disabled = true;
        conflict.roomsDropDown.disabled = true;
        conflict.dayTimeDropDown.style.cursor = "context-menu";
        conflict.roomsDropDown.style.cursor = "context-menu";
        conflict.conflictEdit.style.display = "inline";
        conflict.roomDayTimeWarning.style.display = "none";
        // Save the values for the given conflict
        conflict.room = conflict.roomsDropDown.value;
        conflict.dayAndTime = conflict.dayTimeDropDown.value;
        conflict.saved = true;
        // Remove the option that was selected so that no other class can go in the same room and day and time combination
        removeDaysTimesRooms(conflictSolutions, conflict.room, conflict.dayAndTime);
        updateConflictSolution(conflict); // Store saved values to the local storage
    } else {
        // If both rooms and day and time do not have an option selected, display an error
        conflict.roomDayTimeWarning.style.display = "inline";
    }
}

function getTrueDaysAndTimes(room, faculty){
    let trueDaysAndTimes = []
    for (const roomDayAndTime of room){
        for(const facultyDayAndTime of faculty){
            if(roomDayAndTime === facultyDayAndTime){
                trueDaysAndTimes.push(roomDayAndTime)
            }
        }
    }
    return trueDaysAndTimes
}

async function appendConflicts(conflictSolutions) {
    const selectedRooms = await getSelectedRooms();

    const selectedFaculty = await getSelectedFaculty();


    for (const conflict of conflictSolutions) {
        // Put the rooms in the dropdown menus for each conflict
        await conflict.setRoomDropDown(selectedRooms);
        // If a room is selected, put the day and times for the selected room in the dropdown menus for each conflict
        if (conflict.room !== "") {
            await conflict.setDayTimeDropDown(getTrueDaysAndTimes(selectedRooms[conflict.room], selectedFaculty[conflict.teacher]));

            // If dayAndTime contain something save the values
            if (conflict.dayAndTime !== "") {
                conflict.dayTimeDropDown.value = conflict.dayAndTime;
                conflict.dayTimeDropDown.disabled = false;

                saveConflict(conflictSolutions, conflict);
            }
        }

        conflict.conflictSave.onclick = () => saveConflict(conflictSolutions, conflict); // Occurs when save button is pressed

        // Occurs when the edit icon is clicked
        conflict.conflictEdit.onclick = function () {
            // Enable the save button and dropdown menus and disable the edit icon
            conflict.conflictSave.disabled = false;
            conflict.dayTimeDropDown.disabled = false;
            conflict.roomsDropDown.disabled = false;
            conflict.conflictEdit.style.display = "none";
            conflict.dayTimeDropDown.style.cursor = "pointer";
            conflict.roomsDropDown.style.cursor = "pointer";
            addDayTimesRoomsBack(conflictSolutions, conflict.room, conflict.dayAndTime); // Add the classrooms and days and times that were removed by the save button back
            // Reset the saved data of the conflict
            conflict.room = "";
            conflict.dayAndTime = "";
            conflict.saved = false;
            updateConflictSolution(conflict); // Update the local storage
        };

        // Check the room dropdown to help prevent user from selecting a day and time without a room
        conflict.roomsDropDown.addEventListener("input", async function () {
            if (conflict.roomsDropDown.value === "") {
                conflict.dayTimeDropDown.disabled = true;
                conflict.dayTimeDropDown.options[0].selected = "selected";
                conflict.dayTimeDropDown.style.cursor = "context-menu";
            } else {
                conflict.dayTimeDropDown.disabled = false;
                conflict.dayTimeDropDown.style.cursor = "pointer";
                const selectedFaculty = await getSelectedFaculty();
                conflict.setDayTimeDropDown(getTrueDaysAndTimes(selectedRooms[conflict.roomsDropDown.value], selectedFaculty[conflict.teacher]));
            }
            if (conflict.roomsDropDown.value !== conflict.roomsValue) {
                conflict.dayTimeDropDown.options[0].selected = "selected";
                conflict.roomsValue = conflict.roomsDropDown.value;
            }
        });

        // Create the actual HTML that is shown to the screen
        let className = document.createElement("h6");
        className.textContent = conflict.className;
        className.classList.add("conflictClassName");
        let conflictTeacher = document.createElement("h6");
        conflictTeacher.textContent = conflict.teacher;
        conflictTeacher.classList.add("conflictTeacherName");
        let ConflictDropDown = document.createElement("div");
        ConflictDropDown.classList.add("conflictDropDown");
        ConflictDropDown.appendChild(conflict.roomsDropDownLabel).appendChild(conflict.roomsDropDown);
        ConflictDropDown.appendChild(conflict.dayTimeDropDownLabel).appendChild(conflict.dayTimeDropDown);
        ConflictDropDown.appendChild(conflict.conflictSave);
        ConflictDropDown.appendChild(conflict.conflictEdit);
        ConflictDropDown.appendChild(conflict.roomDayTimeWarning);

        classConflictsContainer.appendChild(className);
        classConflictsContainer.appendChild(conflictTeacher);
        classConflictsContainer.appendChild(ConflictDropDown);

        // Reset everything when the closeIcon is clicked
        const resetOnExit = async () => {
            closeIcon.removeEventListener("click", resetOnExit);

            await conflict.setRoomDropDown(selectedRooms);
            // If a room is selected, put the day and times for the selected room in the dropdown menus for each conflict
            if (conflict.room !== "") {
                const selectedFaculty = await getSelectedFaculty();
                await conflict.setDayTimeDropDown(getTrueDaysAndTimes(selectedRooms[conflict.room], selectedFaculty[conflict.teacher]));

                // If dayAndTime contain something save the values
                if (conflict.dayAndTime !== "") {
                    conflict.dayTimeDropDown.value = conflict.dayAndTime;
                    conflict.dayTimeDropDown.disabled = false;

                    saveConflict(conflictSolutions, conflict);
                }
            } else {
                conflict.dayTimeDropDown.value = conflict.dayAndTime;
                conflict.dayTimeDropDown.disabled = true;
            }

            
            if(classConflictsContainer.contains(className)) {classConflictsContainer.removeChild(className);}
            if(classConflictsContainer.contains(conflictTeacher)){classConflictsContainer.removeChild(conflictTeacher);}
            if(classConflictsContainer.contains(ConflictDropDown)){ classConflictsContainer.removeChild(ConflictDropDown);}
            

            conflict.roomDayTimeWarning.style.display = "none";
        };

        closeIcon.addEventListener("click", resetOnExit);
    }
}

// Remove the time and day chosen for a given room when saved button is pressed. Also, if there are no more days and times left in a room, delete the room
async function removeDaysTimesRooms(conflictSolutions, room, dayAndTime) {
    const selectedRooms = await getSelectedRooms();
    // Get rid of time and day for the given room
    for (let i = 0; i < selectedRooms[room].length; i++) {
        if (selectedRooms[room][i] === dayAndTime) {
            selectedRooms[room].splice(i, 1);
        }
    }
    // Check to see if room time and day info is empty and if so, remove the room
    if (selectedRooms[room].length === 0) {
        delete selectedRooms[room];

        // Update the dropdowns with the new information and make sure that the dropdowns values stay the same when updated
        for (const conflict of conflictSolutions) {
            if (conflict.saved !== true) {
                var roomTempValue = conflict.roomsDropDown.value !== room ? conflict.roomsDropDown.value : "";
                var dayTimeTempValue = conflict.roomsDropDown.value !== room ? conflict.dayTimeDropDown.value : "";
                await conflict.setRoomDropDown(selectedRooms);
                conflict.roomsDropDown.value = roomTempValue;
                conflict.dayTimeDropDown.value = dayTimeTempValue;
                if (conflict.roomsDropDown.value === "") {
                    conflict.dayTimeDropDown.disabled = true;
                }
            }
        }
    }

    // Update the dropdowns with the new information
    for (const conflict of conflictSolutions) {
        if (conflict.saved !== true && conflict.roomsDropDown.value === room) {
            var tempValue = conflict.dayTimeDropDown.value;
            const selectedFaculty = await getSelectedFaculty();
            await conflict.setDayTimeDropDown(getTrueDaysAndTimes(selectedRooms[room], selectedFaculty[conflict.teacher]));
            conflict.dayTimeDropDown.value = tempValue;
        }
    }
}

// Add the day and time and room that were removed by the removeDaysTimesRooms() function. Used when the edit icon is clicked
async function addDayTimesRoomsBack(conflictSolutions, room, dayAndTime) {
    const selectedRooms = await getSelectedRooms();
    // Check to see if the room that is being added back exists or not and if not add it back
    if (selectedRooms[room] === undefined) {
        selectedRooms[room] = [];
        // Update the roomDropDown accordingly
        for (const conflict of conflictSolutions) {
            if (conflict.saved !== true) {
                await conflict.setRoomDropDown(selectedRooms);
            }
        }
    }
    // Add the day and time for the room back
    selectedRooms[room].push(dayAndTime);
    // Update the dayTimeDropdown accordingly and make sure its position in the dropdown is the same
    for (const conflict of conflictSolutions) {
        if (conflict.saved !== true && conflict.roomsDropDown.value === room) {
            var tempValue = conflict.dayTimeDropDown.value;
            const selectedFaculty = await getSelectedFaculty();
            conflict.setDayTimeDropDown(getTrueDaysAndTimes(selectedRooms[room], selectedFaculty[conflict.teacher]));
            conflict.dayTimeDropDown.value = tempValue;
        }
    }
}

let conflictSolutions = null;
getConflictSolutions(); // Gets the conflictSolutions stored in local storage

// Event listener added onto closeIcon
const handleX = () => {
    modal.style.display = "none";
    document.body.style.overflow = "auto";
    submitWarning.style.display = "none";
};

// Event listener added onto submit button
const handleSubmit = async () => {
    const submitWarning = document.getElementById("submitWarning");

    // Checks to see if all conflict solutions are saved and if so, submit. If not, display a warning
    if (conflictSolutions) {
        if (conflictSolutions.some((e) => !e.saved)) {
            submitWarning.style.display = "inline";
        } else {
            submitWarning.style.display = "none";
            for (const conflict of conflictSolutions) {
                await ky.put("/update/solution/assignments", { json: conflict.toLocal() });
            }
            classConflictsContainer.innerHTML = "";
            localStorage.removeItem("conflictSolutions");
            conflictSolutions = null;
            noConflicts.style.display = "inline";
            submitButton.style.display = "none";
            conflictNums.style.display = "none";
            updateGenerateButton.style.visibility = "visible";
        }
    }
};

// Display the modal that contains all the conflict information
function showModal() {
    if (conflictSolutions) {
        appendConflicts(conflictSolutions);
        submitButton.style.display = "inline";
    } else {
        submitButton.style.display = "none";
    }

    submitButton.addEventListener("click", handleSubmit);

    // When the user clicks on <span> (x), close the modal
    closeIcon.addEventListener("click", handleX);

    modal.style.display = "block";
    document.body.style.overflow = "hidden";
}

// Hide the modal when the closeIcon is clicked
function hideModal() {
    modal.style.display = "none";
    document.body.style.overflow = "auto";

    submitWarning.style.display = "none";
    closeIcon.removeEventListener("click", handleX);
    submitButton.removeEventListener("click", handleSubmit);
    getSelectedRooms(true);
    getSelectedFaculty(true);
}

// Update the conflictSolutions with information stored in local storage
export function getConflictSolutions() {
    if (localStorage.hasOwnProperty("conflictSolutions")) {
        conflictSolutions = JSON.parse(localStorage.getItem("conflictSolutions")).map((each) =>
            Conflict.fromLocal(each)
        );
    } else {
        conflictSolutions = null; // If there are currently no conflicts, remove the conflicts saved from before.
    }
}

// When the user clicks the button, open the modal
conflictIcon.addEventListener("click", showModal);
closeIcon.addEventListener("click", hideModal);
