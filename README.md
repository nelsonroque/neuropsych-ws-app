neuropsych-ws-app
==================

Real-time collaborative canvas for cognitive research and behavioral studies.
Built with FastAPI + WebSockets + Tailwind UI.

Admins and participants share an image space for synchronous tasks, cursor tracking, and interaction monitoring.

--------------------
FEATURES
--------------------
- Live cursor tracking across users
- Admin image control (click-to-swap)
- Participant list with live updates
- Responsive Tailwind UI layout
- Scales to 100+ concurrent users
- Supports multi-admin oversight
- Auto WebSocket reconnects
- Sticky sidebar with branding

--------------------
EXAMPLE SCENARIOS
--------------------

One admin + two participants:
    http://127.0.0.1:8000/canvas/test1/admin/admin1
    http://127.0.0.1:8000/canvas/test1/participant/user42
    http://127.0.0.1:8000/canvas/test1/participant/user43

One admin + 100 participants:
    http://127.0.0.1:8000/canvas/test2/admin/admin1
    http://127.0.0.1:8000/canvas/test2/participant/user1
    ...
    http://127.0.0.1:8000/canvas/test2/participant/user100

Two admins overseeing 100 participants:
    http://127.0.0.1:8000/canvas/test3/admin/admin1
    http://127.0.0.1:8000/canvas/test3/admin/admin2
    http://127.0.0.1:8000/canvas/test3/participant/user1
    ...
    http://127.0.0.1:8000/canvas/test3/participant/user100

Three admins watching one participant:
    http://127.0.0.1:8000/canvas/test4/admin/admin1
    http://127.0.0.1:8000/canvas/test4/admin/admin2
    http://127.0.0.1:8000/canvas/test4/admin/admin3
    http://127.0.0.1:8000/canvas/test4/participant/user1

--------------------
SETUP
--------------------

1. Clone and install dependencies

    git clone https://github.com/your-username/neuropsych-ws-app.git
    cd neuropsych-ws-app
    pip install fastapi uvicorn jinja2

2. Folder structure

    .
    ├── app.py                  # FastAPI app
    ├── templates/
    │   └── canvas.html         # Main UI template
    ├── static/
    │   ├── img1.png
    │   ├── img2.png
    │   ├── img3.png
    │   └── blank.png

3. Run the app

    uvicorn app:app --reload

Then open any of the example URLs in your browser to start testing.

--------------------
CUSTOMIZATION IDEAS
--------------------
- Export mouse paths for analysis
- Add audio or video communication
- Time-locked image sequences
- Integrate task modules (e.g., Go/No-Go, Stroop)
- User authentication with JWT/API keys
- MongoDB support for session logs

--------------------
ATTRIBUTION
--------------------
Made with love by [Dr. Nelson Roque](https://www.linkedin.com/in/nelsonroque/)

Inspired by research needs in neuropsychology, real-time cognitive testing,
and collaborative behavioral paradigms.

--------------------
LICENSE
--------------------
MIT — open source, modify and contribute freely.
