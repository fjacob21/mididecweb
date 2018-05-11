import User from './user'

class Event {

        constructor(event){
                this._event = event
        }

        get event_id(){
                return this._event.event_id;
        }

        get title(){
                return this._event.title;
        }

        get description(){
                return this._event.description;
        }

        get max_attendee(){
                return this._event.max_attendee;
        }

        get start(){
                return this._event.start;
        }

        get duration(){
                return this._event.duration;
        }

        get location(){
                return this._event.location;
        }

        get organizer_name(){
                return this._event.organizer_name;
        }

        get organizer_email(){
                return this._event.organizer_email;
        }

        get owner(){
                return new User(this._event.owner_id);
        }

        get attendees(){
                return this._event.attendees;
        }

        get waiting_attendees(){
                return this._event.waiting_attendees;
        }

        get find_attendee(){
                return this._event.waiting_attendees;
        }

        get find_waiting(){
                return this._event.waiting_attendees;
        }
}

Event.ACCESS_NORMAL = 0;
Event.ACCESS_MANAGER = 0x3;
Event.ACCESS_SUPER = 0xFF;
module.exports = Event;
