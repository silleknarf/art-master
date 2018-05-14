import React from 'react';
import { storiesOf } from '@storybook/react';
import * as FetchMock from "fetch-mock";
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/css/bootstrap-theme.css';
import Lobby from '../components/views/Lobby';

storiesOf('Lobby', module)
  .add('Lobby', () => <Lobby />);
