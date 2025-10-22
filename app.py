# app.py
import streamlit as st
import random
from datetime import date
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import textwrap

st.set_page_config(page_title="오늘의 한 마디", page_icon="🌤", layout="centered")

# ================== STYLE (카드 제거, 대형 타이포) ==================
st.markdown("""
<style>
/* 레이아웃 폭 */
.block-container{max-width:760px;padding-top:2.2rem;padding-bottom:2.2rem;}
/* 은은한 배경 (테마와 잘 섞임) */
body{
  background: radial-gradient(1200px 800px at 12% 8%, #f7fbff 0%, #f5f4ff 46%, #f8fafc 100%);
}
/* 타이틀 */
h1{letter-spacing:-0.4px;margin-bottom:.15rem;}
/* 버튼(테마 primaryColor 사용) */
.stButton > button{
  width:100%;height:56px;border:0;border-radius:14px;font-weight:800;font-size:1.05rem;
  box-shadow: 0 10px 28px rgba(79,166,229,.22); transition: transform .05s, box-shadow .2s;
}
.stButton > button:hover{ transform: translateY(-1px); box-shadow: 0 14px 34px rgba(79,166,229,.30); }
.stButton > button:active{ transform: translateY(0); box-shadow: 0 6px 18px rgba(79,166,229,.18); }
/* 대형 문장 – 카드 없이, 화면에 바로 출력 */
.quote{
  margin: 18px 0 8px 0;
  font-size: clamp(28px, 5.4vw, 44px);
  line-height: 1.28;
  font-weight: 800;
  color: #1f2937;
  text-align: center;
  animation: fadeIn .35s ease;
}
@keyframes fadeIn { from{opacity:0; transform:translateY(6px)} to{opacity:1; transform:none} }
.hint{ text-align:center; color:#76839b; font-size:.98rem; margin-top:.6rem;}
.footer{ text-align:center; color:#8a8fa0; font-size:.9rem; margin-top:20px;}
/* 아이콘형 보조 버튼들 */
.ctrl-btn{
  display:inline-flex; align-items:center; gap:.45rem;
  padding:.6rem .9rem; border-radius:12px; border:1px solid rgba(0,0,0,.06);
  background:#ffffffb3; backdrop-filter: blur(6px);
  cursor:pointer; font-weight:700; font-size:.95rem; color:#1f2937;
  transition: background .15s, transform .05s, box-shadow .2s;
  box-shadow: 0 8px 22px rgba(18,37,64,.08);
}
.ctrl-btn:hover{ background:#fff; transform: translateY(-1px); box-shadow: 0 12px 28px rgba(18,37,64,.12); }
.ctrl-wrap{ display:flex; gap:.6rem; justify-content:center; flex-wrap:wrap; margin-top:10px; }
.small{ font-size:.92rem; color:#667085; text-align:center; }
hr{margin:12px 0;}
</style>
""", unsafe_allow_html=True)

# ================== DATA ==================
CATEGORIES = {
    "힐링": [
        "작은 용기가 큰 변화를 만든다.","오늘은 스스로를 믿어보자.","길을 몰라도 걷다 보면 보인다.",
        "너무 멀리 보지 말고, 바로 앞을 보자.","오늘은 잠시 쉬어도 괜찮다.","내가 내 편이 되어주자.",
        "완벽하지 않아도 괜찮아.","비 오는 날도 결국은 그친다.","작은 선물 같은 하루가 될지도 모른다.",
        "오늘은 하늘 한번 올려다보기.","스스로에게 친절해지는 연습을 하자.","괜찮아, 잠깐 멈춰도 돼."
    ],
    "동기": [
        "한 걸음이라도 나아간다면 충분하다.","기적은 꾸준함의 또 다른 이름이다.",
        "어제보다 1%만 나아져도 그건 성장이다.","오늘은 어제의 나를 이길 기회다.",
        "작은 시도라도 오늘 해보자.","끝이 아니라 새로운 시작이다.",
        "당신의 노력은 반드시 빛을 볼 거야.","할 수 없을 것 같을 때, 진짜 시작이다.",
        "때로는 결과보다 과정이 중요하다.","오늘 하루를 기록해보자."
    ],
    "유머": [
        "기대하지 않아도 좋은 일이 찾아온다(배달도 가끔 빨리 옴).",
        "아무 일도 안 하는 것도 때론 용기(소파가 붙잡아서 그래).",
        "하루를 웃음으로 시작해보자(아니면 밈이라도).",
        "오늘은 ‘괜찮다’를 말하고 간식 하나를 더 먹자.",
        "행운은 생각보다 가까이(바지 주머니? 아니면 냉장고?)."
    ],
}
# 전 카테고리 합치기
ALL_QUOTES = []
INDEX = []  # (category, local_idx) 추적
for cat, items in CATEGORIES.items():
    for i, q in enumerate(items):
        INDEX.append((cat, i))
        ALL_QUOTES.append(q)

