import React from 'react';
import { storiesOf } from '@storybook/react';
import Critic from '../components/common/Critic';
import * as FetchMock from "fetch-mock";

storiesOf('Critic', module)
  .add('with images', () => {
      FetchMock.restore()  
      FetchMock.get('glob:*images?*', [{ imageId: 1, location: '1/1.png'}, {imageId: 2, location: '1/1.png'}]);
      FetchMock.post('glob:*rating?*', "test");
      return <Critic />;
    });