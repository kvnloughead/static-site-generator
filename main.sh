#!/bin/bash
#
# Run the src/main.py script and serve public/index.html. By default the 
# webpage is served on port 8888. 
#
# If port 8888 is occupied, you have the option
# to run it on another port. The new port number will be the first available 
# integer that is greater than 8888.

python3 src/main.py
echo "Running main.py" 

PORT=8888

if sudo lsof -i:$PORT >/dev/null; then
  echo "Port 8888 is in use."

  read -p "Use a different port? (y/n): " response

  case $response in
    [yY]|[yY][eE][sS])
        cd public
        NEW_PORT=$(($PORT + 1))
        while sudo lsof -i:$NEW_PORT >/dev/null; do
          NEW_PORT=$(($NEW_PORT + 1))
        done
        echo "Starting server on port $NEW_PORT"
        python3 -m http.server $NEW_PORT
      ;;
    [nN]|[nN][oO])
      echo "Exiting..."
      exit 0
      ;;
    *)
      echo "Invalid input. Please enter y/yes or n/no."
      exit 1
      ;;
  esac

else
  cd public && python3 -m http.server $PORT
fi

