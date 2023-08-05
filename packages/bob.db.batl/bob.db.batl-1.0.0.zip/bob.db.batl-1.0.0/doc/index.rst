.. vim: set fileencoding=utf-8 :
.. Andre Anjos <andre.anjos@idiap.ch>
.. Mon 13 Aug 2012 12:36:40 CEST

.. _bob.db.batl:

=========================
 BATL Database Interface
=========================

File Naming Conventions
-----------------------

The operator is asked to enter some information about the capture to the GUI. After the data capture, most
of this information is encoded in the name of the file. All this information were also saved as an attribute in
the HDF5 file.

Each saved file has the following name format:

<client_id>_<session_id>_<presenter_id>_<type_id>_<pai_id>.hdf5

* client_id: This number presents the identity of what is presented to the system. For bonafide, it is the ID given to the subject upon arrival and for the attacks, it is a number given to a PAI in this protocol. Please note that if the identity of a subject is the same as the identity of an attack this number is the same for both cases. One example is the silicon masks. If a silicon mask is made from subject ‘x’ and subject ‘x’ also participated as bonafide in the data collection the ‘client_id’ for bonafide and silicon mask is the same.

* session_id: The number of session mentioned before.

* presenter_id: If a subject is presenting an attack to the system, this number is the subject’s ‘client_id’. If the attack is presented on a support, this number is ‘000’. If the capture is for bonafide this number is ‘000’ as well since there is no presenter in this case.

* type_id: The type of attack based on groups mentioned before. For bonafide this number is ‘0’

* pai_id: The unique number asscociated with each and every PAI. This number for bonafide with no medical glasses is ‘00’ and for bonafide with medical glasses is ‘01’. In our data capture we included retro glasses as bonafide as well and the ‘pai_id’ for it is ‘02’.


Here are some examples for more clarification:

* 035_01_000_0_00.hdf5 : This is the bonafide file of client number 035 in session number 1 when they did not wear medical glasses.

* 005_01_000_0_01.hdf5 : This is the bonafide file of client number 005 in session number 1 when they did wear medical glasses.

* 530_03_001_2_18.hdf5 : This is a fake face attack where the identity 530 is presented to the camera by client number 001 in session 03.

* 018_02_000_3_10.hdf5 : This is a photo attack where the identity 018 is presented to the camera using stand in session 02.

Package Documentation
---------------------

.. automodule:: bob.db.batl

