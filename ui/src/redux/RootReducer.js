import { UPDATE_ROOM_STATE, UPDATE_ROUND_STATE, UPDATE_USER_STATE, UPDATE_WORDS_STATE, UPDATE_MINIGAMES_STATE } from "./ActionTypes";

const initialState = {
  room: null,
  round: null,
  user: null,
  words: [],
  minigames: []
};

const rootReducer = (state = initialState, action) => {
  switch (action.type) {
    case UPDATE_ROOM_STATE:
      return { ...state, room: action.payload };
    case UPDATE_ROUND_STATE:
      return { ...state, round: action.payload };
    case UPDATE_USER_STATE:
      return { ...state, user: action.payload };
    case UPDATE_WORDS_STATE:
      return { ...state, words: action.payload };
    case UPDATE_MINIGAMES_STATE:
      return { ...state, minigames: action.payload };
    default:
      return state;
  }
};

export default rootReducer;