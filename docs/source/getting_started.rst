Getting started
===============

First steps
-----------

1. Install VirtualBox_
2. Install Vagrant_
3. Install Ansible_
4. Clone this repository:

.. code-block:: bash

    git clone git@github.com:sdonk/geopuglia.git

5. Configure the VM and apply provisioning

.. code-block:: bash

    cd geopuglia
    vagrant up


Download the data
-----------------

.. note:: The download script depends on requests and eventlet. The vagrant machine contains all the necessary dependencies, but if you wish to use it outside the vagrant box, please install the two external libraries on your system using the command below.

.. code-block:: bash

    pip install --user requests==2.6.0 eventlet==0.16.1

The following command will download all the shape files containing the CTR. Use -h for more options.

.. code-block:: bash

    python download_sit_puglia.py --download ctr_vet


.. _VirtualBox: https://www.virtualbox.org/wiki/Downloads
.. _Vagrant: http://docs.vagrantup.com/v2/installation/
.. _Ansible: http://docs.ansible.com/intro_installation.html