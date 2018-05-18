import React from 'react'
import jquery from 'jquery'
import User from './user'
import UserSummary from './usersummary'
import { Table, NavLink, Card, CardTitle, CardText, Button } from 'reactstrap';
import createHistory from "history/createHashHistory"

const history = createHistory();

class UsersAdmin extends React.Component{
        constructor(props) {
                super(props);
                this.state = {users: {count:0, users:[]}, invalid: true};
                this.onEdit = this.onEdit.bind(this);
                this.onDelete = this.onDelete.bind(this);
                this.rmSuccess = this.rmSuccess.bind(this);
                this.rmError = this.rmError.bind(this);
                this.updateUsers();

        }

        updateUsers(){
                var user = User.getSession();
                jquery.ajax({
                type: 'GET',
                url: "/mididec/api/v1.0/users?loginkey="+user.loginkey,
                success: this.success.bind(this),
                error: this.error.bind(this),
                contentType: "application/json",
                dataType: 'json'
                });
        }

        success(data){
                console.debug(data);
                this.state.users = data.users;
                this.state.invalid = false;
                this.setState(this.state);
        }

        error(){

        }

        onEdit(user){
                history.push("/users/"+user.user_id+"/update");
        }

        onDelete(user){
                var loguser = User.getSession();
                if (loguser.user_id != user.user_id) {
                        jquery.ajax({
                        type: 'DELETE',
                        url: "/mididec/api/v1.0/users/"+user.user_id,
                        data: JSON.stringify ({loginkey: loguser.loginkey}),
                        success: this.rmSuccess,
                        error: this.rmError,
                        contentType: "application/json",
                        dataType: 'json'
                        });
                }
        }

        rmSuccess(data){
                this.updateUsers();
        }

        rmError(data){

        }

        render(){
                var users = this.state.users.users.map(user =>
                  <UserSummary user={user} onDelete={this.onDelete} onEdit={this.onEdit}/>
                );
                return (
                        <div className='usersadmin'>
                            <Card body className='users-card'>
                                <CardTitle>Users</CardTitle>
                                {users}
                            </Card>
                        </div>)
        }
}

module.exports = UsersAdmin;
