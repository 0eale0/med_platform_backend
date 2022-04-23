def changed_fields_with_values(history_obj):
    fields = []
    if history_obj.prev_record:
        delta = history_obj.diff_against(history_obj.prev_record)

        for change in delta.changes:
            fields.append(str("{} changed from {} to {}".format(change.field, change.old, change.new)))
        return fields
    return None


def get_dict_with_changes(obj, max_count_of_changes):
    result = {}
    history_obj = obj.history.last()
    for i in range(max_count_of_changes):
        changes = changed_fields_with_values(history_obj)
        key = history_obj.history_date.strftime("%Y-%m-%d %H:%M:%S")
        result[key] = changes
        history_obj = history_obj.next_record

        if not history_obj:
            break

    return result