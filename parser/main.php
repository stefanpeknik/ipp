<?php

// checks if the number of arguments is correct
if ($argc > 2) {
    exit(10);
}
// checks if the argument is --help
if ($argc == 2) {
    if ($argv[1] == '--help') {
        echo("print help");
    }
    else {
        exit(10);
    }    
}
