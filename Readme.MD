
# 💬 Multi-Client Socket Chat Application

A lightweight, concurrent multi-client command-driven chat application written in Python using native TCP sockets and multi-threading.

---

## 🔹 Features

* **Concurrent Connections:** Handles multiple clients simultaneously using Python's `threading` library.
* **Thread Safety:** Uses a synchronization `threading.Lock` to avoid race conditions when adding, removing, or accessing clients.
* **Environment Configuration:** Supports setting custom host and port variables using a `.env` file via `python-dotenv`.
* **Command-Based Protocol:**
* `/join <username>`: Authenticates and registers a handle before chatting.
* `/send <message>`: Broadcasts messages to all other joined room participants.
* `/leave`: Gracefully disconnects from the chat room.



---

## 🔹 Protocol & Commands

| Command | Usage | Description |
| --- | --- | --- |
| `/join` | `/join <username>` | Registers your chosen username. Prevents duplicate usernames. |
| `/send` | `/send <message>` | Broadcasts a message to everyone in the room. Requires `/join` first. |
| `/leave` | `/leave` | Disconnects the socket and broadcasts departure to the room. |

---

## 🔹 Project Structure

```text
.
├── .env                  # Optional: custom HOST and PORT configuration
├── server.py             # Multi-threaded TCP chat server
├── client.py             # Chat client with background listener thread
└── README.md             # Project documentation

```

---

## 🔹 Installation & Requirements

* Python 3.8+
* `python-dotenv`

Install the required dependency:

```bash
pip install python-dotenv

```

*(Optional)* Create a `.env` file in the root directory:

```env
HOST=0.0.0.0
PORT=4444

```

---

## 🔹 How to Run

### 1. Install Process

Run the chat server first:

```bash
git clone https://github.com/chatApp
cd chatApp/

```
### 2. Start the Server

Run the chat server first:

```bash
python server.py

```

Expected output:

```text
Chat server listening on 0.0.0.0-4444

```

### 3. Connect Clients

Open two or more separate terminal windows and run a client in each:

```bash
python client.py

```

---

## 🔹 Usage Example

### Client 1 (`Alice`):

```text
[SYSTEM] Connected. Type '/join <username>' to enter the Chat.
/join Alice
[<-] Joined successfully as Alice. Use '/send <message>' to send message
[JOIN] Alice registered from ('127.0.0.1', 52341)

/send Hello everyone!
[OK] Message send.
[Bob : Hey Alice!]
/leave
[SYSTEM] you left the chat.Good bye broo

```

### Client 2 (`Bob`):

```text
[SYSTEM] Connected. Type '/join <username>' to enter the Chat.
/join Bob
[<-] Joined successfully as Bob. Use '/send <message>' to send message
[<-] Alice joined the chat!
[Alice : Hello everyone!]

/send Hey Alice!
[OK] Message send.
[->] Alice has left the Chat

```

---

## 🛠️ Author

Created by **SRIDHARANITHARAN**