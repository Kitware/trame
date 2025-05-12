# Install requirements (if it exists)
if [ -f /deploy/setup/requirements.txt ]
then
  uv pip install -r /deploy/setup/requirements.txt
fi
