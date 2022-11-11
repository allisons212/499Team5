
// Class that contains the info for each conflict
export class Conflict {
    // Creates all the values needed and set them to the correct HTML for when they are displayed to the screen
    constructor(newClassName, newTeacher) {
        this.className = newClassName;
        this.teacher = newTeacher;
        this.roomsDropDown = document.createElement("select");
        this.dayTimeDropDown = document.createElement("select");
        this.conflictSave = document.createElement("button");
        this.conflictEdit = document.createElement("i");
        this.roomDayTimeWarning = document.createElement("span");
        this.roomsValue = this.roomsDropDown.value;
        this.room = "";
        this.dayAndTime = "";


        this.conflictSave.type = "submit";
        this.conflictSave.classList.add("conflictSave");

        this.conflictEdit.innerHTML = '<i class="fa fa-pencil" id="conflictEdit" style="font-size: 20px"></i>';
        this.roomDayTimeWarning.innerHTML =
            '<i class="fa fa-exclamation-circle"></i> Must have both room and day and time selected.';

        var option = document.createElement("option");
        option.value = "";
        option.text = "--Select--";
        this.roomsDropDown.add(option);
        this.roomsDropDown.value = ""
        option = document.createElement("option");
        option.value = "";
        option.text = "--Select--";
        this.dayTimeDropDown.add(option);
        this.dayTimeDropDown.value = ""


        this.roomsDropDown.name = "rooms";
        this.roomsDropDown.classList.add("conflictRooms");
        this.dayTimeDropDown.name = "dayAndTime";
        this.dayTimeDropDown.classList.add("conflictdayTime");

        this.roomsDropDownLabel = document.createElement("label");
        this.roomsDropDownLabel.innerHTML = "Classroom Selection  ";
        this.roomsDropDownLabel.classList.add("conflictDropDownLabel");
        this.roomsDropDownLabel.htmlFor = "rooms";

        this.dayTimeDropDownLabel = document.createElement("label");
        this.dayTimeDropDownLabel.innerHTML = "Day and Time  ";
        this.dayTimeDropDownLabel.classList.add("conflictDropDownLabel");
        this.dayTimeDropDownLabel.htmlFor = "dayAndTime";

        this.roomDayTimeWarning.style.display = "none";
        this.roomDayTimeWarning.classList.add("roomDayTimeWarning");
        this.dayTimeDropDown.style.cursor = "context-menu";
        this.conflictEdit.style.display = "none";
        this.dayTimeDropDown.disabled = true;

        this.conflictSave.textContent = "Save";
        this.saved = false;
    }

    // Create a conflict from the given information and return the new conflict created (given from local storage)
    static fromLocal({ className, teacher, dayAndTime, room }) {
        const temp = new Conflict(className, teacher);

        temp.dayAndTime = dayAndTime;
        temp.room = room;

        return temp;
    }

    // Return the information stored in the conflict to be used in local storage
    toLocal() {
        return {
            className: this.className,
            teacher: this.teacher,
            dayAndTime: this.dayAndTime,
            room: this.room,
        };
    }

    // Set the values used in the roomDropDown
    setRoomDropDown(emptyRooms) {
        if (this.roomsDropDown.options.length > 0) {
            for (let i = this.roomsDropDown.options.length; i >= 0; i--) {
                this.roomsDropDown.remove(i);
            }
        }

        var option = document.createElement("option");
        option.value = "";
        option.text = "--Select--";
        this.roomsDropDown.appendChild(option);
        for (const room of Object.keys(emptyRooms).sort()) {
            var option = document.createElement("option");
            option.value = room;
            option.text = room;
            option.classList.add("conflictRoom");
            this.roomsDropDown.add(option);
        }

        this.roomsDropDown.value = this.room
    }

    // Remove a room from dropdown
    removeFromRoomDropDown(room) {
        for (let i = 0; i < this.roomsDropDown.length; i++) {
            if (this.roomsDropDown.options[i].value === room) {
                this.roomsDropDown.remove(i);
            }
        }
    }

    // Set the dayAndTimeDropDown given the days and times for a room 
    setDayTimeDropDown(daysAndTimes) {
        if (this.dayTimeDropDown.options.length > 0) {
            for (let i = this.dayTimeDropDown.options.length; i >= 0; i--) {
                this.dayTimeDropDown.remove(i);
            }
        }
        var option = document.createElement("option");
        option.value = "";
        option.text = "--Select--";
        this.dayTimeDropDown.appendChild(option);
        for (const dayAndTime of daysAndTimes.sort()) {
            var option = document.createElement("option");
            option.value = dayAndTime;
            option.text = dayAndTime;
            option.classList.add("conflictDayTime");
            this.dayTimeDropDown.add(option);
        }
    }

    // Remove the day and time from a given room
    removeFromDayTimeDropDown(dayAndTime) {
        for (let i = 0; i < this.dayTimeDropDown.length; i++) {
            if (this.dayTimeDropDown.options[i].value === dayAndTime) {
                this.dayTimeDropDown.remove(i);
            }
        }
    }
}
