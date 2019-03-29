Welcome to PG-hci!

This is the git repository for our project "Firedrills for Administrators" which is part of our Bachelor project. With this prototype, we testeded the concept of firedrills on a few administrators. A firedrill is a repeated training of a critical scenario. We implemented 3 scenarios working on Oracle DB. For more information on our project, read our report (it is written in German though).

To run, you need the following packages:
- Python2.7 (https://docs.python.org/2/install/)
- wxPython (https://wiki.wxpython.org/How%20to%20install%20wxPython)
- matplotlib (https://matplotlib.org/users/installing.html)
- jsonpickle (https://jsonpickle.github.io/)
	
To run the tool properly, you need a Virtual Machine running Windows Server with Oracle DB installed. We can't publish our VM for license reasons, so you will have to set up one for yourself. DO NOT test this tool on a live system. The tool runs batch scripts which modify (and crash) the Oracle DB.

Next, put some dummy data into the database and set up a shared folder. You might need to modify the code if your shared folder is not at F:\repo\PG-hci. You can do this in Statistics.py. The shared folder will then hold data on how long a participant needed for a drill and a nice plotted graph to visualise that data. Then run the batch script RUN.bat to start the tool.

If sou want to add more scenarios, that's pretty easy. Just add a folder to scenarios with the batch-scripts checkSystem.bat, fix.bat, startDrill.bat and put descriptions and hints into info.json. Then, add a new button for your scenario in Drill.py and bind it to the same function as the other DrillButtons. To visualise your new scenario in the statistics graph, change NO_SCENARIOS in Statistics.py and set the plot details for it. Just look into the code, you will find comments pointing out exactly where you have to do what.