# ================== STATE ==================
ss = st.session_state
if "mode_daily" not in ss: ss.mode_daily = False     # 일일 고정 모드
if "category" not in ss: ss.category = ["힐링","동기","유머"]
if "deck" not in ss: ss.deck = []
if "last_i" not in ss: ss.last_i = None
if "favs" not in ss: ss.favs = set()                 # 즐겨찾기 인덱스 보관

def build_deck():
    """선택된 카테고리의 인덱스만 모아 섞기"""
    pool = [k for k,(cat,_) in enumerate(INDEX) if cat in ss.category]
    random.shuffle(pool)
    ss.deck = pool

def daily_pick():
    """날짜+카테고리 조합으로 고정 문장 뽑기"""
    pool = [k for k,(cat,_) in enumerate(INDEX) if cat in ss.category]
    if not pool:
        return None
    seed = hash(date.today().isoformat() + "|" + ",".join(sorted(set(ss.category))))
    rng = random.Random(seed)
    return rng.choice(pool)

def draw_one():
    """한 문장 뽑기(랜덤 모드: 중복 없이), 일일 모드: 고정"""
    if ss.mode_daily:
        ss.last_i = daily_pick()
    else:
        if not ss.deck:
            build_deck()
        ss.last_i = ss.deck.pop()

# 초기 덱 준비
if not ss.deck and not ss.mode_daily:
    build_deck()

# ================== HEADER ==================
st.title("🌤 오늘의 한 마디")
st.caption("매일 하나, 나에게 건네는 짧은 문장")

# ================== CONTROLS ==================
# 메인 버튼
if st.button("✨ 한 문장 뽑기", type="primary", use_container_width=True):
    draw_one()

# 키보드(스페이스바)로도 뽑기
st.markdown("""
<script>
document.addEventListener('keydown', (e)=>{
  if(e.code === 'Space' && !e.repeat){
    const btn = window.parent.document.querySelector('button[kind="primary"]');
    if(btn){ btn.click(); }
    e.preventDefault();
  }
});
</script>
""", unsafe_allow_html=True)

# 옵션(디자인을 해치지 않도록 숨김)
with st.expander("옵션"):
    c1, c2 = st.columns([1,1])
    with c1:
        ss.mode_daily = st.toggle("일일 고정 모드(오늘 하루 같은 문장)", value=ss.mode_daily)
    with c2:
        ss.category = st.multiselect("카테고리 선택", ["힐링","동기","유머"], default=ss.category)
    st.caption("• 랜덤 모드: 중복 없이 한 바퀴 다 볼 때까지 뽑기\n\n• 일일 고정: 오늘은 같은 문장, 내일 자동 변경")
    # 카테고리 바꾸면 덱 재생성
    if st.button("카테고리 반영하여 섞기"):
        build_deck()

# ================== QUOTE OUTPUT ==================
if ss.last_i is not None:
    quote = ALL_QUOTES[ss.last_i]
    st.markdown(f"<div class='quote'>“{quote}”</div>", unsafe_allow_html=True)
else:
    st.markdown("<p class='hint'>버튼을 눌러 첫 문장을 뽑아보세요. (스페이스바도 가능)</p>", unsafe_allow_html=True)

