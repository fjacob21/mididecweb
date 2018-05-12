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
                this.onCreateEvent = this.onCreateEvent.bind(this);
                this.onLogin = this.onLogin.bind(this);
                this.onLogout = this.onLogout.bind(this);
                this.logoutSuccess = this.logoutSuccess.bind(this);
                this.logoutError = this.logoutError.bind(this);
                this.onProfile = this.onProfile.bind(this);
                this.toggle = this.toggle.bind(this);
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
                history.replace("/");
        }

        onProfile(event){
                var user = User.getSession();
                event.preventDefault();
                history.replace("/users/" + user.user_id + '/update');
        }

        onLogin(event){
                event.preventDefault();
                history.replace("/login");
        }

        onCreate(event){
                event.preventDefault();
                history.replace("/createuser");
        }

        onCreateEvent(event){
                event.preventDefault();
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
            history.replace("/");
            this.setState(this.state);
        }

        logoutError(data){
                sessionStorage.removeItem('userinfo');
                history.replace("/");
                this.setState(this.state);
        }

        toggle() {
          this.setState({
            isOpen: !this.state.isOpen
          });
        }

        render(){
                var userlink = (<div className='notlognav'>
                                        <NavItem>
                                                <NavLink className='mailinglist-link' onClick={this.onCreate}>
                                                        Sinscrire
                                                </NavLink>
                                        </NavItem>
                                        <NavItem>
                                                <NavLink className='home-link' onClick={this.onLogin}>
                                                        Login
                                                </NavLink>
                                        </NavItem>
                                </div>);

                var user = User.getSession();
                var createevent = "";
                if (user && (user.isManager || user.isSuperUser))
                    createevent = (<DropdownItem onClick={this.onCreateEvent}>Ajouter un evenement</DropdownItem> );
                if (user){
                        userlink = (    <UncontrolledDropdown nav inNavbar>
                                                <DropdownToggle nav caret>
                                                        <i class="material-icons md-light">account_circle</i>
                                                </DropdownToggle>
                                                <DropdownMenu right>
                                                        <DropdownItem header>
                                                                {user.alias}
                                                        </DropdownItem>
                                                        <DropdownItem onClick={this.onProfile}>
                                                                Profile
                                                        </DropdownItem>
                                                        {createevent}
                                                        <DropdownItem divider />
                                                        <DropdownItem onClick={this.onLogout}>
                                                                Logout
                                                        </DropdownItem>
                                                </DropdownMenu>
                                        </UncontrolledDropdown>)
                }
                return (
                        <div className='navbars'>
                        <NB className='navs'  dark expand="md" fixed={'top'}>
                          <NavbarBrand ><img className='logo' src='res/drawables/mididec.png' onClick={this.onHome}/></NavbarBrand>
                          <NavbarToggler onClick={this.toggle} />
                          <Collapse isOpen={this.state.isOpen} navbar>
                            <Nav className="ml-auto" navbar>
                              <NavItem>
                                      <NavLink className='home-link' onClick={this.onHome}>Home</NavLink>
                              </NavItem>
                              {userlink}
                            </Nav>
                          </Collapse>
                        </NB>



                        </div>)
        }
}

module.exports = Navbar;
