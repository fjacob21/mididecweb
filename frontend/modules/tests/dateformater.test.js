import React from 'react';
import DateFormater from '../dateformater';
import renderer from 'react-test-renderer';

test('A class to format a Date', () => {
  var dateStr = '2018-04-05T23:20:19Z';
  var date = new Date(dateStr);
  var dateform1 = new DateFormater(dateStr);
  var dateform2 = new DateFormater(date);
  expect(typeof dateform1.getDate()).toBe('object');
  expect(dateform1.getDate().constructor.name).toBe('Date');
  expect(typeof dateform2.getDate()).toBe('object');
  expect(dateform2.getDate().constructor.name).toBe('Date');
  expect(dateform1.getTimeText()).toBe('18h20');
  expect(dateform1.getDateText()).toBe('jeudi 5 avril 2018');
  expect(dateform2.getTimeText()).toBe('18h20');
  expect(dateform2.getDateText()).toBe('jeudi 5 avril 2018');

});
