### NOTES ON SETTING UP AN AWS UBUNTU INSTANCE FOR JUPYTER NOTEBOOKS
(From: http://blog.impiyush.me/2015/02/running-ipython-notebook-server-on-aws.html)

1. Special things when creating the instance:
  - Make sure that SSH, HTTPS, and "Custom TCP Rule" (port 8888) are all opened

2. Install Anaconda
  - `> sudo apt-get install libsm6 libxrender1 libfontconfig1 git`
  - The download link can be found here: [https://www.continuum.io/downloads](https://www.continuum.io/downloads)
  - `> wget https://3230d63b5fc54e62148e-c95ac804525aac4b6dba79b00b39d1d3.ssl.cf1.rackcdn.com/Anaconda3-2.5.0-Linux-x86_64.sh`
  - `> bash Anaconda3-2.5.0-Linux-x86_64.sh`
  - `> source .bashrc` (to update path)
  - `sudo apt-get install -y python-qt4` (this is needed for matplotlib inline)

3. Update Anaconda and install useful packages
  - `> conda install seaborn joblib`
  - `> conda update --all` (this might be necessary for everything to work)

4. Generate password SHA1
  - run `> ipython`
  - `> from IPython.lib import passwd`
  - `passwd()`


5. Set up remote notebook access
  - `> mkdir certs`
  - `> cd certs`
  - `> sudo openssl req -x509 -nodes -days 365 -newkey rsa:1024 -keyout mycert.pem -out mycert.pem`
  - `> jupyter notebook --generate-config`
  - `> vim .jupyter/jupyter_notebook_config.py`
  - In the config, we need the following lines:
  c = get_config()

````
# Kernel config
c.IPKernelApp.pylab = 'inline'  # if you want plotting support always in your notebook

# Notebook config
c.NotebookApp.certfile = u'/home/ubuntu/certs/mycert.pem' #location of your certificate file
c.NotebookApp.ip = '*'
c.NotebookApp.open_browser = False  #so that the ipython notebook does not opens up a browser by default
c.NotebookApp.password = u'sha1:68c136a5b064...'  #the encrypted password we generated above
# It is a good idea to put it on a known, fixed port
c.NotebookApp.port = 8888
````

