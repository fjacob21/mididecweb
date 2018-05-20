import Event from '../event';
import User from '../user'

test('A class to keep event info', () => {
  var userinfo = {access:User.ACCESS_SUPER, alias:"root", loginkey:"rootkey", name:"root", user_id:"root"};
  var user = new User(userinfo);
  var userinfo2 = {access:User.ACCESS_SUPER, alias:"root2", loginkey:"rootkey2", name:"root2", user_id:"root2"};
  var user2 = new User(userinfo2);
  var eventinfo = { event_id: 'event',
                    title:'title',
                    max_attendee:20,
                    description:'description',
                    start:'2018-04-26T13:00:00Z',
                    duration:3600,
                    end:'2018-04-26T14:00:00Z',
                    location:'location',
                    organizer_name:'organizer_name',
                    organizer_email:'organizer_email',
                    owner_id: '123',
                    attendees:[userinfo],
                    waitings:[userinfo],
                };

  var event = new Event(eventinfo);
  expect(event.constructor.name).toBe('Event');
  expect(event.event_id).toBe('event');
  expect(event.owner_id).toBe('123');
  expect(event.title).toBe('title');
  expect(event.max_attendee).toBe(20);
  expect(event.description).toBe('description');
  expect(event.start).toBe('2018-04-26T13:00:00Z');
  expect(event.duration).toBe(3600);
  expect(event.end).toBe('2018-04-26T14:00:00Z');
  expect(event.location).toBe('location');
  expect(event.organizer_name).toBe('organizer_name');
  expect(event.organizer_email).toBe('organizer_email');
  expect(event.attendees.constructor.name).toBe('Array');
  expect(event.attendees.length).toBe(1);
  expect(event.attendees[0].constructor.name).toBe('User');
  expect(event.find_attendee(user)).toBeDefined();
  expect(event.find_attendee(user2)).toBeNull();
  expect(event.find_attendee(null)).toBeNull();
  expect(event.waitings.length).toBe(1);
  expect(event.waitings[0].constructor.name).toBe('User');
  expect(event.find_waiting(user)).toBeDefined();
  expect(event.find_waiting(user2)).toBeNull();
  expect(event.find_waiting(null)).toBeNull();
});
