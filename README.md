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
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>


## About The Project

I've seen a lot of twitter/facebook/etc. clones on various learning websites.  Most of which seem pretty "complete" from a beginner standpoint, where they establish some kind of route-structure and slap on a rudimentary front-end to it, but are actually missing many implementation details.  In the middle of thinking about the aforementioned missing implementation details, I pondered how many details were actually missing and how difficult it would be to create a properly-accurate front-end (not just div-boxes with minimal styling/colors), and thus this project was born.

The project serves to:
* Provide practice for me/others who wish to contribute.
* Provide insight as to difficulties when transitioning technologies (EG: using templates at first, and then switching to React).
* Provide a relatively small/midsized code base for other beginners to look at/modify/question/contribute.

Every major version ("build") will be released so people can look at past revisions of/decisions about the code base.  Ofcourse, this is a relatively small/private project, so I don't expect it to garner that much attention, but it should be pretty fun. 


### Built With (current build)

* Backend:
  * [Python3](https://www.python.org/)
  * [Flask](https://palletsprojects.com/p/flask/)
  * [SQLAlchemy](https://www.sqlalchemy.org/)
* Frontend:
  * [Jinja2](https://jinja.palletsprojects.com/en/2.11.x/)
  * [WTForms](https://wtforms.readthedocs.io/en/2.3.x/)
  * HTML5
  * CSS
  * Vanilla JS


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


<!-- CONTRIBUTING -->
## Contributing

Join in the fun and contribute.  This is a non-serious project, so don't be afraid to break something (although I'll try my best not to let that happen by reviewing your changes before merging, of course).

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Your Name - [@your_twitter](https://twitter.com/your_username) - email@example.com

Project Link: [https://github.com/your_username/repo_name](https://github.com/your_username/repo_name)
