# Setting up your laptop

Data Science & AI, cohort 2026-08-03-DS-PT-AP-A

You need four things installed before Wednesday's class: Anaconda, VS Code, Git, and a GitHub account. This guide walks through all four, one at a time, for both Mac and Windows.

Work through it in order. Anaconda first, because the other steps are easier once it is there.

## Before you start

Set aside about 45 minutes. Most of that is waiting for downloads.

You will need:

- The password you use to log in to your own computer. The installers will ask for it.
- About 5 GB of free disk space.
- A reasonable internet connection. The Anaconda download is roughly 1 GB.

If you are using a work laptop that your employer manages, you may not be allowed to install software. Check before you start. If you are blocked, tell us in Slack and use Google Colab in the meantime. Colab runs in your browser and needs nothing installed.

---

## Step 1: Anaconda

Anaconda gives you Python plus the data science libraries plus Jupyter, all in one installer. This is the big one.

### Mac

First, find out which chip your Mac has. Click the Apple menu in the top left corner, then **About This Mac**. Look for the line that says **Chip**.

- If it says Apple M1, M2, M3 or M4, you have Apple Silicon.
- If it says Intel, you have an Intel Mac.

Now:

1. Go to https://www.anaconda.com/download
2. The page may ask for your email address. There is a link to skip this if you prefer.
3. Download the **macOS graphical installer** that matches your chip. Getting this wrong is the most common mistake, so check twice.
4. Open the file you downloaded. It ends in `.pkg`.
5. Click Continue through the screens, agree to the licence, and click Install.
6. Enter your Mac password when asked.
7. Wait. This takes several minutes and the progress bar sits still for a while near the end. That is normal.

To check it worked, open Terminal. Press `Command + Space`, type `Terminal`, press Enter. Then type this and press Enter:

```
conda --version
```

You should see a version number, for example `conda 26.1.1`. Yours may differ. The exact number does not matter.

If you see `command not found`, close Terminal completely and open it again, then try once more. The installer changes a setting that only applies to new Terminal windows.

### Windows

1. Go to https://www.anaconda.com/download
2. The page may ask for your email address. There is a link to skip this if you prefer.
3. Download the **Windows 64-bit graphical installer**.
4. Run the file you downloaded. It ends in `.exe`.
5. If Windows shows a blue box saying "Windows protected your PC", click **More info**, then **Run anyway**. This appears because the file is newly downloaded, not because anything is wrong.
6. Click Next, agree to the licence.
7. When asked who to install for, choose **Just Me (recommended)**.
8. Accept the default install folder.
9. On the Advanced Options screen, **leave "Add Anaconda3 to my PATH environment variable" unticked**. Anaconda's own instructions say to leave it off, and ticking it causes problems later. Leave "Register Anaconda3 as my default Python" ticked.
10. Click Install and wait. This takes several minutes.

To check it worked, open the Start menu, type `Anaconda Prompt`, and open it. Then type this and press Enter:

```
conda --version
```

You should see a version number, for example `conda 26.1.1`. Yours may differ. The exact number does not matter.

**Important for Windows users:** from now on, when this course tells you to open a terminal or run a command, use **Anaconda Prompt**, not Command Prompt and not PowerShell. Anaconda Prompt knows where Python lives. The other two do not, because of step 9.

---

## Step 2: VS Code

VS Code is a code editor. Jupyter notebooks are good for exploring data. VS Code is what you use when you are building something that other people will run.

### Mac

1. Go to https://code.visualstudio.com/download
2. Click the Mac download button.
3. Open the downloaded file. It unzips into an app called **Visual Studio Code**.
4. Drag that app into your **Applications** folder. If you skip this, VS Code will nag you every time you open it.
5. Open it from Applications.

If macOS says the app cannot be opened because it is from an unidentified developer, right-click the app and choose **Open** from the menu instead of double-clicking. Then click Open in the box that appears.

### Windows

