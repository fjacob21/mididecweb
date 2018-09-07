import React from 'react'

class AttendeeIcon extends React.Component{

        constructor(props) {
                super(props);
        }

        render(){
                var avatar = <i className="material-icons md-light attendee-avatar">account_circle</i>
                if (this.props.attendee.have_avatar) {
                        var avatar_path = "/mididec/api/v1.0/users/" + this.props.attendee.user_id+"/avatar?sizex=100&sizey=110&id=" + new Date().getTime();
                        avatar = <img src={avatar_path} className="attendee-avatar"/>
                }
                var alias = this.props.attendee.alias;
                if (this.props.noname)
                        alias = "";
                var className = this.props.className + " attendeeicon " ;
                return (
                        <div className={className}>
                                {avatar}
                                {alias}
                        </div>
                );
        }
}

module.exports = AttendeeIcon;
