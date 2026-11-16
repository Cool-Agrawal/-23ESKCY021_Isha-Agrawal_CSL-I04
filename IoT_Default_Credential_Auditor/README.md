# IoT Default-Credential Auditor

A Python command-line mini project that demonstrates the risks of
default credentials and weak passwords using two local test emulators.

-   Telnet-style TCP login emulator: `127.0.0.1:2323`
-   HTTP Basic Authentication emulator: `127.0.0.1:8000`

**Scope:** These are simulated services running on your own computer,
not physical IoT devices. The Telnet service is a simplified TCP login
demonstration, not a complete Telnet protocol implementation. HTTP
checking supports Basic Authentication only.

## 1. Requirements

-   Windows, macOS or Linux
-   Python 3.8 or later
-   Visual Studio Code or another editor (optional)
-   No third-party packages are required; the project uses Python's
    standard library.

Check Python:

``` bash
python --version
```

On Windows, you can also try:

``` bash
py --version
```

If Python is not installed, download it from
https://www.python.org/downloads/. On Windows, select **Add Python to
PATH** during installation.

## 2. Project structure

``` text
IoT_Default_Credential_Auditor/
├── main.py
├── telnet_emulator.py
├── http_emulator.py
├── auditor.py
├── dictionary_attack.py
├── brute_force.py
├── password_analyzer.py
├── README.md
├── data/
│   └── default_credentials.json
├── reports/
└── screenshots/
```

  -----------------------------------------------------------------------
  File                                Purpose
  ----------------------------------- -----------------------------------
  `main.py`                           Starts the emulators and displays
                                      the menu.

  `telnet_emulator.py`                Runs the local Telnet-style login
                                      emulator.

  `http_emulator.py`                  Runs the local HTTP Basic
                                      Authentication emulator.

  `auditor.py`                        Checks credentials, performs
                                      dictionary checks, analyses
                                      passwords and saves CSV results.

  `dictionary_attack.py`              Dictionary-attack demonstration
                                      wrapper.

  `brute_force.py`                    Bounded offline brute-force
                                      demonstration.

  `password_analyzer.py`              Password-strength analysis wrapper.

  `data/default_credentials.json`     Dummy credential combinations used
                                      in the lab.

  `reports/`                          Destination for generated CSV
                                      reports.

  `screenshots/`                      Store labelled screenshots here.
  -----------------------------------------------------------------------

## 3. Installation

1.  Download the project ZIP.

2.  Extract the ZIP file.

3.  Open the extracted `IoT_Default_Credential_Auditor` folder.

4.  Open that folder in VS Code, or open a terminal in that folder.

5.  Confirm Python is available:

    ``` bash
    python --version
    ```

No `pip install` command is needed.

## 4. Run the project

Open a terminal in the folder containing `main.py` and run:

``` bash
python main.py
```

If Windows does not recognise `python`, use:

``` bash
py main.py
```

The program starts the two local emulators and displays a menu:

``` text
1. Check Telnet default credentials
2. Check HTTP default credentials
3. Run dictionary attack on local service
4. Run bounded brute-force simulation
5. Analyze password strength
6. Run complete audit and generate CSV report
7. Exit
```

Enter the option number and follow the prompts.

## 5. Menu options

### 1 --- Check Telnet default credentials

Connects to `127.0.0.1:2323`, tries the dummy username-password pairs
from the JSON file and reports whether the local Telnet-style emulator
accepts a pair.

### 2 --- Check HTTP default credentials

Connects to `127.0.0.1:8000`, sends the configured credentials using
HTTP Basic Authentication and reports whether the local HTTP emulator
accepts a pair.

### 3 --- Run dictionary attack

Select the local service (for example, `telnet` or `http`) and enter the
requested username. The program tests passwords from its prepared list
against that local emulator.

### 4 --- Run bounded brute-force simulation

Enter a short dummy target such as `ABC`. The program generates
combinations using the small character set `ABCD`, up to its configured
maximum length and attempt limit. This exercise runs offline and does
not send guesses to either emulator.

### 5 --- Analyse password strength

Enter a dummy password. Basic checks flag characteristics such as very
short length, common-password usage, or use of only letters or only
digits. This is an educational heuristic, not a complete
password-security assessment.

### 6 --- Run complete audit and generate CSV report

Checks both local emulators and writes a CSV report in the `reports/`
folder.

### 7 --- Exit

Closes the program. Use `Ctrl+C` if you need to interrupt it.

## 6. Dummy credentials

The local emulators use intentionally weak test credentials:

  Emulator                    Username   Password
  --------------------------- ---------- ----------
  Telnet-style service        `admin`    `123456`
  HTTP Basic Authentication   `admin`    `admin`

These are lab-only values. Do not use real personal, college, workplace
or production credentials.

## 7. View the CSV report

After selecting option 6, open the `reports` folder. Open the generated
CSV file with Excel, LibreOffice Calc or a text editor.

Run the tests yourself and use the actual output in your college report.
Do not describe expected output as if it were observed.

## 8. Troubleshooting

  -----------------------------------------------------------------------
  Problem                             Solution
  ----------------------------------- -----------------------------------
  `python` is not recognised          Try `py main.py`. If that fails,
                                      install Python and enable **Add
                                      Python to PATH**.

  `can't open file 'main.py'`         Change to the extracted project
                                      folder containing `main.py`, then
                                      retry.

  Connection refused                  Start the project using
                                      `python main.py`; it starts the
                                      local emulators.

  Port already in use                 Close another project instance or
                                      local program using port `2323` or
                                      `8000`, then restart.

  CSV report not found                Select option 6 and check the
                                      project's `reports` folder.

  Program exits with an error         Read the full terminal error and
                                      verify that Python 3.8 or later is
                                      installed.
  -----------------------------------------------------------------------

## 9. Safety and ethical use

-   Test only the local emulators on your own computer.
-   Use only the supplied dummy credentials.
-   Do not target public IP addresses, websites, college networks,
    routers, cameras or devices belonging to others.
-   Do not enter real passwords or accounts.
-   The brute-force exercise is deliberately limited and offline.
-   No match means only that the tested list did not find a credential;
    it does not prove that a service is secure.

## 10. Project outcome

The project demonstrates default-credential checking, dictionary-based
password testing, bounded brute-force generation, basic
password-strength checks and CSV audit reporting.

For real IoT deployments, replace default credentials with unique strong
passwords, disable Telnet where possible, use encrypted management
protocols and restrict administrative access to trusted networks.
