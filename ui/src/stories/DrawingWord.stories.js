import React from 'react';
import { storiesOf } from '@storybook/react';
import * as FetchMock from "fetch-mock";
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/css/bootstrap-theme.css';
import DrawingEntry from '../components/common/DrawingEntry';

storiesOf('DrawingEntry', module)
  .add('with word', () => {
    FetchMock.restore();
    const baconEntry = { 
      entryId: 1,
      entryComponents: [{
        entryComponentId: 1,
        key: "Word",
        value: "bacon"
      }]
    };
    FetchMock.get('glob:*entry?*', baconEntry);
    return <DrawingEntry entryId="1" />;
  });
