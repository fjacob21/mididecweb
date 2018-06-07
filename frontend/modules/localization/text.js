import frca from './fr-CA.json'
import enca from './en-CA.json'

class Text {
        static get text(){
                if (!localStorage.locale){
                        if (!Text.obj)
                                Text.obj = new Text('fr-CA');
                        return Text.obj;
                }

                if (!Text.obj || Text.obj.locale != localStorage.locale)
                        Text.obj = new Text(localStorage.locale);
                return Text.obj;
        }

        static getLocales(){
                var locales = [];
                for (var locale in Text.locales)
                        locales.push({id: locale, name: Text.locales[locale].lang});
                return locales;
        }

        constructor(locale){
                this.locale = locale;
                for (var l in Text.locales[locale])
                        this[l] = Text.locales[locale][l]
        }
}

Text.locales = []
Text.locales['fr-CA'] = frca
Text.locales['en-CA'] = enca
Text.obj = null;
module.exports = Text;
