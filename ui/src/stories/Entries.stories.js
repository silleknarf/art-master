import React from 'react';
import { storiesOf } from '@storybook/react';
import * as FetchMock from "fetch-mock";
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/css/bootstrap-theme.css';
import Provider from './Provider'
import Entries from '../components/common/Entries';

import { updateEntriesState, updateUserState, updateRoomState, updateMinigamesState } from "../redux/Actions";

const setupEntries = (entryComponents, entries) => {
  FetchMock.restore()
  store.dispatch(updateEntriesState(entries));
  const user = {
    userId: 1
  };
  store.dispatch(updateUserState(user));
  const room = {
    roomId: 1,
    minigameId: 1
  };
  store.dispatch(updateRoomState(room));
  const minigames = [
    { 
      minigameId: 1, 
      entryComponents: entryComponents
    }
  ]
  store.dispatch(updateMinigamesState(minigames));
  FetchMock.get('glob:*entries?*', entries);
  FetchMock.post('glob:*entry?*', (url, opts) => {
    const testEntry = { 
      entryId: 1,
      entryComponents: [{
        entryComponentId: 1,
        key: "Word",
        value: "Another word!"
      }]
    };

    entries.push(testEntry);
    return "test";
  });
  return <Entries />;
};

storiesOf('Entries', module)
  .addDecorator(story => <Provider story={story()} />)
  .add('with words', () => {
    const entries = [
      { 
        entryId: 1,
        entryComponents: [{
          entryComponentId: 1,
          key: "Word",
          value: "Word!"
        }]
      },
      { 
        entryId: 2,
        entryComponents: [{
          entryComponentId: 1,
          key: "Word",
          value: "Word 2.0"
        }]
      }
    ];
    setupEntries(["Word"], entries)
    return <Entries />;
  });