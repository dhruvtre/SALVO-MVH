# 23rd July 2025

- Running this experiment - started with "lets please begin the execution of this experiment."
- Notes: 
    * Started with checking various things.
    * Was unable to identify which code files were source code. 
    * Turned the text code files into repos for itself with files.
    * Intervened here to check if this was needed or if we could just use the txt files for code reference and make it work - said no.
    * Stopped the making new text files and offered the URL straight. This worked straight.
    * Started to install the requirements of the Dreamerv2 repository. 
    * Perhaps need a config or task to get the source code where relevant with the urls instead of the code in the repo.
    * Asked if we need to do this on local if we have to use modal as per task 1. 
    * Worked on Task 1 and Task 2 and started executing. Ran into some library dependency issues.
    * Ran into issues with mounting the source directory again.
    * Ran into issues with modal commands - SharedVolume
    * Unlike last run tried to deploy first instead of merely creating a temporary sandbox.
    * Kept running into setting up Modal errors - had to stop and ask it to refer to external sources.
    * Could not find the most relevant modal documentation - had to share the link. https://modal.com/docs/guide/project-structure
    * Had to quit and start again. Started from 0 so would need a checkpointing ability. Had to remind to make sure that we have tested task 1 and task 2 before we move on to task 3. 
    * Ran into errors with dm_control.suite.gym
    * Kept defaulting to installing the libraries in the local environment. 
    * In this case though it defaulted to doing run run.py instead of modal deploy run.py. It ran though and the modal app and storage volume was built. 
    * Might be helpful to frame the first task as getting the modal image up and running before writing additional code or add a reminder that the code files have to be written to be run on a modal image. 
    * Kept falling back on outdated ways to use the modal library without direct call out to use the one on the web. 
    * Had to add the local python package to the image definition. Auto mount did not work. Ran into some code issues with the data generation script. This was about how DM Control returns the state and action objects as dictionaries. Did not render the environment for pixel reconstruction.
    * Ran into some troubles with **GLFW** for rendering - not sure what this is. Headless rendering was causing persistent troubles. Had to be solved with internet research.
    * Had to request for addequate logging to be added everywhere.
    * Had to reques to use a GPU since servereless rendering was taking too long. This made everything easier and resolved the issues with GLFW and OpenGL also very quickly - showing data collection happening. 
    * The task 2 is to collect a dataset of 100k cartpole states on a random policy - in some sense this is an important task but we could have just used a public dataset for this too. Turns out that the best practice is actually to do this random policy play only. The alternatives could be D4RL or Minari. 
    * All data collection tasks should ideally have checkpointing available. 
    * Requested to add a sample function to sample a random set of images and states from the dataset and run it to check the quality fo our dataset. 
    * Need to check if during the data collection step we will need the position velocity data also or just the action and reward thing? 
    * All data collection tasks should clearly mention all the details that need to be collected. For instance - this data set does not include the position and velocity - only the image, action, reward and terminal status.
    * Says we do not need the position velocity at least for the SALVO training considering the idea is to only observe the image and render through VLM embeddings etc - and see if you can learn. 
    * Checking if we need it for the Dreamer implementation - turns out we don't. Even Dreamer and its main contribution in some sense is to take in low level actions and images and then turn them into latents that capture the physics without need for the actual low level environment details like position and velocity in the case of cartpole.


