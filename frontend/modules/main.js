import React from 'react'
import { render } from 'react-dom'
import { HashRouter , Link, Route } from 'react-router-dom'
import UsersAdmin from './usersadmin'
import App from './app'
import 'bootstrap/dist/css/bootstrap.css';

render((
  <HashRouter >
    <App>

    </App>
  </HashRouter >
), document.getElementById('app'))
