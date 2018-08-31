import React , { Component, PropTypes } from 'react'
import { browserHistory} from 'react-router'
import jquery from 'jquery'
import User from './user'
import createHistory from "history/createHashHistory"
import Text from './localization/text'
import {
  Input,
  Collapse,
  Navbar as NB,
  NavbarToggler,
  NavbarBrand,
  Nav,
  NavItem,
  NavLink,
  UncontrolledDropdown,
  Dropdown,
  DropdownToggle,
  DropdownMenu,
  DropdownItem } from 'reactstrap';

const history = createHistory();
class Navbar extends React.Component{
        constructor(props) {
                super(props);
                var locale = 'fr-CA';
                if (localStorage.locale)
                        locale = localStorage.locale;
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
                this.onChange = this.onChange.bind(this);
                this.state = {
                  locale: locale,
                  isOpen: false
                };
        }

        componentDidMount(){
        }

        componentWillUnmount(){
        }

        onChange(e) {
                console.debug(e.target.value);
                localStorage.setItem('locale', e.target.value);
                this.state.locale = e.target.value;
                this.setState(this.state);
                this.props.refresh();
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
                    useradmin = (<NavItem><NavLink className='home-link' onClick={this.onUsersAdmin}>{Text.text.nav_useradmin_label}</NavLink></NavItem>);
                var eventadmin = "";
                if (user && (user.isSuperUser || user.isManager))
                        eventadmin = (<NavItem><NavLink className='home-link' onClick={this.onEventsAdmin}>{Text.text.nav_eventadmin_label}</NavLink></NavItem> );
                var createevent = "";
                if (user && (user.isManager || user.isSuperUser))
                    createevent = (<NavItem><NavLink className='home-link' onClick={this.onCreateEvent}>{Text.text.nav_create_event_label}</NavLink></NavItem> );
                if (user){
                        var avatar = <i className="material-icons md-light">account_circle</i>
                        if (user.have_avatar) {
                                var avatar_path = "/mididec/api/v1.0/users/" + user.user_id+"/avatar?" + new Date().getTime();
                                avatar = <img src={avatar_path} className="nav-avatar"/>
                        }
                        userlink = (    <UncontrolledDropdown nav inNavbar>
                                                <DropdownToggle nav caret>
                                                        {avatar}
                                                </DropdownToggle>
                                                <DropdownMenu right>
                                                        <DropdownItem header>
                                                                {user.alias}
                                                        </DropdownItem>
                                                        <DropdownItem onClick={this.onProfile}>
                                                                {Text.text.profile}
                                                        </DropdownItem>
                                                        <DropdownItem divider />
                                                        <DropdownItem onClick={this.onLogout}>
                                                                {Text.text.logout}
                                                        </DropdownItem>
                                                </DropdownMenu>
                                        </UncontrolledDropdown>)
                }
                else {
                        subscribelink = (<NavItem>
                                <NavLink className='subscribe-link' onClick={this.onCreate}>
                                        {Text.text.nav_user_add_label}
                                </NavLink>
                        </NavItem>);
                        loginlink =(<NavItem>
                                <NavLink className='home-link' onClick={this.onLogin}>
                                        {Text.text.login}
                                </NavLink>
                        </NavItem>);
                }
                var langs = Text.getLocales().map((locale) =>
                        <option key={locale.id} value={locale.id}>{locale.name}</option>
                  );
                return (
                        <div className='navbars'>
                        <NB className='navs'  dark expand="md" fixed={'top'} onMouseLeave={this.onLeave}>
                          <NavbarBrand ><img className='logo' src='res/drawables/mididec.png' onClick={this.onHome}/></NavbarBrand>
                          <NavbarToggler onClick={this.toggle} />
                          <Collapse isOpen={this.state.isOpen}  navbar>
                          <Nav className="" navbar>
                                  <NavItem>
                                  <NavLink className='home-link' onClick={this.onHome}>{Text.text.nav_home_label}</NavLink>
                                  </NavItem>
                                  {createevent}
                                  {eventadmin}
                                  {useradmin}
                          </Nav>
                            <Nav className="ml-auto" navbar>
                              <NavItem>
                                    <Input type="select" name="locale" id="locale" onChange={this.onChange} value={this.state.locale}>
                                        {langs}
                                    </Input>
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
