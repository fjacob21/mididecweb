import Text from './localization/text'

class Errors {
        static getErrorMessage(error){
                return Text.text[Errors._messages[error]];
        }
}

Errors.ERROR_INVALID_EVENT = 1;
Errors.ERROR_INVALID_REQUEST = 2;
Errors.ERROR_MISSING_PARAMS = 3;
Errors.ERROR_ACCESS_DENIED = 4;
Errors.ERROR_INVALID_LOGIN = 5;
Errors.ERROR_LOGIN_NEEDED = 6;
Errors.ERROR_NOT_REGISTERED = 7;
Errors.ERROR_SENDING_EMAIL = 8;
Errors.ERROR_INVALID_USER = 9;
Errors.ERROR_VALIDATION_REQUIRED = 10;
Errors.ERROR_NO_AVATAR = 11;
Errors.ERROR_INVALID_SMS_CODE = 12;
Errors.ERROR_ATTACHMENT_PRESENT = 13;
Errors.ERROR_INVALID_ATTACHMENT = 14;
Errors.ERROR_ATTENDEE_TOO_LOW = 15;

Errors._messages = [];
Errors._messages[Errors.ERROR_INVALID_EVENT] = "err_invalid_event_msg";
Errors._messages[Errors.ERROR_INVALID_REQUEST] = "err_invalid_request_msg";
Errors._messages[Errors.ERROR_MISSING_PARAMS] = "err_missing_params_msg";
Errors._messages[Errors.ERROR_ACCESS_DENIED] = "err_access_denied_msg";
Errors._messages[Errors.ERROR_INVALID_LOGIN] = "err_invalid_login_msg";
Errors._messages[Errors.ERROR_LOGIN_NEEDED] = "err_login_needed_msg";
Errors._messages[Errors.ERROR_NOT_REGISTERED] = "err_not_registered_msg";
Errors._messages[Errors.ERROR_SENDING_EMAIL] = "err_sending_email_msg";
Errors._messages[Errors.ERROR_INVALID_USER] = "err_invalid_user_msg";
Errors._messages[Errors.ERROR_VALIDATION_REQUIRED] = "err_validation_required_msg";
Errors._messages[Errors.ERROR_NO_AVATAR] = "err_no_avatar_msg";
Errors._messages[Errors.ERROR_INVALID_SMS_CODE] = "err_invalid_sms_code_msg";
Errors._messages[Errors.ERROR_ATTACHMENT_PRESENT] = "err_attachment_present_msg";
Errors._messages[Errors.ERROR_INVALID_ATTACHMENT] = "err_invalid_attachment_msg";
Errors._messages[Errors.ERROR_ATTENDEE_TOO_LOW] = "err_attendee_too_low_msg";
module.exports = Errors;
