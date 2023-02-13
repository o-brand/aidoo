# Common practices

You must follow these rules to keep our code clean.

Keep things consistent!

If you think we should add anything else, or change something, feel free to do it, but notify everybody about the changes.

***If you write a new function, write tests for it!!***

## Code quality

- Naming variables, functions, classes, & objects: Python - snake_case; JS - camelCase; HTML and CSS - dash-case. The names should be meaningful and complete.

- Indentations: Python - 4 spaces; JS, HTML and CSS - 2 spaces.

- Line length: limit all lines to a maximum of 79 characters everywhere.

- Spacing: use 2 empty lines between external classes' and functions' declaration.

- Unused code: you should delete unused code and imports.

- Import order: the order of the imports should follow this list:
  + Basic Python libraries
  + Django libraries
  + Our project

- End of file: every file should end with an empty line.

### Comments

- Every class, function should have a meaningful comment what is it for - Use [docstrings](https://peps.python.org/pep-0008/#documentation-strings) in Python and ```/** This is a description of the foo function. */``` in JS.

- An explanation is necessary for ombigous variable names.

- You can comment on loops and if-else statements if it is not obvious what they do.

- Use "TODO" to state that a code is not working or complete.

## Developing stuff

- If any test fails after your commit, please try to solve the problem or ask for help from the last person who edited that file. She/He might be able to help.

- If you are not sure what a function/file does, ask the last person who edited that file.

- If you created a new branch for your task, try to limit the lifespan of the branch to a maximum of 3 days. And try to keep the irrelevant changes as few as possible to avoid merge conflicts. ***Always create a new branch from main.***

- If somebody else's task depends on you task, try to finish it before the weekend.

### Backend

- Please use small comments if you add Python code to the project, and respect the comments of others (i.e., do not delete them).

- If you've made any changes to the database via an action on the website, make sure to wipe the database and reload the data using the instructions found on the DB.md file.

- If you are writing a test for an url not in the login app, then use ```LoginRequiredTestCase``` instead of the default ```TestCase```. (You can import like this: ```from Golf.utils import LoginRequiredTestCase```.)

- Prioritize using [HTMX](https://htmx.org/) (and [Hyperscript](https://hyperscript.org/)) over JS. Validating submitted values on the backend is still necessary.

- JS is used to control some responsive behaviors on the website. Use HTMX where possible, otherwise no sensitive information should be communicated via the JS functions and you should check the values on the backend.

- Use ```f-strings``` for string formatting. [Examples](https://zetcode.com/python/fstring/)

### Frontend

- Reminder: keep things consistent!

- All styling should be placed in the styles.css file. The exception is the styling of the ```<body>``` tag, if you think this is necessary, consult other team members to see if other solutions are available, and if not, use the ```block style``` to incorporate in-document (but not in-line) styling.

- Use current guidelines for HTML5, CSS3 and JS.

- Try not to build components from scratch if alternatives exist. Check the Bootstrap *v5.3* (make sure the URL lists this version) documentation for many premade patterns you can readily integrate into the design.  
