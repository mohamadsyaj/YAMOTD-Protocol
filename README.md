# YAMOTD (Yet-Another Message-Of-The-Day) Client & Server

A simple TCP client-server pair written in **Python 3**.  
The server maintains a single global “Message of the Day” (MOTD).  
Clients can retrieve or replace the MOTD, disconnect, or shut down the server (with a password).

---

## Files

| File | Purpose |
|------|---------|
| `server.py` | Listens on a configurable port (`PORT = 16948`), handles multiple clients with threads, and processes protocol commands. |
| `client.py` | Connects to the server, reads user commands from standard input, and displays server responses. |

---

## Protocol Commands

Command | Description | Typical Server Reply
--------|-------------|---------------------
`MSGGET` | Retrieve the current MOTD. | `200 OK` followed by the message text.
`MSGSTORE` | Replace the MOTD. Server first replies `200 OK`, then waits for the new text on the next line. | `200 OK` after storing.
`QUIT` | Disconnect the client only. | `200 OK`
`SHUTDOWN` | Shut down the server. Server replies `300 PASSWORD REQUIRED`, waits for a password, and shuts down if it matches `password` in `server.py`. | `200 OKAY` (success) or `301 WRONG PASSWORD`

---

## Running the Server

```bash
python server.py
Listens on all interfaces, port 16948 by default.

Accepts up to two simultaneous client connections.

To change the listening port, edit PORT at the top of server.py.

Default shutdown password is 123?abc; change password in server.py for production use.

Running the Client
bash
Copy
python client.py <server_ip>
Example (local machine):

bash
Copy
python client.py 127.0.0.1
The client prompts:

bash
Copy
Type command (MSGGET, MSGSTORE, QUIT, SHUTDOWN):
MSGSTORE then prompts for the replacement MOTD.

SHUTDOWN prompts for the server password.

Concurrency and Data Integrity
Each accepted client is handled in its own threading.Thread.

A threading.Lock (lock) guards access to the shared motd variable so concurrent MSGSTORE commands do not overlap.

When a correct SHUTDOWN is issued, the server closes its main socket, sets a flag, and spawns a dummy connection to unblock the listening thread for a graceful exit.

Extending the Project
Error Handling: Replace broad except blocks with targeted exception types.

Persistence: Save the MOTD to disk or a database so it survives server restarts.

Authentication: Implement per-client authentication rather than a single global password.

Encryption: Wrap the socket in TLS (using ssl) for secure communication.

License
© 2025 Mohamad Syaj. All Rights Reserved.
This source code is provided for personal or educational use only.
You may not sell, publish, or redistribute it without explicit written permission from the author.

Author
Mohamad Syaj
For questions or feedback, open an issue or contact the author directly.
