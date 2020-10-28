import React from 'react';
import { storiesOf } from '@storybook/react';
import * as FetchMock from "fetch-mock";
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/css/bootstrap-theme.css';
import Provider from './Provider'
import RoomUsers from '../components/common/RoomUsers';
import { updateRoomState, updateUserState } from "../redux/Actions";

storiesOf('RoomUsers', module)
  .addDecorator(story => <Provider story={story()} />)
  .add('with users', () => {
    FetchMock.restore()
    const room = {
      roomId: 1,
      roomUsers: [
        { userId: 1, username: "User1", score: 0},
        { userId: 2, username: "User2 ", score: 10}
      ],
      currentRoundId: 1
    };
    store.dispatch(updateRoomState(room));
    FetchMock.get('glob:*room?*', room);
    const user = {
      userId: 1
    };
    store.dispatch(updateUserState(user));
    return <RoomUsers />;
  });