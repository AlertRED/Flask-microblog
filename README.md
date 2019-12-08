# **Flask-microblog**
### Change configuration (on example "DEBUG")
---
#### Venv console
**Windows:** set FLASK_DEBUG=1
**Linux:** $export FLASK_DEBUG=1
#### In code
DEBUG = True
or
app.config['DEBUG'] = True
or
app.debug = True

### Types configuration
---
##### Debug mode
 Whether debug mode is enabled. When using flask run to start the development server, an interactive debugger will be shown for unhandled exceptions, and the server will be reloaded when code changes. The debug attribute maps to this config key.
**Console:** FLASK_DEBUG=1


##### Testing
Enable testing mode. Exceptions are propagated rather than handled by the the app’s error handlers. Extensions may also change their behavior to facilitate easier testing. You should enable this in your own tests.

**Console:** FLASK_TESTING=1

##### Debug & Reloader mode
Setting FLASK_ENV to development will enable debug mode. flask run will use the interactive debugger and reloader by default in debug mode.

**Console:** FLASK_ENV=development

