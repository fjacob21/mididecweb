
class User {

        static getSession(){
                if (!sessionStorage.userinfo)
                        return null
                var userinfo = JSON.parse(sessionStorage.userinfo);
                return new User(userinfo);
        }

        constructor(userinfo){
                this._userinfo = userinfo
        }

        get infotype(){
                return this._userinfo.infotype;
        }

        get user_id(){
                return this._userinfo.user_id;
        }

        get name(){
                return this._userinfo.name;
        }

        get alias(){
                return this._userinfo.alias;
        }

        get password(){
                return this._userinfo.password;
        }

        get phone(){
                return this._userinfo.phone;
        }

        get useemail(){
                return this._userinfo.useemail;
        }

        get usesms(){
                return this._userinfo.usesms;
        }

        get profile(){
                return this._userinfo.profile;
        }

        get validated(){
                return this._userinfo.validated;
        }

        get smsvalidated(){
                return this._userinfo.smsvalidated;
        }

        get lastlogin(){
                return this._userinfo.lastlogin;
        }

        get email(){
                return this._userinfo.email;
        }

        get present(){
                return this._userinfo.present;
        }

        get presentTime(){
                return this._userinfo.present_time;
        }

        get have_avatar(){
                return this._userinfo.have_avatar;
        }

        get loginkey(){
                return this._userinfo.loginkey;
        }

        get access(){
                return this._userinfo.access;
        }

        get isNormalUser(){
                return this.access == User.ACCESS_NORMAL;
        }

        get isManager(){
                return this.access == User.ACCESS_MANAGER;
        }

        get isSuperUser(){
                return this.access == User.ACCESS_SUPER;
        }
}

User.ACCESS_NORMAL = 0;
User.ACCESS_MANAGER = 0x3;
User.ACCESS_SUPER = 0xFF;
module.exports = User;
