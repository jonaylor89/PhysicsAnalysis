
# Windows Setup
*The set up is almost exactly the same for macOS and linux*
------------------------------
### Getting CSV file from an android device (Physics Toolbox Suite app)
1. Change setting in the Physics Toolbox Suite to Linear Acceleration
2. To begin collecting data, press the large red button
3. To stop the collection, press the large red button again
4. Change the filename to the desired name and email to yourself
---------------------------------------

**[!!!] Requires Python >3**

### Running Application
1. Download the CSV file from your email onto your laptop
2. Open a command prompt and change into the PhysicsAnalysis directory
3. Run the commands

```
C:\PhysicsAnalysis>pip install -r requirements.txt
C:\PhysicsAnalysis>python EmbeddingMPL.pyx
```

5. Click *file* in the top left corner and open your csv file 


![Window](https://github.com/jonaylor89/PhysicsAnalysis/blob/master/Images/GridLayout.png)
