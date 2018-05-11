import React from 'react';
import { storiesOf } from '@storybook/react';
import * as FetchMock from "fetch-mock";
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/css/bootstrap-theme.css';
import Provider from './Provider'
import RoundInfo from '../components/common/RoundInfo';
import { updateRoundState } from "../redux/Actions";

storiesOf('RoundInfo', module)
  .addDecorator(story => <Provider story={story()} />)
  .add('roundInfo', () => {
    FetchMock.restore();
    const round = { 
      stageStateId: 0,
      timeRemaining: 30
    };
    store.dispatch(updateRoundState(round));
    FetchMock.get("glob:*round*", round);
    return <RoundInfo />;
  });