from flask import jsonify

def to_words_dto(word_entities):
    return jsonify(to_words_dict(word_entities))

def to_words_dict(word_entities):
    words = [{
        "wordId": w.WordId,
        "userId": w.UserId,
        "word": w.Word
    } for w in word_entities]
    return words
