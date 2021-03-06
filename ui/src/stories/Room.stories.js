import React from "react";
import { storiesOf } from "@storybook/react";
import Provider from "./Provider";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/dist/css/bootstrap-theme.css";
import Room from "../components/views/Room";
import "../../public/css/literallycanvas.css";
import * as FetchMock from "fetch-mock";
import store from "../redux/Store";
import { 
  updateRoomState,
  updateRoundState,
  updateWordsState,
  updateMinigamesState,
  updateUserState } from "../redux/Actions";

const setupRoom = (currentRoundId, currentStageId, minigameId, minigameName) => {
  FetchMock.restore()

  const room = {
    roomId: 1,
    roomUsers: [
      { userId: 1, username: "User1"},
      { userId: 2, username: "User2 "}
    ],
    currentRoundId: currentRoundId,
    minigameId: minigameId
  };
  store.dispatch(updateRoomState(room));
  FetchMock.get("glob:*room?*", room);

  const user = {
    userId: 1
  };
  store.dispatch(updateUserState(user));

  const round = {
    stageStateId: currentStageId,
    timeRemaining: 30,
    drawingWordId: 1
  };
  store.dispatch(updateRoundState(round));
  FetchMock.get("glob:*round?*", round);

  const words = [
    {
      wordId: 1,
      userId: 1,
      word: "test"
    },
    {
      wordId: 2,
      userId: 2,
      word: "test2"
    }
  ];
  store.dispatch(updateWordsState(words));
  FetchMock.get("glob:*words?*", words);
  FetchMock.get("glob:*word?*", { wordId: 1, word: "bacon"});

  const ratings = [
    { userId: 1, imageBase64: "1/1.png", username: "User1"},
    { userId: 2, imageBase64: "1/1.png", username: "User2"}
  ];
  FetchMock.get("glob:*ratings?*", ratings);

  FetchMock.get("glob:*images?*", [{ imageId: 1, imageBase64: "1/1.png"}, {imageId: 2, imageBase64: "1/1.png"}]);
  FetchMock.post("glob:*rating?*", "test");

  const minigames = [{ minigameId: minigameId, name: minigameName }];
  store.dispatch(updateMinigamesState(minigames));
  FetchMock.get("glob:*minigames", minigames);
}

storiesOf("Room", module)
  .addDecorator(story => <Provider story={story()} />)
  .add("AM - Round not started", () => {
    setupRoom(null, 0, 1, "Art Master");
    return <Room />;
  })
  .add("AM - Drawing", () => {
    setupRoom(1, 0, 1, "Art Master");
    return <Room />;
  })
  .add("AM - Reviewing", () => {
    setupRoom(97, 1, 1, "Art Master");
    return <Room />;
  })
  .add("AM - Critiquing", () => {
    setupRoom(97, 2, 1, "Art Master");
    return <Room />;
  })
  .add("STD - Round not started", () => {
    setupRoom(null, 0, 2, "Sentenced To Death");
    return <Room />;
  })