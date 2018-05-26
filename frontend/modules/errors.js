
class Errors {
        static getErrorMessage(error){
                return Errors._messages[error];
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

Errors._messages = [];
Errors._messages[Errors.ERROR_INVALID_EVENT] = "Cet Événement n'existe pas";
Errors._messages[Errors.ERROR_INVALID_REQUEST] = "Mauvais format de la requête";
Errors._messages[Errors.ERROR_MISSING_PARAMS] = "Il manque des paramettres dans la requête";
Errors._messages[Errors.ERROR_ACCESS_DENIED] = "Vous n'avez pas les accès requis pour effectuer cette opération";
Errors._messages[Errors.ERROR_INVALID_LOGIN] = "Mot de passe ou usager invalide";
Errors._messages[Errors.ERROR_LOGIN_NEEDED] = "Vous devez être connecté";
Errors._messages[Errors.ERROR_NOT_REGISTERED] = "Vous n'etes pas inscrit à cette événement";
Errors._messages[Errors.ERROR_SENDING_EMAIL] = "Erreur lors de l'envoit des courriels";
Errors._messages[Errors.ERROR_INVALID_USER] = "Cet usager n'existe pas";
Errors._messages[Errors.ERROR_VALIDATION_REQUIRED] = "Vous devez valider votre compte avant de pouvoir vous connecter";
Errors._messages[Errors.ERROR_NO_AVATAR] = "Cet usager n'a pas d'avatar";
module.exports = Errors;
