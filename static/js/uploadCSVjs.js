
import ky from "https://cdn.skypack.dev/ky";

const classTextBox = document.getElementById("classTextBox"); // Class number text box that is checked to see if the class they entered already exists and to check if its in the correct format
const facultyTextBox = document.getElementById("faculty"); // Used to check to see if contents are in the correct format
const getDBData = await ky.get("/get/DB").json(); // Get the data from the database to test the classes against the contents of classTextBox
const classOverwriteWarning = document.getElementById("classOverwriteWarning"); // Warning that appears if a class is about to be overwritten
const department = document.getElementById("department"); // Used to disable department dropdown if there is only 1 department that person has access to
const manualSubmitButton = document.getElementById("manualSubmitButton"); // Manual entry submit button
const uploadCSVSubmitButton = document.getElementById("uploadCSVSubmitButton"); // CSV upload submit button
const uploadCSV = document.getElementById("uploadCSV"); // Class CSV input
const uploadRooms = document.getElementById("uploadRooms"); // Room CSV input

// Used so classTextBox is not being check everytime there is some change to it
const debounce = (func, delay) => {
    let debounceTimer
    return function() {
        const context = this
        const args = arguments
            clearTimeout(debounceTimer)
                debounceTimer
            = setTimeout(() => func.apply(context, args), delay)
    }
} 

// Checks to see if class that is inputted in classTextBox already exists and if so gives a warning that it exists
if (classTextBox != null) {
    classTextBox.addEventListener("input", debounce(function() {
        console.log("hello")
        let realClassName = department.value + classTextBox.value;
        for (const className of Object.keys(getDBData)) {
            if (realClassName === className) {
                classOverwriteWarning.style.visibility = "visible";
                break;
            } else {
                classOverwriteWarning.style.visibility = "hidden";
            }
        }
    }, 100));
}

// Disable department dropdown if there is only one department option
if (department != null) {
    if (department.options.length === 1) {
        department.style.appearance = "none";
        department.disabled = true;
    }
}

// If button is pressed, then set boolean updateGenerateButton to true to indicate that the schedule needs to be updated
if (uploadCSVSubmitButton != null) {
    uploadCSVSubmitButton.addEventListener("click", async (e) => {
        if (uploadCSV.value != "" && uploadRooms.value != "") {
            localStorage.clear();
            localStorage.setItem("updateGenerateButton", true)
        }
    });
}

// If the button is pressed and all info inputted is correct and then set boolean updateGenerateButton to true to indicate that the schedule needs to be updated
if (manualSubmitButton != null) {
    manualSubmitButton.addEventListener("click", async (e) => {
        if (/^[0-9]{3}[-][0-9]{2}$/.test(classTextBox.value) && /^[A-Za-z.' ]{1,40}$/.test(facultyTextBox.value)) {
            localStorage.clear();
            localStorage.setItem("updateGenerateButton", true)
        }
    });
}
