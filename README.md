# ⚡ Postly — REST Explorer

> **A sleek, full-featured CRUD web application** built with Flask and the [JSONPlaceholder](https://jsonplaceholder.typicode.com) API. Browse, publish, revise, and retire posts — all wrapped in a premium dark UI.

---

## ✨ Features at a Glance

| Feature | Details |
|---|---|
| 📋 **Explore Posts** | Paginated archive with live search & sort |
| ✍️ **Publish Post** | Submit new content via `POST /posts` |
| ✏️ **Revise Post** | Full replace (`PUT`) or partial update (`PATCH`) |
| 🗑️ **Retire Post** | Two-step confirmation before `DELETE` |
| 📖 **Post Detail** | Full post view + threaded comments panel |
| 👤 **Author Profiles** | Browse all posts by any of 10 authors |
| 📊 **Live Dashboard** | Real-time stats — posts, users, comments, albums |
| ⌨️ **Keyboard Shortcuts** | `G` Explore · `C` Publish · `U` Revise · `D` Retire · `H` Home |
| 🔔 **Auto-dismiss Toasts** | Success / error notifications that slide in and fade out |
| ⚡ **Parallel API Fetching** | Home page stats loaded concurrently via `ThreadPoolExecutor` |

---

## 🗂 Project Structure

```
Postly/
├── manage.py                  # Flask app — all routes & logic
├── templates/
│   ├── base.html              # Shared layout: sidebar, topbar, toasts
│   ├── index.html             # Dashboard with hero image & live stats
│   ├── getData.html           # Explore posts (search, sort, paginate)
│   ├── postDetail.html        # Single post + comments
│   ├── userPosts.html         # Posts by author
│   ├── createData.html        # Publish new post
│   ├── updateData.html        # Revise post (PUT / PATCH)
│   └── deleteData.html        # Retire post (DELETE)
├── public/
│   ├── hero.png               # Hero illustration (dashboard)
│   └── ...                    # Other static assets
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### 1 — Clone the repo

```bash
git clone https://github.com/your-username/postly.git
cd postly
```

### 2 — Create a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3 — Install dependencies

```bash
pip install flask requests
```

### 4 — Run the app

```bash
py manage.py
```

Then open **[http://127.0.0.1:5000](http://127.0.0.1:5000)** in your browser. 🎉

---

## 🌐 API Routes

| Method | Route | Description |
|--------|-------|-------------|
| `GET` | `/` | Dashboard — live stats & navigation |
| `GET` | `/api/FetchData` | Paginated list of all posts |
| `GET` | `/api/PostDetail/<id>` | Single post + its comments |
| `GET` | `/api/UserPosts?userId=<n>` | Posts filtered by author |
| `GET` + `POST` | `/api/CreateData` | Publish a new post |
| `GET` + `POST` | `/api/UpdateData` | Revise post via PUT or PATCH |
| `GET` + `POST` | `/api/DeleteData` | Retire a post with confirmation |

---

## ⌨️ Keyboard Shortcuts

Press any key while **not** focused on an input field:

| Key | Action |
|-----|--------|
| `H` | Go to Home / Dashboard |
| `G` | Go to Explore Posts |
| `C` | Go to Publish a Post |
| `U` | Go to Revise a Post |
| `D` | Go to Retire a Post |

---

## 🛠 Tech Stack

- **Backend** — [Flask](https://flask.palletsprojects.com/) · Python 3.x
- **Templating** — Jinja2 (via Flask)
- **HTTP Client** — `requests` library
- **API** — [JSONPlaceholder](https://jsonplaceholder.typicode.com) (free fake REST API)
- **Frontend** — Vanilla HTML · CSS · JavaScript (zero frameworks)
- **Fonts** — [Inter](https://fonts.google.com/specimen/Inter) via Google Fonts

---

## 🎨 Design System

The UI is built on a handcrafted dark design token system defined in `base.html`:

```css
--bg:      #080d16   /* Page background      */
--s1:      #0e1623   /* Surface (cards)       */
--indigo:  #6366f1   /* Primary accent        */
--sky:     #38bdf8   /* Secondary accent      */
--rose:    #f43f5e   /* Danger / delete       */
--emerald: #10b981   /* Success               */
--amber:   #f59e0b   /* Warning / PUT         */
```

---

## 📌 Notes

- JSONPlaceholder is a **mock API** — `POST`, `PUT`, `PATCH`, and `DELETE` requests return simulated responses. Data is **not** persisted.
- The app uses `ThreadPoolExecutor` to fetch dashboard stats (posts, users, comments, albums) **in parallel** for fast page loads.
- All flash messages auto-dismiss after **4.5 seconds**.

---

## 📄 License

MIT © 2025 — Free to use, fork, and learn from.

---

<div align="center">
  <sub>Built with ❤️ using Flask · Designed for learning & exploration</sub>
</div>
