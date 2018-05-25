import jquery from 'jquery'

class FormQuery {

        static isIos(){
                var iOS = !!navigator.platform && /iPad|iPhone|iPod/.test(navigator.platform);
                return iOS;
        }

        constructor(obj){
            this._obj = obj
        }

        parse(){
                for (var prop in this._obj)
                        this._obj[prop] = jquery('#'+prop)[0].value;
                return this._obj;
        }


}

module.exports = FormQuery;
