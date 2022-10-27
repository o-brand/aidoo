# Code of Conduct

These are the "rules" we should follow while developing our project. If you think we should add anything else, or change something, feel free to do it, but notify everybody about the changes.

- If any test fails after your commit, please try to solve the problem or ask for help from the last person who edited that file. She/He might be able to help.

- Please use small comments if you add Python code to the project, and respect the comments of others (i.e., do not delete them).

- If you are not sure what a function/file does, ask the last person who edited that file.

- Before you commit, check if you made ACTUAL changes to the DB file. (It has a column for when the user last logged in, so the DB will have at least one difference, if you logged in.) If you didn't update the DB, then discard the changes before you commit. This way, it would be easier to merge branches later.

- If you are writing a test for an url not in the login app, then use ```LoginRequiredTestCase``` instead of the default ```TestCase```. (You can import like this: ```from Golf.utils import LoginRequiredTestCase```.)
