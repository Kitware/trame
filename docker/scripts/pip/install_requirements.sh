# Install requirements (if it exists)
if [ -f /deploy/setup/requirements.txt ]
then
  pip install -r /deploy/setup/requirements.txt
fi
