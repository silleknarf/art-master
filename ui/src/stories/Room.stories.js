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

const setupRoom = (currentRoundId, currentStageId) => {
  FetchMock.restore()

  const room = { 
    roomId: 1,
    roomUsers: [
      { userId: 1, username: "User1"}, 
      { userId: 2, username: "User2 "}
    ],
    currentRoundId: currentRoundId
  };
  store.dispatch(updateRoomState(room));
  FetchMock.get('glob:*room?*', room);

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
      word: "test"
    },
    {
      wordId: 2,
      word: "test2"
    }
  ];
  store.dispatch(updateWordsState(words));
  FetchMock.get('glob:*words?*', words);
  FetchMock.get('glob:*word?*', { wordId: 1, word: "bacon"});

  const ratings = [
    { winnerId: 1, winningImageLocation: '1/1.png', winnerUsername: "User1"}, 
    { winnerId: 2, winningImageLocation: '1/1.png', winnerUsername: "User2"}
  ];
  FetchMock.get('glob:*ratings?*', ratings);

  FetchMock.get('glob:*images?*', [{ imageId: 1, location: '1/1.png'}, {imageId: 2, location: '1/1.png'}]);
  FetchMock.post('glob:*rating?*', "test");
}

storiesOf('Room', module)
  .addDecorator(story => <Provider story={story()} />)
  .add('Round not started', () => { 
    setupRoom(null, 0);
    return <Room />;
  })
  .add('Drawing', () => { 
    setupRoom(1, 0);
    return <Room />;
  })
  .add('Reviewing', () => { 
    setupRoom(97, 1);
    return <Room />;
  })
  .add('Critiquing', () => { 
    setupRoom(97, 2);
    return <Room />;
  });