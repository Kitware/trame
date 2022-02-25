# Install requirements (if it exists)
if [ -f /deploy/setup/requirements.txt ]
then
  conda install -y --file /deploy/setup/requirements.txt
fi
