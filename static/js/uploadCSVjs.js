
import ky from "https://cdn.skypack.dev/ky";

const classTextBox = document.getElementById("classTextBox");
const facultyTextBox = document.getElementById("faculty");
const getDBData = await ky.get("/get/DB").json();
const classOverwriteWarning = document.getElementById("classOverwriteWarning");
const department = document.getElementById("department");
const uploadCSVSubmitButton = document.getElementById("uploadCSVSubmitButton");
const uploadCSV = document.getElementById("uploadCSV");
const uploadRooms = document.getElementById("uploadRooms");
const manualSubmitButton = document.getElementById("manualSubmitButton");

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

if (classTextBox != null) {
    classTextBox.addEventListener("input", debounce(function() {
        console.log("hello");
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

if (department != null) {
    if (department.options.length === 1) {
        department.style.appearance = "none";
        department.disabled = true;
    }
}
if (uploadCSVSubmitButton != null) {
    uploadCSVSubmitButton.addEventListener("click", async (e) => {
        if (uploadCSV.value != "" && uploadRooms.value != "") {
            localStorage.clear();
            localStorage.setItem("updateGenerateButton", true)
            console.log("Hello")
        }
    });
}

if (manualSubmitButton != null) {
    manualSubmitButton.addEventListener("click", async (e) => {
        if (/^[0-9]{3}[-][0-9]{2}$/.test(classTextBox.value) && /^[A-Za-z.' ]{1,40}$/.test(facultyTextBox.value)) {
            localStorage.clear();
            localStorage.setItem("updateGenerateButton", true)
            console.log("General")
        }
    });
}
