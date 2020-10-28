import React from 'react';
import { storiesOf } from '@storybook/react';
import * as FetchMock from "fetch-mock";
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/css/bootstrap-theme.css';
import DrawingWord from '../components/common/DrawingWord';

storiesOf('DrawingWord', module)
  .add('with word', () => {
    FetchMock.restore();
    FetchMock.get('glob:*word?*', { wordId: 1, word: "bacon"});
    return <DrawingWord wordId="1" />;
  });
