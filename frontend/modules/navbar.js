import React , { Component, PropTypes } from 'react'
import { browserHistory} from 'react-router'
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
                            </Nav>
                          </Collapse>
                        </NB>



                        </div>)
        }
}

module.exports = Navbar;
