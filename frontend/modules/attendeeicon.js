import React from 'react'
import User from './user'

class AttendeeIcon extends React.Component{

        constructor(props) {
                super(props);
        }

        render(){
                var user = User.getSession();
                var avatar = <i className="material-icons md-light attendee-avatar">account_circle</i>
                if (this.props.attendee.have_avatar) {
                        var avatar_path = "/mididec/api/v1.0/users/" + this.props.attendee.user_id+"/avatar?sizex=100&sizey=110&id=" + new Date().getTime();
                        avatar = <img src={avatar_path} className="attendee-avatar"/>
                }
                var alias = this.props.attendee.alias;
                if (user && (user.isManager || user.isSuperUser)) {
                  alias = this.props.attendee.name;
                }
                if (this.props.noname)
                        alias = "";
                var className = this.props.className + " attendeeicon " ;
                return (
                        <div className={className}>
                                {avatar}
                                <div className='attendeeicon-name'>{alias}</div>
                        </div>
                );
        }
}

module.exports = AttendeeIcon;
