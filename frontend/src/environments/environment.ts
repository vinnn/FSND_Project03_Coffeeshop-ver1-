/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'coffeetenant2.eu', // the auth0 domain prefix
    audience: 'coffeeidentifier2', // the audience set for the auth0 app
    clientId: 'fdTL55MXOe9iOH2MQ9UU25j7nQ9DG7OW', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application. I: Note: the font-end adds '/tabs/user-page' to this URL
  }
};
