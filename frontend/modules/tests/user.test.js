import User from '../user';

test('A class to keep user info', () => {
  var userinfo = { access:User.ACCESS_SUPER,
                   alias:"root",
                   loginkey:"rootkey",
                   name:"root",
                   infotype:"normal",
                   password:"password",
                   phone:"phone",
                   useemail:true,
                   usesms:true,
                   profile:"profile",
                   validated:true,
                   smsvalidated:true,
                   lastlogin:"root",
                   email:"email",
                   user_id:"root"};
  var user = new User(userinfo);
  expect(user.access).toBe(User.ACCESS_SUPER);
  expect(user.alias).toBe('root');
  expect(user.loginkey).toBe('rootkey');
  expect(user.name).toBe('root');
  expect(user.user_id).toBe('root');
  expect(user.password).toBe('password');
  expect(user.phone).toBe('phone');
  expect(user.useemail).toBe(true);
  expect(user.usesms).toBe(true);
  expect(user.profile).toBe('profile');
  expect(user.validated).toBe(true);
  expect(user.smsvalidated).toBe(true);
  expect(user.email).toBe('email');
  expect(user.lastlogin).toBe('root');
  expect(user.isNormalUser).toBe(false);
  expect(user.isManager).toBe(false);
  expect(user.isSuperUser).toBe(true);

  var userinfo = {access:User.ACCESS_NORMAL, alias:"root", loginkey:"rootkey", name:"root", user_id:"root"};
  var user = new User(userinfo);
  expect(user.access).toBe(User.ACCESS_NORMAL);
  expect(user.isNormalUser).toBe(true);
  expect(user.isManager).toBe(false);
  expect(user.isSuperUser).toBe(false);
  expect(user.email).toBeUndefined();
  expect(user.password).toBeUndefined();
  expect(user.useemail).toBeUndefined();
  expect(user.usesms).toBeUndefined();
  expect(user.profile).toBeUndefined();
  expect(user.validated).toBeUndefined();
  expect(user.smsvalidated).toBeUndefined();
  expect(user.lastlogin).toBeUndefined();

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
