import React from 'react'
import { render } from 'react-dom'
import { hashHistory } from 'react-router'
import { HashRouter , Link, Route } from 'react-router-dom'
import Home from './home'
import Events from './events'
import MailingList from './mailinglist'
import App from './app'

render((
  <HashRouter >
    <App>
      <Route exact path="/" component={Home} />
      <Route path="/events/:id" component={Events} />
      <Route path="/mailinglist" component={MailingList} />
    </App>
  </HashRouter >
), document.getElementById('app'))
