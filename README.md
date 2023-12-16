# Setting Up and Running the App

Follow these steps to set up and run the application:

1. Open a command prompt.
2. Navigate to the folder using the `cd` command. Replace `"folder path here"` with the actual path to your folder:

    ```bash
    cd "folder path here"
    ```

3. Install the virtual environment using:

    ```sh
    python -m venv venv
    ```

4. Install required packages using:

    ```sh
    pip install -r requirements.txt
    ```

5. Activate the environment using:

    ```sh
    \venv\Scripts\activate
    ```

6. Run the app using:

    ```sh
    python run.py
    ```

It is running on port [http://127.0.0.1:5000](http://127.0.0.1:5000), so ensure this is set up correctly.

# Notes on the Development Process

Decided to make the application in Python as I like Python, and it allowed me to start writing application-relevant code straight away. I worked on the project for around 8-10 hours. There was a bit of time spent setting up the environment correctly. Had some trouble getting Flask and Pylance to work together in Visual Studio Code IDE, which I used. Then there was also some time spent deciding on the procedure to handle logins, and OAuth app was decided upon for the following reasons:

1. Token-based, so it removes dependency on username/password authentication and removes the need for my application to handle a user's GitHub credentials directly.
2. Single sign-on is always great for the user experience and gives the application the ability to grow in scope and include other applications in the future.

The issue, though, was the complexity of implementing the OAuth and handling the redirects. I have not worked with OAuth before, so there was some hard-earned hands-on experience to be gained here.

For help I used ChatGPT to help generate HTML templates and ad styling to these. I am a backend developer and hence have very limited experience setting up HTML from scratch. I also used chatGPT to help debugging when setting up OAuth and ensuring correct routing. Besides that I asked my brother and best friend to review and test my application as they are both developers. 

In terms of what can be done to improve the application in its current state:

1. Move some of the OAuth setup into a configuration file.
2. Move styling in HTML into a CSS file.
3. Implement star/unstarred functionality.
4. Error handling.
5. ...
