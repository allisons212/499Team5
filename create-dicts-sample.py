def create_partial_section_entry(self, faculty_ass="", room_pref="", time_pref="", day_pref="",
                                     room_ass="", time_ass="", day_ass="", seats_open=""):
        """
        Creates a dictionary section for a specific section
        (e.g., "CS/CS100-01")

        Args:
            faculty_ass (str, optional): Faculty Assignment. Defaults to "".
            room_pref (str, optional): Room Preference. Defaults to "".
            time_pref (str, optional): Time Preference. Defaults to "".
            day_pref (str, optional): Day Preference. Defaults to "".
            room_ass (str, optional): Room Assignment. Defaults to "".
            time_ass (str, optional): Time Assignment. Defaults to "".
            day_ass (str, optional): Day Assignment. Defaults to "".
            seats_open (str, optional): Seats Open. Defaults to "".

        Returns:
            Dictionary: Returns a dictionary keyed by all the parameters.
        """
        partial_dict = {
                        ColumnHeaders.FAC_ASSIGN.value : faculty_ass,
                        ColumnHeaders.ROOM_PREF.value : room_pref,
                        ColumnHeaders.TIME_PREF.value : time_pref,
                        ColumnHeaders.DAY_PREF.value : day_pref,
                        ColumnHeaders.ROOM_ASS.value : room_ass,
                        ColumnHeaders.TIME_ASS.value : time_ass,
                        ColumnHeaders.DAY_ASS.value : day_ass,
                        ColumnHeaders.SEATS_OPEN.value : seats_open,
                       }
        return partial_dict
    # End of create_partial_section_entry
    
    
    def create_full_section_entry(self, section_name="", faculty_ass="", room_pref="", time_pref="", day_pref="",
                                     room_ass="", time_ass="", day_ass="", seats_open=""):
        """
        Creates a dictionary section for a whole section.
        Can be used to create a whole new section dict to update to a department header (e.g., "CS", "ECE").

        Args:
            section_name (str, optional): Class Section. Defaults to "".
            faculty_ass (str, optional): Faculty Assignment. Defaults to "".
            room_pref (str, optional): Room Preference. Defaults to "".
            time_pref (str, optional): Time Preference. Defaults to "".
            day_pref (str, optional): Day Preference. Defaults to "".
            room_ass (str, optional): Room Assignment. Defaults to "".
            time_ass (str, optional): Time Assignment. Defaults to "".
            day_ass (str, optional): Day Assignment. Defaults to "".
            seats_open (str, optional): Seats Open. Defaults to "".

        Returns:
            Dictionary: Returns a dictionary keyed by all the parameters.
        """
        partial_dict = {
                        ColumnHeaders.FAC_ASSIGN.value : faculty_ass,
                        ColumnHeaders.ROOM_PREF.value : room_pref,
                        ColumnHeaders.TIME_PREF.value : time_pref,
                        ColumnHeaders.DAY_PREF.value : day_pref,
                        ColumnHeaders.ROOM_ASS.value : room_ass,
                        ColumnHeaders.TIME_ASS.value : time_ass,
                        ColumnHeaders.DAY_ASS.value : day_ass,
                        ColumnHeaders.SEATS_OPEN.value : seats_open,
                       }
        full_dict = { section_name : partial_dict }
        return full_dict
    # End of create_full_section_entry