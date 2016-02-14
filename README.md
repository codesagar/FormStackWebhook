Python Webhook for FormStack to SendGrid
=========================

This Python web application is meant to serve as a base for you to build Webhook Handlers.

The application integrates the following:

  + Shared Secret Validation
  + Request parsing

To add your own logic, all you have to do is extend the `webhook_post_handler` function in `app.py`.


Usage
=====

To deploy the app, you can:

   + Add it to an instance you own, install its dependencies
   + Use a PaaS, either deployed on your own infrastructure (CloudFoundry), or on public infrastructure (e.g. Heroku)


Installing Dependencies
-----------------------

To install the app's dependencies, do the following:

  + Ensure that you have the [Python Pip installer][0] available on your system
  + Run `pip install -r requirements.txt`, from the root of the project



Running the app
---------------

The app will listen on port `5000` by default.
