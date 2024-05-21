echo 'Starting Script'
if python src/main.py; then
    flask --app src/server.py run --debug
else
    echo "Exit code of $?, failure"
fi

