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
      { winnerId: 1, winningImageBase64: '1/1.png', winnerUsername: "User1"}, 
      { winnerId: 2, winningImageBase64: '1/1.png', winnerUsername: "User2"}
    ];
    FetchMock.get('glob:*ratings?*', ratings);
    return <Review roundId="97" />;
  });