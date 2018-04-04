import React from 'react'
import Navbar from './navbar'

class Events extends React.Component{
        constructor(props) {
                super(props);
        }

        render(){
                return (
                        <div className='event'>
                                <div> {this.props.match.params.id} </div>
                        </div>)
        }
}

module.exports = Events;
