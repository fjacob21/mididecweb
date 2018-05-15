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

        get end(){
            return this._event.end;
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

        get owner_id(){
            return this._event.owner_id;
        }

        get attendees(){
            var attendees = [];
            for (let attendee of this._event.attendees)
                attendees.push(new User(attendee));
            return attendees;
        }

        get waitings(){
            var waitings = [];
            for (let attendee of this._event.waitings)
                waitings.push(new User(attendee));
            return waitings;
        }

        find_attendee(user){
            if (!user)
                return null;
            var attendees = this.attendees;
            for (let attendee of attendees)
                if (attendee.user_id == user.user_id)
                    return attendee;
            return null;
        }

        find_waiting(user){
            if (!user)
                return null;
            var waitings = this.waitings;
            for (let attendee of waitings)
                if (attendee.user_id == user.user_id)
                    return attendee;
            return null;
        }
}

module.exports = Event;