1. Go to https://code.visualstudio.com/download
2. Click the Windows download button.
3. Run the downloaded `.exe`.
4. Accept the licence and the default folder.
5. On the "Select Additional Tasks" screen, tick **Add to PATH**. The other boxes are optional but "Add 'Open with Code' action" is handy.
6. Click Install, then Finish.

### Both: add the two extensions

Extensions are what make VS Code understand Python. You need two, and they are both published by Microsoft.

1. Open VS Code.
2. Click the Extensions button in the bar down the left side. It looks like four small squares, with one square separated from the rest.
3. Type `Python` in the search box. Find the one by **Microsoft** and click **Install**.
4. Clear the search box, type `Jupyter`. Again find the one by **Microsoft** and click **Install**.

There are lots of extensions with similar names. Check the publisher says Microsoft before you install.

---

## Step 3: Git

Git keeps the history of your work. GitHub, in the next step, is where that history gets published so employers can see it.

### Mac

Git may already be on your Mac. Open Terminal and run:

```
git --version
```

If you get a version number, you are done. Move to step 4.

If a box pops up offering to install the command line developer tools, click **Install** and wait. That gives you Git. When it finishes, run `git --version` again to confirm.

If neither happens, go to https://git-scm.com/downloads, download the macOS version, and run the installer.

### Windows

1. Go to https://git-scm.com/downloads
2. Click Windows. The download usually starts on its own.
3. Run the installer.
4. There are a lot of screens. Accept the default on every one, with a single exception below.
5. On the screen asking you to choose a default editor, pick **Use Visual Studio Code as Git's default editor** from the dropdown. The default option is a very old editor that is hard to get out of.
6. Keep clicking Next, then Install.

To check it worked, open **Anaconda Prompt** and run:

```
git --version
```

You should see a version number, for example `git version 2.50.1`. Yours may differ.

---

## Step 4: A GitHub account

1. Go to https://github.com
2. Click **Sign up**.
3. Use an email address you will still have in a year. A personal address is usually the better choice.
4. Choose your username carefully. It becomes part of the web address for everything you build, and it goes on your CV. Something close to your real name works well. Something you would not want to explain in an interview does not.
5. Confirm your email address when GitHub sends you the message. Your account is not fully active until you do.

You do not need to create any repositories yet. We do that together in class.

---

## Step 5: Check everything

Open Terminal on Mac, or Anaconda Prompt on Windows, and run these four commands one at a time:

```
conda --version
python --version
jupyter --version
git --version
```

All four should print a version number. If any of them says `command not found` or `is not recognized`, that tool did not install properly. Go back to its step above.

There is also a cell at the bottom of the class notebook, `Lab0_Session1_Walkthrough.ipynb`, that runs all of these checks at once and prints a tidy report. Run it once you are set up and post the result in Slack. That tells us you are ready without you having to explain anything.

---

## When something goes wrong

Everything below has happened to someone before. None of it means you have broken anything.

**"conda: command not found" on Mac.** Close Terminal completely, using `Command + Q` rather than the red button, then open it again. The installer only affects new Terminal windows.

**"'conda' is not recognized" on Windows.** You are in Command Prompt or PowerShell. Open Anaconda Prompt from the Start menu instead.

**"Windows protected your PC".** Click More info, then Run anyway. Windows shows this for any recently downloaded installer.

**Mac refuses to open the installer.** Right-click it and choose Open, rather than double-clicking.

**The download is taking forever.** Anaconda is about 1 GB. On a slow connection this is a genuine 20 minute wait. Start it and go and do something else.

**Not enough disk space.** Anaconda needs several GB once unpacked. Empty your Downloads folder and your Trash, then try again.

**Your work laptop blocks installers.** Do not fight it. Tell us in Slack and use Google Colab, which needs nothing installed, until you can use a personal machine.

## Still stuck

Post in Slack with a screenshot of what you are seeing. A screenshot gets you an answer far faster than a description does. Include which operating system you are on.

You can also bring it to the 30 minute support session before class. We can share screens and fix it there.

Do not sit on a broken setup and hope it resolves itself. It is a 10 minute problem this week and a serious one by week 4.
