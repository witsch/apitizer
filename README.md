Plone APItizer
==============

This is an experiment to refactor existing Plone packages to use
[plone.api](https://docs.plone.org/develop/plone.api/docs/) using
[rope](https://github.com/python-rope/rope).

After setting things up you can run the `apitizer` script from your
source checkout:

  ```
  $ git clone git@github.com:witsch/apitizer.git
  $ cd apitizer
  $ make
  $ cd <your-project>
  $ <path-to-apitizer>/bin/apitizer
  ```
