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
                                {this.props.children}
                        </div>)
        }
}

module.exports = App;
