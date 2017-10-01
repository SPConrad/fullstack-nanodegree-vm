Udacity Full Stack Web Developer Nanodegree - The Backend: Databases & Applications - Catalog Project


Necessary components (doesn't HAVE to be in this order, is probably better in this order):

python https://www.python.org/download/releases/2.7/

VirtualBox https://www.virtualbox.org/wiki/Downloads

Vagrant https://www.vagrantup.com/downloads.html


Download VM config here: https://d17h27t6h515a5.cloudfront.net/topher/2017/August/59822701_fsnd-virtual-machine/fsnd-virtual-machine.zip

Unzip that file

Clone this repository into the unzipped directory

Open a terminal

Navigate to the vagrant file in the unzipped directory

Run 'vagrant up' in that directory

After that is finished, run 'vagrant ssh' to connect to the virtual machine

You'll now want to navigate to the /catalog directory where the models.py, lotsofgames.py, and views.py files live

Create the database - 

python models.py

Populate the database - 

python lotsofgames.py

Navigate to localhost:5000 to use the app






More detailed instructions and troubleshooting avaialble here https://classroom.udacity.com/nanodegrees/nd004/parts/8d3e23e1-9ab6-47eb-b4f3-d5dc7ef27bf0/modules/bc51d967-cb21-46f4-90ea-caf73439dc59/lessons/5475ecd6-cfdb-4418-85a2-f2583074c08d/concepts/14c72fe3-e3fe-4959-9c4b-467cf5b7c3a0