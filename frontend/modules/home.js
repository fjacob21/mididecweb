import React from 'react'
import Navbar from './navbar'

class Home extends React.Component{
        constructor(props) {
                super(props);
        }

        render(){
                return (
                        <div className='home'>
                                <div> Next talk </div>
                        </div>)
        }
}

module.exports = Home;
