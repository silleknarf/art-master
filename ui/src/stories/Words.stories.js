import React from 'react';
import { storiesOf } from '@storybook/react';
import * as FetchMock from "fetch-mock";
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/css/bootstrap-theme.css';
import Provider from './Provider'
import Words from '../components/common/Words';

import { updateWordsState, updateUserState, updateRoomState } from "../redux/Actions";

storiesOf('Words', module)
  .addDecorator(story => <Provider story={story()} />)
  .add('with words', () => {
    FetchMock.restore()
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
    const user = {
      userId: 1
    };
    store.dispatch(updateUserState(user));
    const room = {
      roomId: 1
    };
    store.dispatch(updateRoomState(room));
    FetchMock.get('glob:*words?*', words);
    FetchMock.post('glob:*word?*', (url, opts) => {
      words.push({wordId: 3, word: "Another word!"}); 
      return "test"; 
    });
    return <Words />;
  });