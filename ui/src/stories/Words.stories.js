import React from 'react';
import { storiesOf } from '@storybook/react';
import * as FetchMock from "fetch-mock";
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/css/bootstrap-theme.css';
import Provider from './Provider'
import Words from '../components/common/Words';

import { updateWordsState } from "../redux/Actions";

storiesOf('Words', module)
  .addDecorator(story => <Provider story={story()} />)
  .add('with words', () => {
    FetchMock.restore()
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
    return <Words />;
  });