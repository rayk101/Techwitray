# Run your first project

You only need to set this up once. Start with the included examples.

## 1. Get Python

Install [Python](https://www.python.org/downloads/) — version 3.11 or newer.

On Windows, if the installer offers **Add Python to PATH**, tick it.

## 2. Download the projects

[Download Techwitray](https://github.com/rayk101/Techwitray/archive/refs/heads/main.zip).

Open the downloaded ZIP and **extract it**. On Windows, right-click it and choose **Extract All**. On Mac, double-click it.

Open the extracted folder. You should see `start.py` and `START_WINDOWS.bat`.

## 3. Pick a project

**Windows:** Double-click **START_WINDOWS.bat**. A menu will open. Type a number and press Enter.

**Mac:** Right-click the extracted folder in Finder, then choose **Services → New Terminal at Folder**. Type this and press Enter:

```bash
python3 start.py
```

**Linux:** Open a terminal in the extracted folder and run the same command.

Choose **1** for the spending tracker. It uses sample expenses, so you do not need to upload anything.

You will see the result on screen. Your saved reports are in the **output** folder. Type **q** at the menu to quit.

## Make one small change

Open `projects/01-expense-analyzer/sample.csv` in a text editor such as Notepad or TextEdit. Change `-84.32` to `-90.00`, save the file, and run project **1** again.

The Food total changes from **148.00** to **153.68**. You just changed the input and saw the result.

## Stuck?

- **The window says Python is missing:** Finish installing Python, then try again.
- **“Can't open file start.py”:** Open the extracted folder first. The file must be inside the folder where you run the command.
- **Not sure what an error means:** Copy the error into Claude and ask, “Explain this simply and give me one step to fix it.”

[Back to the 10 projects](../README.md)
