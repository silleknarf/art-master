from flask import jsonify
from collections import defaultdict

def to_entries_json(entry_entities, entry_component_entities):
    return jsonify(to_entries_dto(entry_entities, entry_component_entities))

def to_entry_json(entry_entity, entry_component_entities):
    return jsonify(to_entries_dto([entry_entity], entry_component_entities)[0])

def to_entries_dto(entry_entities, entry_components_entities):
    entries_components_dict = defaultdict(list)
    for ece in entry_components_entities:
        entries_components_dict[ece.EntryId].append(ece)

    entries = []
    for entry_entity in entry_entities:
        entry_components_entities = entries_components_dict[entry_entity.EntryId]
        entry = {
            "entryId": entry_entity.EntryId,
            "userId": entry_entity.UserId,
            "entryComponents": to_entry_components_dto(entry_components_entities)
        }
        entries.append(entry)

    return entries

def to_entry_components_dto(entry_components_entities):
    entry_components = [{
        "entryId": e.EntryId,
        "key": e.Key,
        "value": e.Value
    } for e in entry_components_entities]
    return entry_components
