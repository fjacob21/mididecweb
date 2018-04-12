
class DateFormater {
  constructor(date) {
    if (typeof date == 'string')
      this._date = new Date(date)
    else if (date.constructor.name == "Date")
      this._date = date
  }

  getDate(){
    return this._date
  }

  getDateText(){
    var dateOptions = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', timeZone: 'UTC'};
    return this._date.toLocaleDateString('fr-CA', dateOptions);
  }

  getShortDateText(){
    var dateOptions = { weekday: undefined, year: 'numeric', month: 'numeric', day: 'numeric', timeZone: 'UTC'};
    return this._date.toLocaleDateString('fr-CA', dateOptions);
  }

  getTimeText(){
    var timeOptions = { hour: 'numeric', minute: 'numeric', second: undefined, timeZone: 'UTC'};
    return this._date.toLocaleTimeString('fr-CA', timeOptions).replace(/ /g, '');
  }
}

module.exports = DateFormater;
