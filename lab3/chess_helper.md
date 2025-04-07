# Chess Terminology Helper - Lab3

## Summary
It's a small application that connects via an API to a model in LM Studio. The model has a defined prompt system to respond according to the topic. In this case, it focuses on providing explanatory help, in different languages ​​and levels, on chess terms.

## Tools used

### LM Studio: 
As local LLM hoster of my LLM model. I used because is an easy tool and I had it since the previous session and I investigate more about it and how to integrate it in python
![alt text](image-7.png)

### Tkinder: 
For the creation fo the interface as GUI framework. Use of buttom, fram and scrolling functions for a better interface can be seen. I use it because we have seen it in previously semesters and I am related with it.

### Threading: 
For execution in the background with out closing the Graphical Interface. Because I want to avoid blocking the graphic window during execution and be available in case the response takes a long time. This came after a try that the window froze it and I can do nothing until it give me the solution.

## Development

### Build the interface

![Definitions](Captura%20de%20pantalla%202025-04-07%20125208.png)

Defining the model that Im going to use and setting the initialations to start with the widgets im going to put on my Graphic Interface. For the creation Tkinter functions where use as being a fast and easy way to create a simply interface.

#### Main widgets:

- Ask box:

    Here the user can type for the concepts or terms about chess that has
![Ask box](Captura%20de%20pantalla%202025-04-07%20125639.png)

- Language settings:

    The user can select the language in which the model is going to answer, as the user can ask in any language he have to choose in which language wants to be answered, being English the default one.
![Language](Captura%20de%20pantalla%202025-04-07%20125821.png)

- Expertise answer:

    Also the users can select the level of expertisement that they want on their answer in order to meet their necessities.
![Expertise](Captura%20de%20pantalla%202025-04-07%20170646.png)

- Common terms searcher:

    The interface offer simple buttoms that are attached to common terms in chess to be search directly as an extra functionality.
![Common terms 1](Captura%20de%20pantalla%202025-04-07%20130255.png)
![Common terms 2](Captura%20de%20pantalla%202025-04-07%20171239.png)

- Answer box:

    Place where the answer of the LLM is going to appear and the user can scroll on it to see the full answer.
![Answer box](Captura%20de%20pantalla%202025-04-07%20171923.png)

### Search and interactions

For this part all the send, recieve and managing the info and process of sending and recieving.

#### Send and recieve

- Send:

    Selecting the term on the ask box and deleting the previous so the LLM can recieve it clearly is the main function in sending.
![Send](image.png)

- Recieve:

    Taking the answer of the LLM and printing it on the answer box, deleting previously all the content in this box to have a white space to print the new answer.
![Recieve](image-1.png)

Basically this are the 2 main funtions, however the interactions and process while this two functions are more extensive.

#### Interactions

The managing od sending and recieving process make sure that the app works according to the task is made for.

##### Sending:

Inside sending there are 3 main parts:

- Answer settings:

    Basically saving the language and expertise configurations of the user to use it in the system prompt
![Answer settings](image-2.png)

- Functionality settings:

    This part is more for a proper development of the actions and well working of the app. In this case, after the sending of the term, all the functions of the graphic window are deactivated in order to not to interfere during the process.
![Funct settings1](image-3.png)

    Also to mainteining the graphic window open the process is carry in the background unless the window is close(Daemon=True), here is were I use the threading library
![Funt settings2](image-4.png)

- System Prompt:

    This part is key for the distinction of a common LLM and a the app. In this prompt is what is sent to the LLM to give an answer according to the main functionality of the app. Here the user settings and the term to be found is settle, and in addition to this points that have to explain to refering to the term searched and manage terms that are not related with chess, not explaining it and raising a message offering terms that are related with chess that the user might refer to.

![System Prompt](image-5.png)

##### Recieving:

The recieving is very similar to what I describe previously adding a interaction with the graphic window. In this case the app revieve the prompt and do the same process as previously and after that reactive all the functions on the graphic window for a new term explanation.

![Recieving](image-6.png)

### Error handle

The app is provided with this functions just to avoid problems and normally consist in restarting the process and enter a new term to search, by giving examples because of missunderstanding or directly error during the process.

## Results

The results of a provided term in the buttoms availeable generated with custom settings and the response.
![Result](Captura%20de%20pantalla%202025-04-07%20133842.png)