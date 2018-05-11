import React from 'react';

import { storiesOf } from '@storybook/react';
import Provider from './Provider'

import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/css/bootstrap-theme.css';

import Room from '../components/views/Room';
import "../../public/css/literallycanvas.css";
import * as FetchMock from "fetch-mock";

import store from "../redux/Store";
import { updateRoomState, updateRoundState, updateWordsState } from "../redux/Actions";

const setupRoom = () => {
  FetchMock.restore()

  const room = { 
    roomId: 1,
    roomUsers: [
      { userId: 1, username: "User1"}, 
      { userId: 2, username: "User2 "}
    ],
    currentRoundId: 1
  };
  store.dispatch(updateRoomState(room));
  FetchMock.get('glob:*room?*', room);

  const round = { 
    stageStateId: 0,
    timeRemaining: 30
  };
  store.dispatch(updateRoundState(round));
  FetchMock.get("glob:*round*", round);

  const words = [
    {
      wordId: 1,
      word: "test"
    },
    {
      wordId: 2,
      word: "test2"
    }
  ];
  store.dispatch(updateWordsState(words));
  FetchMock.get('glob:*words?*', words);
}

storiesOf('Room', module)
  .addDecorator(story => <Provider story={story()} />)
  .add('Room', () => { 
    setupRoom();
    return <Room />;
  });