import React from 'react';
import { storiesOf } from '@storybook/react';
import * as FetchMock from "fetch-mock";
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/css/bootstrap-theme.css';
import Draw from '../components/common/Draw';
import "../../public/css/literallycanvas.css";

const setupDraw = () => {
  FetchMock.restore();
  FetchMock.post('glob:*image?*', "test");
}
storiesOf('Draw', module)
  .add('draw', () => {
    setupDraw()
    return <Draw />;
  })
  .add('drawing submitted', () => {
    setupDraw()
    return <Draw drawingSubmitted={ true }/>
  });
