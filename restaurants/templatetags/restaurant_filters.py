from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    if dictionary is None:
        return None
    
    # Split the key into parts for nested access
    keys = key.split('.')
    
    # Traverse the dictionary
    for k in keys:
        if isinstance(dictionary, dict):
            dictionary = dictionary.get(k)
        elif isinstance(dictionary, list) and k.isdigit():
            index = int(k)
            if 0 <= index < len(dictionary):
                dictionary = dictionary[index]
            else:
                return None
        else:
            return None
    
    return dictionary

@register.filter
def get_slot_time(hours, day_slot):
    """
    Get the time for a specific day and slot from hours data.
    Usage: {{ form.initial.hours|get_slot_time:'monday.0.start' }}
    """
    day, slot_index, time_type = day_slot.split('.')
    try:
        return hours.get(day, [])[int(slot_index)][time_type]
    except (KeyError, IndexError):
        return ''

@register.filter
def get_field(form, field_name):
    """
    Get a form field by its name.
    Usage: {{ form|get_field:'monday_start_0' }}
    """
    return form[field_name]

@register.filter
def get_field(form, field_name):
    """
    Get a form field by its name.
    Usage: {{ form|get_field:'monday_start_0' }}
    """
    return form[field_name]