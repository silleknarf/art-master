import io from "socket.io-client";
import {
  updateRoomState,
  updateRoundState,
  updateWordsState,
  updateMinigamesState,
  updateUserState } from "./redux/Actions";
import store from "./redux/Store";
import Config from "./constant/Config";

window.io = io;
window.store = store;

const initRoom = async (roomId) => {
  const roomStateRes = await fetch(`${Config.apiurl}/room?roomId=${roomId}`);
  if (roomStateRes.status === 200) {
    const roomState = await roomStateRes.json();
    store.dispatch(updateRoomState(roomState));
    return roomState;
  }
};

const initRound = async (currentRoundId) => {
  let inRound = false;
  if (currentRoundId) {
    const roundStateRes = await fetch(`${Config.apiurl}/round?roundId=${currentRoundId}`);
    if (roundStateRes.status === 200) {
      const roundState = await roundStateRes.json();
      inRound = true;
      store.dispatch(updateRoundState(roundState));
    }
  }

  if (!inRound) {
    store.dispatch(updateRoundState(null));
  }
};

const initWords = async (roomId) => {
  const wordsStateRes = await fetch(`${Config.apiurl}/words?roomId=${roomId}`);
  if (wordsStateRes.status === 200) {
    const wordsState = await wordsStateRes.json();
    store.dispatch(updateWordsState(wordsState));
  }
};

const initMinigames = async () => {
  const minigamesRes = await fetch(`${Config.apiurl}/minigames`);
  if (minigamesRes.status === 200) {
    const minigamesState = await minigamesRes.json();
    store.dispatch(updateMinigamesState(minigamesState));
  }
};

const initUser = (roomId) => {
  const userIdByRoomIdJson = localStorage.getItem("userIdByRoomId");
  let loggedIn = false;
  if (userIdByRoomIdJson !== null) {
    const userIdByRoomId = JSON.parse(userIdByRoomIdJson);
    const userId = userIdByRoomId[roomId];
    if (userId) {
      loggedIn = true;
      store.dispatch(updateUserState({ "userId": parseInt(userId, 10) }));
    }
  }

  if (!loggedIn) {
    store.dispatch(updateUserState( { "userId": null }));
  }
};

export const connectToRoom = async (roomId) => {
  // init
  const room = await initRoom(roomId);
  initRound(room.currentRoundId);
  initWords(roomId);
  initMinigames();
  initUser(roomId);

  // subscribe
  const socket = io(Config.apiurl);
  socket.emit("join", roomId);

  socket.on("room", (roomState) => {
    store.dispatch(updateRoomState(roomState));
  });
  socket.on("round", (roundState) => {
    store.dispatch(updateRoundState(roundState));
  });
  socket.on("words", (wordsState) => {
    store.dispatch(updateWordsState(wordsState));
  });
};