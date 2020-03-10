import React from 'react';
import { storiesOf } from '@storybook/react';
import * as FetchMock from "fetch-mock";
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/css/bootstrap-theme.css';
import Review from '../components/common/Review';

storiesOf('Review', module)
  .add('with images', () => {
    FetchMock.restore()
    const ratings = [
      { winnerId: 1, winningImageBase64: '1/1.png', winnerUsername: "User1", votes: 1}, 
      { winnerId: 2, winningImageBase64: '1/1.png', winnerUsername: "User2", votes: 2}
    ];
    FetchMock.get('glob:*ratings?*', ratings);
    return <Review roundId="97" />;
  })
  .add('with words', () => {
    FetchMock.restore()
    const ratings = [
      { winnerId: 1, winnerUsername: "User1", word: "test", votes: 1}, 
      { winnerId: 2, winnerUsername: "User2", word: "test 2", votes: 2}
    ];
    FetchMock.get('glob:*ratings?*', ratings);
    return <Review roundId="97" />;
  });