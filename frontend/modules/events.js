import React from 'react'

class Events extends React.Component{
        constructor(props) {
                super(props);
        }

        render(){
                return (
                        <div className='event'>
                                <div> Event:{this.props.match.params.id} </div>
                        </div>)
        }
}

module.exports = Events;
