def working_hours_as_string(data):
    data["location"]["opening_hours"]["weekly_text"] = ", ".join(
        data["location"]["opening_hours"]["weekly_text"])
    return data


def working_hours_as_list(data):
    data["location"]["opening_hours"]["weekly_text"] = (
        data["location"]["opening_hours"]["weekly_text"].split(", "))
    return data
