<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#testing">Testing</a></li>
      </ul>
    </li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>


## About The Project

I've seen a lot of twitter/facebook/etc. clones on various learning websites.  Most of which seem pretty "complete" from a beginner standpoint, where they establish some kind of route-structure and slap on a rudimentary front-end to it, but are actually missing many implementation details.  In the middle of thinking about the aforementioned missing implementation details, I pondered how many details were actually missing and how difficult it would be to create a properly-accurate front-end (not just div-boxes with minimal styling/colors), and thus this project was born.

The project serves to:
* Provide practice for me/others who wish to contribute.
* Provide insight as to difficulties when transitioning technologies (EG: using templates at first, and then switching to React).
* Provide a relatively small/midsized code base for other people to look at/modify/question/contribute.
* Provide an easy way for people who are scared of breaking things to start contributing (to something that noone depends upon).

Every major version ("build") will be released so people can look at past revisions of/decisions about the code base.  Ofcourse, this is a relatively small/private project, so I don't expect it to garner that much attention, but it should be pretty fun. 


### Built With

* Backend:
  * Core:
    * [Python3](https://www.python.org/)
    * [Flask](https://palletsprojects.com/p/flask/)
  * Database:
    * [SQLAlchemy](https://www.sqlalchemy.org/)
    * [SQLite3](https://www.sqlite.org/index.html)
* Frontend:
  * [Jinja2](https://jinja.palletsprojects.com/en/2.11.x/)
  * [WTForms](https://wtforms.readthedocs.io/en/2.3.x/)
  * HTML5
  * CSS
  * Special note: There is NO JS in this build.
* DevOps/Testing
  * [Pytest](https://docs.pytest.org/en/stable/)
  * [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
  * [Coverage](https://coverage.readthedocs.io/en/coverage-5.3/)

### Past builds

* None yet.


## Getting Started

1. Clone the repo.
  ```
  git clone https://github.com/Nickatak/twitter-clone
  ```

2. Install the dependencies.
  ```
  pip install -r requirements.txt
  ```

3. Run the server.
  ```
  flask run
  ```

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
  * Python3

### Testing

1. Clone the repo (if you haven't already).
  ```
  git clone https://github.com/Nickatak/twitter-clone
  ```

2. Install the dependencies (if you haven't already).
  ```
  pip install -r requirements.txt
  ```

3. Run pytest (with coverage).
  ```
  coverage run -m pytest
  ```

  OPTIONAL: If you don't want to see the test-coverage, then you can just run (and stop here):
  ```
  pytest
  ```

4. Generate coverage-report.
  ```
  coverage html
  ```

5. Open up `/htmlcov/index.html` in your browser to see the coverage report.

## Contributing

Join in the fun and contribute.  This is a non-serious project, so don't be afraid to break something (although I'll try my best not to let that happen by reviewing your changes before merging, of course).

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Write new tests for your new feature.
6. Run tests (See: [testing](#Testing)) and make sure they all pass.
7. Open a Pull Request


## License

Distributed under the Apache License, version 2.0. See `LICENSE.txt` for more information.
