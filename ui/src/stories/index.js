import React from 'react';

import { storiesOf } from '@storybook/react';
import { action } from '@storybook/addon-actions';
import { linkTo } from '@storybook/addon-links';

import { Button, Welcome } from '@storybook/react/demo';
import Critic from '../components/common/Critic';
import DrawingWord from '../components/common/DrawingWord';
import Draw from '../components/common/Draw';
import "../../public/css/literallycanvas.css"

storiesOf('Critic', module)
  .add('with images', () => <Critic roundId="53" />);
storiesOf('DrawingWord', module)
  .add('with word', () => <DrawingWord wordId="1" />);

storiesOf('Draw', module)
  .add('draw', () => <Draw />);