# ================== ACTIONS: 공유 · 복사 · PNG · 즐겨찾기 ==================
def to_png_bytes(text: str, w=1200, h=628):  # 1.91:1 SNS 카드
    bg = Image.new("RGB", (w, h), (247, 250, 255))
    draw = ImageDraw.Draw(bg)
    # 폰트 (기본 내장 폰트 사용; 서버에 폰트 없을 수 있음)
    font = ImageFont.load_default()
    # 텍스트 래핑
    wrapped = "\n".join(textwrap.wrap(text, width=22))
    # 위치 중앙 정렬
    tw, th = draw.multiline_textbbox((0,0), f"“{wrapped}”", font=font, spacing=8)[2:]
    x = (w - tw)//2
    y = (h - th)//2
    draw.text((x, y), f"“{wrapped}”", fill=(31,41,55), font=font, spacing=8)
    # 워터마크
    draw.text((w-240, h-40), "© 오늘의 한 마디", fill=(100,110,130), font=font)
    buf = BytesIO(); bg.save(buf, format="PNG"); buf.seek(0)
    return buf

def page_url_with_index(i: int) -> str:
    base = st.get_option("server.baseUrlPath") or ""
    # Streamlit Cloud/로컬 모두 동작: 현재 주소 추정
    # JS 복사 버튼에서 window.location.origin 사용하므로 여기선 쿼리만 반환
    return f"?i={i}"

# 퍼머링크 쿼리 처리: ?i=123 로 접속 시 해당 문장 표시
qp = st.query_params
if "i" in qp:
    try:
        idx = int(qp["i"])
        if 0 <= idx < len(ALL_QUOTES):
            ss.last_i = idx
    except Exception:
        pass

# 액션 버튼 모음
if ss.last_i is not None:
    col = st.container()
    with col:
        # 즐겨찾기 상태
        fav_state = ("⭐ 즐겨찾기 해제", "⭐ 즐겨찾기")[ss.last_i not in ss.favs]

        st.markdown("""
<div class="ctrl-wrap">
  <button class="ctrl-btn" id="copyBtn">📋 복사</button>
  <button class="ctrl-btn" id="shareLinkBtn">🔗 링크 복사</button>
  <button class="ctrl-btn" id="dlBtn">🖼 PNG 다운로드</button>
  <button class="ctrl-btn" id="favBtn">⭐ 즐겨찾기</button>
</div>
<script>
const copyBtn = document.getElementById('copyBtn');
const shareLinkBtn = document.getElementById('shareLinkBtn');
const dlBtn = document.getElementById('dlBtn');
const favBtn = document.getElementById('favBtn');
</script>
""", unsafe_allow_html=True)

        # 1) 클립보드 복사
        st.markdown(f"""
<script>
if(copyBtn) {{
  copyBtn.onclick = async () => {{
    try {{
      await navigator.clipboard.writeText("“{quote}”");
      copyBtn.innerText = "✅ 복사됨";
      setTimeout(() => copyBtn.innerText = "📋 복사", 1200);
    }} catch(e) {{ console.log(e); }}
  }}
}}
</script>
""", unsafe_allow_html=True)

        # 2) 링크 복사 (현재 페이지 + ?i=idx)
        st.markdown(f"""
<script>
if(shareLinkBtn){{
  shareLinkBtn.onclick = async () => {{
    const url = window.location.origin + window.location.pathname + "{page_url_with_index(ss.last_i)}";
    try {{
      await navigator.clipboard.writeText(url);
      shareLinkBtn.innerText = "✅ 링크 복사됨";
      setTimeout(() => shareLinkBtn.innerText = "🔗 링크 복사", 1200);
    }} catch(e){{ console.log(e); }}
  }}
}}
</script>
""", unsafe_allow_html=True)

        # 3) PNG 다운로드
        png_buf = to_png_bytes(quote)
        st.download_button("🖼 PNG 다운로드", data=png_buf, file_name="one_line.png", mime="image/png", key="dl_png", use_container_width=False)

        # 4) 즐겨찾기 토글
        fav_clicked = st.button(fav_state, key="fav_btn_internal", help="현재 문장을 즐겨찾기에 저장/해제")
        if fav_clicked:
            if ss.last_i in ss.favs: ss.favs.remove(ss.last_i)
            else: ss.favs.add(ss.last_i)

# 즐겨찾기 리스트(선택)
if ss.favs:
    with st.expander(f"⭐ 즐겨찾기 ({len(ss.favs)})"):
        for i in sorted(ss.favs):
            st.write(f"• {ALL_QUOTES[i]}")

st.markdown("<div class='footer'>© 오늘의 한 마디</div>", unsafe_allow_html=True)
