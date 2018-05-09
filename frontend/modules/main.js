import React from 'react'
import { render } from 'react-dom'
import { hashHistory } from 'react-router'
import { HashRouter , Link, Route } from 'react-router-dom'
import Home from './home'
import Events from './events'
import CreateEvent from './createevent'
import CreateUser from './createuser'
import MailingList from './mailinglist'
import App from './app'
import Login from './login'
import 'bootstrap/dist/css/bootstrap.css';

render((
  <HashRouter >
    <App>
      <Route exact path="/" component={Home} />
      <Route path="/login" component={Login} />
      <Route path="/events/:id" component={Events} />
      <Route path="/mailinglist" component={MailingList} />
      <Route path="/createevent" component={CreateEvent} />
      <Route path="/createuser" component={CreateUser} />
    </App>
  </HashRouter >
), document.getElementById('app'))
