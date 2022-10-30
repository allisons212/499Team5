export class Conflict{
    constructor(newClassName, newTeacher){
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

        // this.roomsDropDown.addEventListener('input', listenRoomsDropDown(this.roomsDropDown, this.dayTimeDropDown, this.roomsValue));

        this.conflictSave.type = "submit";
        this.conflictSave.classList.add("conflictSave");


        this.conflictEdit.innerHTML = '<i class="fa fa-pencil" id="conflictEdit" style="font-size: 20px"></i>';
        this.roomDayTimeWarning.innerHTML = '<i class="fa fa-exclamation-circle"></i> Must have both room and day and time selected.';



        var option = document.createElement("option");
        option.value = "";
        option.text = "--Select--";
        this.roomsDropDown.add(option);
        this.dayTimeDropDown.add(option);

        // console.log(this.roomsDropDown.options.length)

        // this.dayTimeDropDown.options[0].selected = 'selected';
        // this.roomsDropDown.options[0].selected = 'selected';

        this.roomsDropDown.name = "rooms";
        this.roomsDropDown.classList.add("conflictRooms");
        this.dayTimeDropDown.name = "dayAndTime";
        this.dayTimeDropDown.classList.add("conflictdayTime");

        this.roomsDropDownLabel = document.createElement("label");
        this.roomsDropDownLabel.innerHTML = "Classroom Selection  ";
        this.roomsDropDownLabel.classList.add("conflictDropDownLabel")
        this.roomsDropDownLabel.htmlFor = "rooms";

        this.dayTimeDropDownLabel = document.createElement("label");
        this.dayTimeDropDownLabel.innerHTML = "Day and Time  ";
        this.dayTimeDropDownLabel.classList.add("conflictDropDownLabel");
        this.dayTimeDropDownLabel.htmlFor = "dayAndTime";


        this.roomDayTimeWarning.style.display = "none";
        this.roomDayTimeWarning.classList.add("roomDayTimeWarning")
        this.dayTimeDropDown.style.cursor = "context-menu";
        this.conflictEdit.style.display = "none";
        this.dayTimeDropDown.disabled = true;

        this.conflictSave.textContent = "Save";

        // this.conflictSave.onclick = function () {
        //     console.log("GENERAL KENOBI");
        //     if (this.roomsDropDown.value != "" && this.dayTimeDropDown.value != "") {
        //       this.conflictSave.disabled = true;
        //       this.dayTimeDropDown.disabled = true;
        //       this.roomsDropDown.disabled = true
        //       this.dayTimeDropDown.style.cursor = "context-menu";
        //       this.roomsDropDown.style.cursor = "context-menu"
        //       this.conflictEdit.style.display = "inline";
        //       this.roomDayTimeWarning.style.display = "none";
        //     }
        //     else {
        //       this.roomDayTimeWarning.style.display = "inline";
        //     }
        //   }

        
    }

    // setDayAndTime(newDay){
    //     this.day = newDay;
    // }
    // setRoom(newRoom){
    //     this.room = newRoom;
    // }

    // getRoom(){
    //     return this.room;
    // }


    setRoomDropDown(emptyRooms){

        if(this.roomsDropDown.options.length > 0){
            for(let i = this.roomsDropDown.options.length; i >= 0; i--) {
                this.roomsDropDown.remove(i);
             }
          
        }

        var option = document.createElement("option");
        option.value = "";
        option.text = "--Select--";
        this.roomsDropDown.appendChild(option);
        for(const room of Object.keys(emptyRooms)){
            var option = document.createElement("option");
            option.value = room;
            option.text = room;
            option.classList.add("conflictRoom")
            this.roomsDropDown.add(option);
        }
    }

    removeFromRoomDropDown(room){
        for(let i = 0; i < this.roomsDropDown.length; i++){
            if(this.roomsDropDown.options[i].value === room){
                this.roomsDropDown.remove(i);
            }
        }
    }

    setDayTimeDropDown(daysAndTimes){
        if(this.dayTimeDropDown.options.length > 0){
            for(let i = this.dayTimeDropDown.options.length; i >= 0; i--) {
                this.dayTimeDropDown.remove(i);
             }
          
        }
        var option = document.createElement("option");
        option.value = "";
        option.text = "--Select--";
        this.dayTimeDropDown.appendChild(option);
        for(let i = 0; i < daysAndTimes.length; i++){
            var option = document.createElement("option");
            option.value = daysAndTimes[i];
            option.text = daysAndTimes[i];
            option.classList.add("conflictDayTime");
            this.dayTimeDropDown.add(option);
          }
    }

    removeFromDayTimeDropDown(dayAndTime){
        for(let i = 0; i < this.dayTimeDropDown.length; i++){
            if(this.dayTimeDropDown.options[i].value === dayAndTime){
                this.dayTimeDropDown.remove(i);
            }
        }
    }






}









