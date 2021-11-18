#!/bin/bash
# echo "Enter Your Name"
# read name
# echo "Welcome $name to LinuxHint"


# echo "Total arguments : $#"
# echo "1st Argument = $1"
# echo "2nd argument = $2"

ARGUMENT=${1}

case $ARGUMENT in
	test)
		pytest -vrP src/tests/
		# break
		;;
    serve)
		uvicorn main:app --reload --app-dir src
		# break
		;;
	*)
		echo "Sorry, I don't understand"
		;;
  esac





# function F1()
# {
# echo 'I like bash programming'
# }

# F1