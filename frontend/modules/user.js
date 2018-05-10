
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

        get access(){
                return this._userinfo.access;
        }

        get email(){
                return this._userinfo.email;
        }

        get name(){
                return this._userinfo.name;
        }

        get alias(){
                return this._userinfo.alias;
        }

        get loginkey(){
                return this._userinfo.loginkey;
        }

        get user_id(){
                return this._userinfo.user_id;
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
