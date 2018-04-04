import React from 'react'
import { render } from 'react-dom'
import { hashHistory } from 'react-router'
import { HashRouter , Link, Route } from 'react-router-dom'
import Home from './home'
import Events from './events'
import App from './app'

render((
  <HashRouter >
  <App>
    <Link to="/about">About</Link>
    <Route path="/about" component={Home} />
    <Route path="/events/:id" component={Events} />
  </App>
  </HashRouter >
), document.getElementById('app'))
