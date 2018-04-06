import React , { Component, PropTypes } from 'react'
import { browserHistory} from 'react-router'
import Navbar from './navbar'

class App extends React.Component{
        constructor(props) {
                super(props);
        }

        componentDidMount(){
        }

        componentWillUnmount(){
        }

        render(){
                return (
                        <div className='app'>
                                <Navbar prev='' next=''></Navbar>
                                <div className='content'>{this.props.children}</div>

                        </div>)
        }
}

module.exports = App;
