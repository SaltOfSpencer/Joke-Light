**Important Information**
- First time use of the program -> cd into the folder and run the batch script (windows only - sorry)
- To run the program on a video, you must drop an mp4 file into the videos folder before starting the program
 - The sign-in details that will grant access to the main program are 
user: admin
password: homunculus
- The skip button in the top left corner of the sign-in page exists as a navigational tool, be sure to test other user password combinations!
- Inputting hacker as the username will result in a music file being played, which will hold the program until the song is finished


**Introduction**
In the modern day, technology is considered to be the favoured form of communication for the general public. However, deficits in social communication caused by neurodiverse conditions such as autism, form a societal divide that is only emphasised by technology. We intend to use technology to make social interaction more accessible for everyone, without the barrier or confusing connotation or misleading facial expressions.

**Developing a Tech Stack**
The most important part of the software is the tone-labelled captioning feature. The ideal goal would be realtime live captioning running in conjunction with all the sentiment analysis elements; however, whilst real-time voice transcription libraries were available, there were audio input issues in both Windows and Debian which proved prohibitive to submitting such a solution in the given timeframe
In order to produce software that detects facial emotions, it was first necessary to be able to find and crop faces from a given image. Whilst a Convolutional Neural Network (CNN) may have been able to produce more accurate detections overall, we opted for the Haar Cascade Classifier due to its computational efficiency, a trait pertinent to both deployment on the test machine (a low-tier notebook), and widespread usage of the software overall. We used the pre-trained models included with OpenCV due to time constraints (24 hours), which allowed us to identify faces in real-time. The integration with OpenCV allowed us to crop to the face involved (we deemed the largest face on the screen to be the most relevant as they were most likely to be the speaker). The program runs entirely offline for data protection purposes, and produces a dictionary of tone tags, emotion classification and the sentence they correspond to.

**Developing a User Interface**
We wanted to ensure our program was as smooth running and easy to use as possible. As we had limited knowledge of front-end development, we decided to make use of the Python GUI library tkinter. As we already knew the language it would make the process easier and as a bonus, it made connecting with the back-end, already written in Python, relatively simple. Using Canva we developed decorative buttons, titles and icons to decorate our GUI. 

**Combining front-end and back-end**
Finally we had to take our result from the analysis process and output it in a readable format on the GUI. We did this by concatenating each phrase with its measured emotion, a combination of its tone tag and emotion classification. This resulted in 14 unique emotions overall, ranging from disgust to pride. Testing this program on different Youtube videos we were able to demonstrate a general accuracy in tone description, and excellent speech to text capabilities.

**Beyond the Hackathon**
Included in the GUI are a few seemingly unfinished sections, such as the ability to create an account and to see your processing history. With more time this program would be able to save the GUI output as a text file on the users account so that repeating processing for the same video would not be necessary. The tick boxes on the program options page allow the user to request the input of either tone tags or facial expressions into the emotion classification, both, or neither for simple captioning. 
