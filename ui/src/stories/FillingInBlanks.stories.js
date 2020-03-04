import React from 'react';
import { storiesOf } from '@storybook/react';
import * as FetchMock from "fetch-mock";
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/css/bootstrap-theme.css';
import Provider from './Provider'
import FillingInBlanks from '../components/common/FillingInBlanks';
import { updateRoomState, updateUserState } from "../redux/Actions";

storiesOf('Filling in blanks', module)
  .addDecorator(story => <Provider story={story()} />)
  .add('with sentence with blanks', () => {
    FetchMock.restore();
    FetchMock.get('glob:*word?*', { wordId: 1, word: "Fill _ the blanks __ of this sentence."});
    const room = { 
      roomId: 1,
      currentRoundId: 1
    };
    store.dispatch(updateRoomState(room));
    const user = {
      userId: 1
    };
    store.dispatch(updateUserState(user));
    FetchMock.post('glob:*word?*', "test");
    return <FillingInBlanks wordId="1" />;
  })
  .add('with sentence', () => {
    FetchMock.restore();
    FetchMock.get('glob:*word?*', { wordId: 1, word: "Fill _ the blanks __ of this sentence.", roundId: 1 });
    const room = { 
      roomId: 1,
      currentRoundId: 1
    };
    store.dispatch(updateRoomState(room));
    const user = {
      userId: 1
    };
    store.dispatch(updateUserState(user));
    FetchMock.post('glob:*word?*', "test");
    return <FillingInBlanks wordId="1" />;
  }); 
