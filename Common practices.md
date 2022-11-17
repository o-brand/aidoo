# Common practices

You must follow these rules to keep our code clean.

If you think we should add anything else, or change something, feel free to do it, but notify everybody about the changes.

## Code quality

- Naming variables, functions, classes, objects: Python - snake_case; JS - camelCase; HTML - dash-case. The names should be meaningful and complete.

- Indentations: Python - 4 spaces; JS, HTMl - 2 spaces.

- Limit all lines to a maximum of 79 characters everywhere.

- Use 2 empty lines between external classes' and functions' declaration.

- You should delete unused code and imports.

- Every file should end with an empty line.

### Comments

- Every class, function should have a meaningful comment what is it for - Use [docstrings](https://peps.python.org/pep-0008/#documentation-strings) in Python and ```/** This is a description of the foo function. */``` in JS.

- An explanation is necessary for ombigous variable names.

- You can comment on loops, if statements if it is not obvious what it does.

- Use "TODO" to state that a code is not working or complete.

## Developing stuff

- If any test fails after your commit, please try to solve the problem or ask for help from the last person who edited that file. She/He might be able to help.

- Please use small comments if you add Python code to the project, and respect the comments of others (i.e., do not delete them).

- If you are not sure what a function/file does, ask the last person who edited that file.

- Before you commit, check if you made ACTUAL changes to the DB file. (It has a column for when the user last logged in, so the DB will have at least one difference, if you logged in.) If you didn't update the DB, then discard the changes before you commit. This way, it would be easier to merge branches later.

- If you are writing a test for an url not in the login app, then use ```LoginRequiredTestCase``` instead of the default ```TestCase```. (You can import like this: ```from Golf.utils import LoginRequiredTestCase```.)

- JS is just used to communicate with Django. So no sensitive information should be communicated via the JS functions and you should check the values on the backend.
