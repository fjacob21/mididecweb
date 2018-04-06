import React from 'react';
import Navbar from '../navbar';
import renderer from 'react-test-renderer';

test('Link changes the class when hovered', () => {
  const component = renderer.create(
    <Navbar></Navbar>
  );
  let tree = component.toJSON();
  expect(tree).toMatchSnapshot();
});
