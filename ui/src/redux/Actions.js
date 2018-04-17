import { UPDATE_ROOM_STATE, UPDATE_ROUND_STATE, UPDATE_USER_STATE } from "./ActionTypes";

export const updateRoomState = roomState => ({ type: UPDATE_ROOM_STATE, payload: roomState });
export const updateRoundState = roundState => ({ type: UPDATE_ROUND_STATE, payload: roundState });
export const updateUserState = userState => ({ type: UPDATE_USER_STATE, payload: userState });