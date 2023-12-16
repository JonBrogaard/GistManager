# Setting Up and Running the App
Follow these steps to set up and run the application:
1. Open a command prompt.
2. Navigate to the folder using the `cd` command. Replace `"folder path here"` with the actual path to your folder:
    ```bash
    cd "folder path here"
    ```
3. Install virtual enviroment using: 
    ```sh
    python -m venv venv
    ```
4. Install required packages using: 
    ```sh
    pip install -r requirements.txt
    ```
5. Activate environment using:
    ```
    \venv\Scripts\activate
    ```
6. Run the app using: 
    ```sh
    python run.py
    ```
It is running on port http://127.0.0.1:5000 so ensure this is set up correctly