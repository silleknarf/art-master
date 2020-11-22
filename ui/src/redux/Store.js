// src/js/store/index.js
import { createStore } from "redux";
import rootReducer from "./RootReducer";
import { updateUserState, updateRoomState } from "../redux/Actions";

const store = createStore(rootReducer);

const userId = localStorage.getItem("userId");
if (userId !== null) {
    store.dispatch(updateUserState({ "userId": parseInt(userId, 10) }))
}

const roomId = localStorage.getItem("roomId");
if (roomId !== null) {
    store.dispatch(updateRoomState({ "roomId": parseInt(roomId, 10) }))
}

export default store;