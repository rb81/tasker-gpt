# TaskerGPT

![TaskerGPT](/header.png)

**TaskerGPT** is a simple web application that allows users to input an objective that the LLM autonomously breaks down into tasks and executes. The system is capable of refining the objective and the derived set of tasks (to ensure they are capable of being executed by the LLM). The LLM is provided with the option to execute the tasks on its own, or "request help" which triggers an LLM-to-LLM dialogue to help resolve any issues with the task. (The executing agent assumes it is getting help from a human supervisor.)

## Features

- **Objective Processing**: Input an objective (which is autonomously refined).
- **Task Generation**: Automatically generate a list of tasks based on the objective (which is autonomously refined).
- **Task Execution**: Execute tasks with the help of OpenAI's language models.
- **Real-time Logging**: View logs of the task execution process in real-time.
- **Result Display**: View and download the results of the task execution.

## Benefits

Using this system, answers may be improved as the LLM is able to break down the task into smaller steps and execute them with LLM assistance as and when needed. This project is meant to serve as a simple proof of concept and has not been rigorously tested. Initial experiments do show promise, though. This system is effective in coming up with novel ideas when a detailed brief is provided by the user.

See [samples/tasker-gpt.md](samples/tasker-gpt.md) and [samples/chatgpt.md](samples/chat-gpt.md) for a simple comparison.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/rb81/tasker-gpt.git
   cd tasker-gpt
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   - Create a `.env` file in the root directory.
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_openai_api_key
     ```

## Usage

1. **Run the application**:
   
   Using Python -m:

   ```bash
   python -m app.app
   ```

   Using Gunicorn:

   ```bash
   gunicorn --worker-class eventlet -w 1 wsgi:app
   ```

2. **Access the application**:
   - Open your web browser and go to `http://localhost:5000` (or the appropriate URL if running with Gunicorn).

3. **Enter an objective**:
   - Input your objective in the text field and click "Execute".
   - View the execution log and results on the same page.
   - Download or copy the results as plain text.

## Logging

- Logs are emitted to the console and displayed in the web interface.
- Logs include information about the processing of objectives, task generation, and task execution.

## Shortcomings / Limitations

- Once started, the server cannot be shut down from the web interface.
- Refreshing the page will reconnect the client to the server and the process will continue from where it left off.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Transparency Disclaimer

[ai.collaboratedwith.me](ai.collaboratedwith.me) in creating this project.