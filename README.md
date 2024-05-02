## Installation

Before running the script, ensure your system is set up with the necessary dependencies.

### Python Installation

1. **Download Python 3.8.1**:
   - Visit [Python.org](https://www.python.org/downloads/release/python-381/) and download the Python 3.8.1 installer for your operating system.
   - Follow the installation instructions, making sure to check the box that says **"Add Python 3.8 to PATH"** at the beginning of the installation process.

### Virtual Environment (Optional)

Setting up a virtual environment for Python projects is recommended as it allows you to manage dependencies separately for each project.

2. **Create and Activate Virtual Environment**:
   - Open a terminal or command prompt.
   - Navigate to your project directory:
     ```bash
     cd DNA
     ```
   - Create a virtual environment:
     ```bash
     python -m venv venv
     ```
   - Activate the virtual environment:
     - On Windows:
       ```bash
       venv\Scripts\activate
       ```
     - On macOS and Linux:
       ```bash
       source venv/bin/activate
       ```

### Install Selenium and Other Dependencies

3. **Install Selenium**:
   - With your virtual environment activated, install Selenium and web driver manager using pip:
     ```bash
     pip install selenium
     pip install webdriver-manager
     ```

### Additional Libraries

### Check Installation

7. **Verify All Dependencies**:
   - Ensure all installations are correctly done by checking the installed packages:
     ```bash
     pip list
     ```

### Update pip (Optional)

8. **Upgrade pip**:
   - It's a good practice to keep pip updated:
     ```bash
     python -m pip install --upgrade pip
     ```

## Running the Script

To run the script, navigate to the script's directory and run:

```bash
python src/main.py
 ```

Script will output runtime logs using Python native logger.  