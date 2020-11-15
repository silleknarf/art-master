import React from 'react';
import { storiesOf } from '@storybook/react';
import * as FetchMock from "fetch-mock";
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/css/bootstrap-theme.css';
import Draw from '../components/common/Draw';
import "../../public/css/literallycanvas.css";
import Provider from './Provider';

const setupDraw = () => {
  FetchMock.restore();
  FetchMock.post('glob:*image?*', "test");
}
storiesOf('Draw', module)
  .addDecorator(story => <Provider story={story()} />)
  .add('draw', () => {
    setupDraw()
    return <Draw />;
  })
  .add('drawing submitted', () => {
    setupDraw()
    return <Draw drawingSubmitted={ true }/>
  });
