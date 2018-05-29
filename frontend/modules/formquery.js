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
                for (var prop in this._obj) {
                        var obj = jquery('#'+prop)[0];
                        if (obj) {
                            if (obj.type == 'checkbox')
                                this._obj[prop] = obj.checked
                            else
                                this._obj[prop] = obj.value;
                        }
                }
                return this._obj;
        }
}

module.exports = FormQuery;
