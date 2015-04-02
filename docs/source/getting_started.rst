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

.. note:: The download script uses the Python standard library and it can be used outside of the Vagrant virtual machine. If you're only interested in downloading the data clone the repository only.

The following command will download all the shape files containing the CTR. Use -h for more options.

.. code-block:: bash

    python download_sit_puglia.py --download ctr_vet


.. _VirtualBox: https://www.virtualbox.org/wiki/Downloads
.. _Vagrant: http://docs.vagrantup.com/v2/installation/
.. _Ansible: http://docs.ansible.com/intro_installation.html