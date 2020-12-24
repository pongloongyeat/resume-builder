# Résumé Builder

A simple Django-based résumé builder app.

## Requirements

- Python3
- pip

Create a virtualenv and then use `pip install -r requirements.txt` to install dependencies.

## Running

To start the server, first apply migrations using `python manage.py migrate` then run with `python manage.py startserver`.

## Known issues

Due to my lack of knowledge in CSS and my eagerness in trying to keep everything in Python to allow for better maintainability, this app cannot:

- Render extra forms dynamically ([#11](https://github.com/pongloongyeat/resume-builder/issues/11)). Since this app is completely static, you'll have to refresh the app to see the extra form pop up.
- Remove forms ([#12](https://github.com/pongloongyeat/resume-builder/issues/12)). Again, this would require a bit of JavaScript, which I haven't really gotten into. Even if this were to be implemented right now, you would need to refresh the page to see the form disappear.
- Remove résumés ([#21](https://github.com/pongloongyeat/resume-builder/issues/21)). Same as above.
- Show a present label on month times ([#13](https://github.com/pongloongyeat/resume-builder/issues/13)). I suck at CSS and I have no clue how to add that option.
- Render the PDF nicely ([#24](https://github.com/pongloongyeat/resume-builder/issues/24)). Again, I suck at CSS.
- Render the PDF if there are certain special characters ([#26](https://github.com/pongloongyeat/resume-builder/issues/26)).