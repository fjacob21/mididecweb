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
                this.onLogin = this.onLogin.bind(this);
                this.onLogout = this.onLogout.bind(this);
                this.logoutSuccess = this.logoutSuccess.bind(this);
                this.logoutError = this.logoutError.bind(this);
                this.onMailingList = this.onMailingList.bind(this);
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

        onLogin(event){
                event.preventDefault();
                history.replace("/login");
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

        onMailingList(event){
                event.preventDefault();
                history.replace("/mailinglist");
        }

        toggle() {
          this.setState({
            isOpen: !this.state.isOpen
          });
        }

        render(){
                var userlink = (<NavItem>
                                        <NavLink className='home-link' onClick={this.onLogin}>
                                                <i class="material-icons md-light">account_circle</i>
                                        </NavLink>
                                </NavItem>);

                var user = User.getSession();
                if (user){
                        console.debug('normal', user.isNormalUser);
                        console.debug('manager', user.isManager);
                        console.debug('super', user.isSuperUser);
                        userlink = (    <UncontrolledDropdown nav inNavbar>
                                                <DropdownToggle nav caret>
                                                        <i class="material-icons md-light">account_circle</i>
                                                </DropdownToggle>
                                                <DropdownMenu right>
                                                        <DropdownItem header>
                                                                {user.alias}
                                                        </DropdownItem>
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
                              <NavItem>
                                      <NavLink className='mailinglist-link' onClick={this.onMailingList}>Mailing List</NavLink>
                              </NavItem>
                              {userlink}


                            </Nav>
                          </Collapse>
                        </NB>



                        </div>)
        }
}

module.exports = Navbar;
