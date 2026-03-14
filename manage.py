from flask import Flask, render_template, request, redirect, url_for, flash
import requests
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__, static_folder='public', static_url_path='/public')
app.secret_key = 'dev-secret-key'

BASE = 'https://jsonplaceholder.typicode.com'

# ── Helpers ───────────────────────────────────────────────────────────────────

def fetch_json(url):
    try:
        r = requests.get(url, timeout=6)
        return r.json() if r.ok else []
    except Exception:
        return []

def paginate(data, page, per_page=10):
    total = len(data)
    total_pages = max(1, (total + per_page - 1) // per_page)
    page = max(1, min(page, total_pages))
    start = (page - 1) * per_page
    visible = sorted(set(
        [1, total_pages] +
        list(range(max(1, page - 2), min(total_pages, page + 2) + 1))
    ))
    return {
        'items': data[start:start + per_page],
        'page': page,
        'total': total,
        'total_pages': total_pages,
        'visible_pages': visible,
        'last_record': min(page * per_page, total),
    }

# ── Home (with live stats) ────────────────────────────────────────────────────

@app.route('/')
def index():
    with ThreadPoolExecutor(max_workers=4) as ex:
        f_posts    = ex.submit(fetch_json, f'{BASE}/posts')
        f_users    = ex.submit(fetch_json, f'{BASE}/users')
        f_comments = ex.submit(fetch_json, f'{BASE}/comments')
        f_albums   = ex.submit(fetch_json, f'{BASE}/albums')

    stats = {
        'posts':    len(f_posts.result()),
        'users':    len(f_users.result()),
        'comments': len(f_comments.result()),
        'albums':   len(f_albums.result()),
    }
    return render_template('index.html', ap='home', stats=stats)

# ── GET: Fetch all posts (paginated) ──────────────────────────────────────────

@app.route('/api/FetchData')
def api_data():
    data = fetch_json(f'{BASE}/posts')
    p    = paginate(data, int(request.args.get('page', 1)))
    return render_template('getData.html', ap='fetch',
                           posts=p['items'], page=p['page'],
                           total_pages=p['total_pages'], total=p['total'],
                           visible_pages=p['visible_pages'], last_record=p['last_record'])

# ── GET: Post detail + comments ───────────────────────────────────────────────

@app.route('/api/PostDetail/<int:post_id>')
def post_detail(post_id):
    with ThreadPoolExecutor(max_workers=2) as ex:
        f_post     = ex.submit(fetch_json, f'{BASE}/posts/{post_id}')
        f_comments = ex.submit(fetch_json, f'{BASE}/posts/{post_id}/comments')
    post     = f_post.result()
    comments = f_comments.result()
    if not post or isinstance(post, list):
        flash(f'❌ Post #{post_id} not found.', 'error')
        return redirect(url_for('api_data'))
    return render_template('postDetail.html', ap='fetch',
                           post=post, comments=comments)

# ── GET: Posts by user ────────────────────────────────────────────────────────

@app.route('/api/UserPosts')
def user_posts():
    user_id = request.args.get('userId', type=int)
    posts   = fetch_json(f'{BASE}/posts?userId={user_id}') if user_id else []
    return render_template('userPosts.html', ap='userposts',
                           posts=posts, selected_user=user_id)

# ── POST: Create ──────────────────────────────────────────────────────────────

@app.route('/api/CreateData', methods=['GET', 'POST'])
def create_data():
    if request.method == 'POST':
        payload  = {'title': request.form['title'],
                    'body':  request.form['body'],
                    'userId': int(request.form['userId'])}
        resp = requests.post(f'{BASE}/posts', json=payload)
        if resp.status_code == 201:
            c = resp.json()
            flash(f'✅ Post created! ID: {c.get("id")} — "{c.get("title","")[:45]}"', 'success')
            return redirect(url_for('api_data'))
        flash(f'❌ Create failed — API returned {resp.status_code}.', 'error')
        return redirect(url_for('create_data'))
    return render_template('createData.html', ap='create')

# ── PUT / PATCH: Update ───────────────────────────────────────────────────────

@app.route('/api/UpdateData', methods=['GET', 'POST'])
def update_data():
    post = None
    if request.method == 'GET' and request.args.get('id'):
        pid  = request.args.get('id')
        resp = requests.get(f'{BASE}/posts/{pid}')
        post = resp.json() if resp.ok else None
        if not post:
            flash(f'❌ Post #{pid} not found.', 'error')
    elif request.method == 'POST':
        pid    = request.form['post_id']
        method = request.form.get('method', 'PUT').upper()
        title  = request.form.get('title', '').strip()
        body   = request.form.get('body', '').strip()
        userId = request.form.get('userId', '').strip()
        if method == 'PUT':
            payload = {'title': title, 'body': body, 'userId': int(userId) if userId else 1}
            resp = requests.put(f'{BASE}/posts/{pid}', json=payload)
        else:
            payload = {}
            if title:  payload['title']  = title
            if body:   payload['body']   = body
            if userId: payload['userId'] = int(userId)
            resp = requests.patch(f'{BASE}/posts/{pid}', json=payload)
        if resp.ok:
            u = resp.json()
            flash(f'✅ Post #{pid} updated via {method} — "{u.get("title","")[:45]}"', 'success')
            return redirect(url_for('api_data'))
        flash(f'❌ {method} failed — {resp.status_code}.', 'error')
        return redirect(url_for('update_data'))
    return render_template('updateData.html', ap='update', post=post)

# ── DELETE ────────────────────────────────────────────────────────────────────

@app.route('/api/DeleteData', methods=['GET', 'POST'])
def delete_data():
    post = None
    if request.method == 'GET' and request.args.get('id'):
        pid  = request.args.get('id')
        resp = requests.get(f'{BASE}/posts/{pid}')
        post = resp.json() if resp.ok else None
        if not post:
            flash(f'❌ Post #{pid} not found.', 'error')
    elif request.method == 'POST':
        pid  = request.form['post_id']
        resp = requests.delete(f'{BASE}/posts/{pid}')
        if resp.ok:
            flash(f'✅ Post #{pid} deleted successfully.', 'success')
            return redirect(url_for('api_data'))
        flash(f'❌ Delete failed — {resp.status_code}.', 'error')
        return redirect(url_for('delete_data'))
    return render_template('deleteData.html', ap='delete', post=post)

if __name__ == '__main__':
    app.run(debug=True)
