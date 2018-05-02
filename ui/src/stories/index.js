import React from 'react';

import { storiesOf } from '@storybook/react';
import { action } from '@storybook/addon-actions';
import { linkTo } from '@storybook/addon-links';
import Provider from './Provider'

import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/css/bootstrap-theme.css';

import { Button, Welcome } from '@storybook/react/demo';
import Critic from '../components/common/Critic';
import DrawingWord from '../components/common/DrawingWord';
import Draw from '../components/common/Draw';
import Review from '../components/common/Review';
import RoomUsers from '../components/common/RoomUsers';
import RoundInfo from '../components/common/RoundInfo';
import Words from '../components/common/Words';
import Lobby from '../components/views/Lobby';
import Room from '../components/views/Room';
import "../../public/css/literallycanvas.css";
import * as FetchMock from "fetch-mock";

import store from "../redux/Store";
import { updateRoomState, updateRoundState, updateWordsState } from "../redux/Actions";


FetchMock.get('glob:*images?*', [{ imageId: 1, location: '1/1.png'}, {imageId: 2, location: '1/1.png'}]);
FetchMock.post('glob:*rating?*', "test");
storiesOf('Critic', module)
  .add('with images', () => <Critic />);

FetchMock.get('glob:*word?*', { wordId: 1, word: "test"});
storiesOf('DrawingWord', module)
  .add('with word', () => <DrawingWord wordId="1" />);

FetchMock.post('glob:*image?*', "test");
storiesOf('Draw', module)
  .add('draw', () => <Draw />);

const ratings = [
  { winnerId: 1, winningImageLocation: '1/1.png', winnerUsername: "User1"}, 
  { winnerId: 2, winningImageLocation: '1/1.png', winnerUsername: "User2"}
];
FetchMock.get('glob:*ratings?*', ratings);
storiesOf('Review', module)
  .add('with images', () => <Review roundId="97" />);

const room = { 
  roomId: 1,
  roomUsers: [
    { userId: 1, username: "User1"}, 
    { userId: 2, username: "User2 "}
  ],
  currentRoundId: 1
};
store.dispatch(updateRoomState(room));
FetchMock.get('glob:*room?*', room);

storiesOf('RoomUsers', module)
  .addDecorator(story => <Provider story={story()} />)
  .add('with users', () => <RoomUsers /> );

const round = { 
  stageStateId: 0,
  timeRemaining: 30
};
store.dispatch(updateRoundState(round));
FetchMock.get("glob:*round*", round);
storiesOf('RoundInfo', module)
  .addDecorator(story => <Provider story={story()} />)
  .add('roundInfo', () => <RoundInfo />);

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

storiesOf('Words', module)
  .addDecorator(story => <Provider story={story()} />)
  .add('with words', () => <Words />);

const user = { userId: 1 };
//store.dispatch
storiesOf('Lobby', module)
  .add('Lobby', () => <Lobby />);

storiesOf('Room', module)
  .addDecorator(story => <Provider story={story()} />)
  .add('Room', () => <Room />);



