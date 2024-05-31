@echo off

:: Compile expanded CSS
call sass --style=expanded --no-source-map bootstrap.scss bootstrap.css

:: Compile minified CSS
call sass --style=compressed bootstrap.scss ..\css\bootstrap.min.css
