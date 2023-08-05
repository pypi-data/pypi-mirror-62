Pyexpander administration scripts
=================================

How to create a new release
---------------------------

Create a new version
++++++++++++++++++++

Show the current version with this command::

  ./show-version.sh

Make up a new version VERSION and create it with::

  ./new-version.sh <VERSION>

Rebuild documentation
+++++++++++++++++++++

Enter this command::

  ./doc-rebuild.sh

Create tar.gz distribution files
++++++++++++++++++++++++++++++++

Enter these commands::

  ./cleanup-distdirs.sh
  ./mk-dist.sh

Create docker images
++++++++++++++++++++

Check if the docker images for pyexpander exist, note that you may use "podman"
instead of "docker"::


  docker images | grep pyexpander

If you see nothing, create the images with::

  ./docker-build-all.sh

Now create all pyexpander packages with::

  ./docker-run-all.sh

Upload files to sourceforge
+++++++++++++++++++++++++++

Upload the documentation with::

  ./sourceforge-upload-html.sh

Upload the distribution files with::

  ./sourceforge-upload-distfiles.sh

Prepare the local repository
++++++++++++++++++++++++++++

Use these commands to change mq patches to regular mercurial patches::

  hg qcommit -m backup
  hg qfinish -a

Give a tag::

  hg tag <VERSION>

upload the repository to sourceforge
++++++++++++++++++++++++++++++++++++

Push all patches to the central sourceforge repository::

  hg push

upload the repository to bitbucket
++++++++++++++++++++++++++++++++++

Enter this command::

  ./bitbucket-push.sh

Upload to pypi
++++++++++++++

Note: ~/pypirc must have this content (password omitted here)::

  [distutils]
  index-servers=
      pypi
      testpypi
  
  [testpypi]
  repository = https://test.pypi.org/legacy/
  username = Goetz.Pfeiffer
  password = ***
  
  [pypi]
  username = Goetz.Pfeiffer
  password = ***

Since you cannot undo an upload of a specific version, first test with the
pypi test site.

pypi test site
::::::::::::::

Run::

  ./pypi-test-upload.sh

Now test with these commands::

  bash
  mkdir tmp
  cd tmp
  pip install pyexpander -i https://testpypi.python.org/pypi --prefix `pwd`
  export PYTHONUSERBASE=`pwd`
  PATH=`pwd`/bin:$PATH
  expander.py -h
  exit

If everything worked, remove the test directory with::

  rm -rf tmp

pypi site
:::::::::

Upload to pypi with::

  ./pypi-upload.sh

Explanation of scripts
----------------------

Sourceforge administration
++++++++++++++++++++++++++

sourceforge-shell.sh
  Open an interactive shell at sourceforge.

sourceforge-upload-distfiles.sh
  Upload files from "dist" directory to sourceforge.

sourceforge-upload-html.sh
  Upload html documentation to sourceforge.

Bitbucket administration
++++++++++++++++++++++++

bitbucket-push.sh
  Push patches to mercurial repository at Bitbucket.

Version handling
++++++++++++++++

check-version.sh
  Check if version numbers are consistent.

show-version.sh
  Show version numbers in all scripts and modules.

new-version.sh
  Create a new version (see "Steps to create a new release" in this file).

Documentation
+++++++++++++

doc-rebuild.sh
  Rebuild the html documentation

Create distribution files
+++++++++++++++++++++++++

mk-dist.sh
  Create distribution (*.tar.gz) files

cleanup-distdirs.sh
  Clean the distribution directory

mk-rpm.sh
  Create an rpm file (works only on a fedora system)

mk-deb.sh
  Create a debian file, should be used on a debian system or a debian docker
  container.

pypi support
++++++++++++

pypi-upload.sh
  Upload a new version to pypi.

pypi-test-upload.sh
  Upload a new version to the pypi test server.

Docker support
++++++++++++++

docker          
  The directory with the docker files

docker-build.sh
  Build docker debian containers needed for mk-xxx.sh scripts run this as
  docker-build.sh <system-name> with system-name one of: debian-7 debian-8
  fedora-21 fedora-22

docker-build-all.sh 
  Build docker containers for all supported linux systems.

docker-run.sh
  Run a docker container run this as docker-run.sh <system-name> with
  system-name one of: debian-7 debian-8 fedora-21 fedora-22

docker-run-all.sh
  Build pyexpander packages for all supported linux systems.

mk-deb.sh
  Create debian packages, called from within the debian docker container.

mk-rpm.sh
  Create rpm packages, called from within the fedora docker container.

