@REM ----------------------------------------------------------------------------
@REM  Copyright 2001-2006 The Apache Software Foundation.
@REM
@REM  Licensed under the Apache License, Version 2.0 (the "License");
@REM  you may not use this file except in compliance with the License.
@REM  You may obtain a copy of the License at
@REM
@REM       http://www.apache.org/licenses/LICENSE-2.0
@REM
@REM  Unless required by applicable law or agreed to in writing, software
@REM  distributed under the License is distributed on an "AS IS" BASIS,
@REM  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
@REM  See the License for the specific language governing permissions and
@REM  limitations under the License.
@REM ----------------------------------------------------------------------------
@REM
@REM   Copyright (c) 2001-2006 The Apache Software Foundation.  All rights
@REM   reserved.

@echo off

set ERROR_CODE=0

:init
@REM Decide how to startup depending on the version of windows

@REM -- Win98ME
if NOT "%OS%"=="Windows_NT" goto Win9xArg

@REM set local scope for the variables with windows NT shell
if "%OS%"=="Windows_NT" @setlocal

@REM -- 4NT shell
if "%eval[2+2]" == "4" goto 4NTArgs

@REM -- Regular WinNT shell
set CMD_LINE_ARGS=%*
goto WinNTGetScriptDir

@REM The 4NT Shell from jp software
:4NTArgs
set CMD_LINE_ARGS=%$
goto WinNTGetScriptDir

:Win9xArg
@REM Slurp the command line arguments.  This loop allows for an unlimited number
@REM of arguments (up to the command line limit, anyway).
set CMD_LINE_ARGS=
:Win9xApp
if %1a==a goto Win9xGetScriptDir
set CMD_LINE_ARGS=%CMD_LINE_ARGS% %1
shift
goto Win9xApp

:Win9xGetScriptDir
set SAVEDIR=%CD%
%0\
cd %0\..\.. 
set BASEDIR=%CD%
cd %SAVEDIR%
set SAVE_DIR=
goto repoSetup

:WinNTGetScriptDir
for %%i in ("%~dp0..") do set "BASEDIR=%%~fi"

:repoSetup
set REPO=


if "%JAVACMD%"=="" set JAVACMD=java

if "%REPO%"=="" set REPO=%BASEDIR%\lib

set CLASSPATH="%BASEDIR%"\etc;"%REPO%"\demetra-tss-2.2.5.jar;"%REPO%"\demetra-utils-2.2.5.jar;"%REPO%"\guava-32.1.2-jre.jar;"%REPO%"\failureaccess-1.0.1.jar;"%REPO%"\listenablefuture-9999.0-empty-to-avoid-conflict-with-guava.jar;"%REPO%"\java-io-xml-0.0.30.jar;"%REPO%"\java-io-base-0.0.30.jar;"%REPO%"\java-io-xml-bind-0.0.30.jar;"%REPO%"\jaxb-api-2.4.0-b180830.0359.jar;"%REPO%"\javax.activation-api-1.2.0.jar;"%REPO%"\jaxb-runtime-2.4.0-b180830.0438.jar;"%REPO%"\txw2-2.4.0-b180830.0438.jar;"%REPO%"\istack-commons-runtime-3.0.7.jar;"%REPO%"\stax-ex-1.8.jar;"%REPO%"\FastInfoset-1.2.15.jar;"%REPO%"\demetra-tstoolkit-2.2.5.jar;"%REPO%"\demetra-workspace-2.2.5.jar;"%REPO%"\picocli-4.7.6.jar;"%REPO%"\picocli-jansi-graalvm-1.2.0.jar;"%REPO%"\jansi-1.18.jar;"%REPO%"\slf4j-jdk14-2.0.13.jar;"%REPO%"\slf4j-api-2.0.13.jar;"%REPO%"\demetra-spreadsheet-2.2.5.jar;"%REPO%"\spreadsheet-api-2.5.9.jar;"%REPO%"\spreadsheet-standalone-2.5.9.jar;"%REPO%"\spreadsheet-poi-2.5.9.jar;"%REPO%"\poi-ooxml-5.2.5.jar;"%REPO%"\poi-5.2.5.jar;"%REPO%"\commons-codec-1.16.0.jar;"%REPO%"\commons-math3-3.6.1.jar;"%REPO%"\SparseBitSet-1.3.jar;"%REPO%"\poi-ooxml-lite-5.2.5.jar;"%REPO%"\xmlbeans-5.2.0.jar;"%REPO%"\commons-compress-1.25.0.jar;"%REPO%"\commons-io-2.15.0.jar;"%REPO%"\curvesapi-1.08.jar;"%REPO%"\commons-collections4-4.4.jar;"%REPO%"\xml-apis-1.0.b2.jar;"%REPO%"\log4j-to-slf4j-2.23.1.jar;"%REPO%"\log4j-api-2.23.1.jar;"%REPO%"\demetra-jdbc-2.2.5.jar;"%REPO%"\java-sql-jdbc-1.0.6.jar;"%REPO%"\demetra-odbc-2.2.5.jar;"%REPO%"\java-sql-odbc-1.0.6.jar;"%REPO%"\java-io-win-0.0.30.jar;"%REPO%"\java-sql-lhod-1.0.6.jar;"%REPO%"\demetra-sdmx-2.2.5.jar;"%REPO%"\demetra-common-2.2.5.jar;"%REPO%"\opencsv-2.3.jar;"%REPO%"\jwsacruncher-2.2.5.jar

set ENDORSED_DIR=lib/ext
if NOT "%ENDORSED_DIR%" == "" set CLASSPATH="%BASEDIR%"\%ENDORSED_DIR%\*;%CLASSPATH%

if NOT "%CLASSPATH_PREFIX%" == "" set CLASSPATH=%CLASSPATH_PREFIX%;%CLASSPATH%

@REM Reaching here means variables are defined and arguments have been captured
:endInit

%JAVACMD% %JAVA_OPTS% -Djava.util.logging.config.file="%BASEDIR%"/etc/logging.properties -classpath %CLASSPATH% -Dapp.name="jwsacruncher" -Dapp.repo="%REPO%" -Dapp.home="%BASEDIR%" -Dbasedir="%BASEDIR%" ec.jwsacruncher.App %CMD_LINE_ARGS%
if %ERRORLEVEL% NEQ 0 goto error
goto end

:error
if "%OS%"=="Windows_NT" @endlocal
set ERROR_CODE=%ERRORLEVEL%

:end
@REM set local scope for the variables with windows NT shell
if "%OS%"=="Windows_NT" goto endNT

@REM For old DOS remove the set variables from ENV - we assume they were not set
@REM before we started - at least we don't leave any baggage around
set CMD_LINE_ARGS=
goto postExec

:endNT
@REM If error code is set to 1 then the endlocal was done already in :error.
if %ERROR_CODE% EQU 0 @endlocal


:postExec

if "%FORCE_EXIT_ON_ERROR%" == "on" (
  if %ERROR_CODE% NEQ 0 exit %ERROR_CODE%
)

exit /B %ERROR_CODE%
