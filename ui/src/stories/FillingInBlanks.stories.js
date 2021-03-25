import React from 'react';
import { storiesOf } from '@storybook/react';
import * as FetchMock from "fetch-mock";
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/css/bootstrap-theme.css';
import Provider from './Provider'
import FillingInBlanks from '../components/common/FillingInBlanks';
import { updateRoomState, updateRoundState, updateUserState } from "../redux/Actions";

storiesOf('Filling in blanks', module)
  .addDecorator(story => <Provider story={story()} />)
  .add('with sentence with blanks', () => {
    FetchMock.restore();
    const entry = {
      entryId: 1,
      entryComponents: [
        {
          key: "Sentence",
          value: "Fill _ the blanks __ of this sentence."
        }
      ]
    }
    FetchMock.get('glob:*entry?*', entry);
    const room = {
      roomId: 1,
      currentRoundId: 1
    };
    store.dispatch(updateRoomState(room));
    const user = {
      userId: 1
    };
    store.dispatch(updateUserState(user));
    const round = {
      timeRemaining: 1000
    };
    store.dispatch(updateRoundState(round));
    FetchMock.post('glob:*entry?*', "test");
    return <FillingInBlanks entryId="1" />;
  });
