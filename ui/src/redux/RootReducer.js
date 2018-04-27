import { UPDATE_ROOM_STATE, UPDATE_ROUND_STATE, UPDATE_USER_STATE } from "./ActionTypes";

const initialState = {
  room: null,
  round: null,
  user: null
};

const rootReducer = (state = initialState, action) => {
  switch (action.type) {
    case UPDATE_ROOM_STATE:
      return { ...state, room: action.payload };
    case UPDATE_ROUND_STATE:
      return { ...state, round: action.payload };
    case UPDATE_USER_STATE:
      return { ...state, user: action.payload };
    default:
      return state;
  }
};

export default rootReducer;