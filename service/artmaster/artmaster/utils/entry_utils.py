from flask import jsonify

def to_entry_components_json(entry_entities, entry_components_entities):
    return jsonify(to_entry_components_dto(entry_entities, entry_components_entities))

def to_entry_components_dto(entry_entities, entry_components_entities):
    entry_entities_dict = { e.EntryId:e for e in entry_entities }
    entry_components = [{
        "entryId": e.EntryId,
        "userId": entry_entities_dict[e.EntryId].UserId,
        "key": e.Key,
        "value": e.Value
    } for e in entry_components_entities]
    return entry_components
