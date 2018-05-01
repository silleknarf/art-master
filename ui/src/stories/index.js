import React from 'react';

import { storiesOf } from '@storybook/react';
import { action } from '@storybook/addon-actions';
import { linkTo } from '@storybook/addon-links';

import { Button, Welcome } from '@storybook/react/demo';
import Critic from '../components/common/Critic';
import DrawingWord from '../components/common/DrawingWord';
import Draw from '../components/common/Draw';
import Review from '../components/common/Review';
import Lobby from '../components/views/Lobby';
import Room from '../components/views/Room';
import "../../public/css/literallycanvas.css"
import * as FetchMock from "fetch-mock"


storiesOf('Critic', module)
  .add('with images', () => <Critic roundId="53" />);

storiesOf('DrawingWord', module)
  .add('with word', () => <DrawingWord wordId="1" />);

FetchMock.post('*', "test");
storiesOf('Draw', module)
  .add('draw', () => <Draw />);
FetchMock.restore();

storiesOf('Review', module)
  .add('with images', () => <Review roundId="97" />);

// We need to allow in the props at any stage
//storiesOf('RoomUsers', module)
  //.add('with users', () => <RoomUsers rooom" />);

// We need to allow in the props at any stage
//storiesOf('RoundInfo', module)
  //.add('roundInfo', () => <RoundInfo roundId="97" />);

// We need to allow in the props at any stage
//storiesOf('Words', module)
  //.add('with words', () => <Words roomId="1" />);

storiesOf('Lobby', module)
  .add('Lobby', () => <Lobby room={room} round={round} user={user} />);

const room = { roomId: 1 };
const user = { userId: 1 };
const round = { roundId: 1 };

// We need to allow in the props at any stage
//storiesOf('Room', module)
  //.add('Room', () => <Room room={room} round={round} user={user} />);



