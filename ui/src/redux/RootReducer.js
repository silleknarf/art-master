import { UPDATE_ROOM_STATE, UPDATE_ROUND_STATE } from "./ActionTypes";

const initialState = {
  room: null,
  round: null
};

const rootReducer = (state = initialState, action) => {
  switch (action.type) {
    case UPDATE_ROOM_STATE:
      return { ...state, room: action.payload };
    case UPDATE_ROUND_STATE:
      return { ...state, round: action.payload };
    default:
      return state;
  }
};

export default rootReducer;