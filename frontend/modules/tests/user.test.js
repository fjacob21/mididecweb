import User from '../user';

test('A class to keep user info', () => {
  var userinfo = {access:User.ACCESS_SUPER, alias:"root", loginkey:"rootkey", name:"root", user_id:"root"};
  var user = new User(userinfo);
  expect(user.access).toBe(User.ACCESS_SUPER);
  expect(user.alias).toBe('root');
  expect(user.loginkey).toBe('rootkey');
  expect(user.name).toBe('root');
  expect(user.user_id).toBe('root');
  expect(user.isNormalUser).toBe(false);
  expect(user.isManager).toBe(false);
  expect(user.isSuperUser).toBe(true);

  var userinfo = {access:User.ACCESS_NORMAL, alias:"root", loginkey:"rootkey", name:"root", user_id:"root"};
  var user = new User(userinfo);
  expect(user.access).toBe(User.ACCESS_NORMAL);
  expect(user.isNormalUser).toBe(true);
  expect(user.isManager).toBe(false);
  expect(user.isSuperUser).toBe(false);

  var userinfo = {access:User.ACCESS_MANAGER, alias:"root", loginkey:"rootkey", name:"root", user_id:"root"};
  var user = new User(userinfo);
  expect(user.access).toBe(User.ACCESS_MANAGER);
  expect(user.isNormalUser).toBe(false);
  expect(user.isManager).toBe(true);
  expect(user.isSuperUser).toBe(false);

  user = User.getSession();
  expect(user).toBe(null);
  
  var userinfo = {access:User.ACCESS_MANAGER, alias:"root", loginkey:"rootkey", name:"root", user_id:"root"};
  sessionStorage.setItem('userinfo', JSON.stringify(userinfo));
  user = User.getSession();
  expect(user.constructor.name).toBe('User');
});
