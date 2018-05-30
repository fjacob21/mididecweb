import React , { Component, PropTypes } from 'react'
import { browserHistory} from 'react-router'
import jquery from 'jquery'
import User from './user'
import createHistory from "history/createHashHistory"
import {
  Collapse,
  Navbar as NB,
  NavbarToggler,
  NavbarBrand,
  Nav,
  NavItem,
  NavLink,
  UncontrolledDropdown,
  DropdownToggle,
  DropdownMenu,
  DropdownItem } from 'reactstrap';

const history = createHistory();
class Navbar extends React.Component{
        constructor(props) {
                super(props);
                this.onHome = this.onHome.bind(this);
                this.onCreate = this.onCreate.bind(this);
                this.onUsersAdmin = this.onUsersAdmin.bind(this);
                this.onEventsAdmin = this.onEventsAdmin.bind(this);
                this.onCreateEvent = this.onCreateEvent.bind(this);
                this.onLogin = this.onLogin.bind(this);
                this.onLogout = this.onLogout.bind(this);
                this.logoutSuccess = this.logoutSuccess.bind(this);
                this.logoutError = this.logoutError.bind(this);
                this.onProfile = this.onProfile.bind(this);
                this.toggle = this.toggle.bind(this);
                this.onLeave = this.onLeave.bind(this);
                this.state = {
                  isOpen: false
                };
        }

        componentDidMount(){
        }

        componentWillUnmount(){
        }

        onHome(event){
                event.preventDefault();
                this.toggle();
                history.replace("/");
        }

        onProfile(event){
                var user = User.getSession();
                event.preventDefault();
                this.toggle();
                history.replace("/users/" + user.user_id + '/update');
        }

        onLogin(event){
                event.preventDefault();
                this.toggle();
                history.replace("/login");
        }

        onCreate(event){
                event.preventDefault();
                this.toggle();
                history.replace("/createuser");
        }

        onUsersAdmin(event){
                event.preventDefault();
                this.toggle();
                history.replace("/usersadmin");
        }

        onEventsAdmin(event){
                event.preventDefault();
                this.toggle();
                history.replace("/eventsadmin");
        }

        onCreateEvent(event){
                event.preventDefault();
                this.toggle();
                history.replace("/createevent");
        }

        onLogout(event){
                var userinfo = JSON.parse(sessionStorage.userinfo);
                jquery.ajax({
                type: 'POST',
                url: "/mididec/api/v1.0/users/" + userinfo.user_id + '/logout',
                data: JSON.stringify (userinfo),
                success: this.logoutSuccess,
                error: this.logoutError,
                contentType: "application/json",
                dataType: 'json'
                });
        }

        logoutSuccess(data){
            sessionStorage.removeItem('userinfo');
            this.toggle();
            history.replace("/");
            this.setState(this.state);
        }

        logoutError(data){
                sessionStorage.removeItem('userinfo');
                this.toggle();
                history.replace("/");
                this.setState(this.state);
        }

        toggle() {
          this.setState({
            isOpen: !this.state.isOpen
          });
        }

        onLeave(e){
                this.setState({
                  isOpen: false
                });
        }
        render(){
                var subscribelink = "";
                var loginlink = "";
                var userlink = "";

                var user = User.getSession();
                var useradmin = "";
                if (user && user.isSuperUser)
                    useradmin = (<DropdownItem onClick={this.onUsersAdmin}>Gestion des usagers</DropdownItem> );
                var eventadmin = "";
                if (user && (user.isSuperUser || user.isManager))
                        eventadmin = (<DropdownItem onClick={this.onEventsAdmin}>Gestion des rencontres</DropdownItem> );
                var createevent = "";
                if (user && (user.isManager || user.isSuperUser))
                    createevent = (<DropdownItem onClick={this.onCreateEvent}>Ajouter une rencontres</DropdownItem> );
                if (user){
                        userlink = (    <UncontrolledDropdown nav inNavbar>
                                                <DropdownToggle nav caret>
                                                        <i className="material-icons md-light">account_circle</i>
                                                </DropdownToggle>
                                                <DropdownMenu right>
                                                        <DropdownItem header>
                                                                {user.alias}
                                                        </DropdownItem>
                                                        <DropdownItem onClick={this.onProfile}>
                                                                Profile
                                                        </DropdownItem>
                                                        {createevent}
                                                        {eventadmin}
                                                        {useradmin}
                                                        <DropdownItem divider />
                                                        <DropdownItem onClick={this.onLogout}>
                                                                Logout
                                                        </DropdownItem>
                                                </DropdownMenu>
                                        </UncontrolledDropdown>)
                }
                else {
                        subscribelink = (<NavItem>
                                <NavLink className='subscribe-link' onClick={this.onCreate}>
                                        S'inscrire
                                </NavLink>
                        </NavItem>);
                        loginlink =(<NavItem>
                                <NavLink className='home-link' onClick={this.onLogin}>
                                        Login
                                </NavLink>
                        </NavItem>);
                }
                return (
                        <div className='navbars'>
                        <NB className='navs'  dark expand="md" fixed={'top'} onMouseLeave={this.onLeave}>
                          <NavbarBrand ><img className='logo' src='res/drawables/mididec.png' onClick={this.onHome}/></NavbarBrand>
                          <NavbarToggler onClick={this.toggle} />
                          <Collapse isOpen={this.state.isOpen}  navbar>
                            <Nav className="ml-auto" navbar>
                              <NavItem>
                                      <NavLink className='home-link' onClick={this.onHome}>Home</NavLink>
                              </NavItem>
                              {subscribelink}
                              {loginlink}
                              {userlink}
                            </Nav>
                          </Collapse>
                        </NB>



                        </div>)
        }
}

module.exports = Navbar;
