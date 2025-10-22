import streamlit as st
import random

st.set_page_config(page_title="오늘의 한 마디", page_icon="🌤", layout="centered")

# -------------------- STYLE --------------------
st.markdown("""
<style>
.block-container{max-width:760px;padding-top:2.2rem;padding-bottom:2.2rem;}
body{
  background: radial-gradient(1200px 800px at 12% 8%, #f7fbff 0%, #f5f4ff 46%, #f8fafc 100%);
}
h1{letter-spacing:-0.4px;margin-bottom:.15rem;}
.stButton > button{
  width:100%;height:56px;border:0;border-radius:14px;font-weight:800;font-size:1.05rem;
  box-shadow: 0 10px 28px rgba(79,166,229,.22); transition: transform .05s, box-shadow .2s;
}
.stButton > button:hover{ transform: translateY(-1px); box-shadow: 0 14px 34px rgba(79,166,229,.30); }
.stButton > button:active{ transform: translateY(0); box-shadow: 0 6px 18px rgba(79,166,229,.18); }

/* 애니메이션 키프레임 */
@keyframes fadeUp {
  0% { opacity: 0; transform: translateY(10px); filter: blur(6px); }
  100% { opacity: 1; transform: translateY(0); filter: blur(0); }
}
@keyframes gradientShift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

/* 문장 타이포(애니메이션은 JS로 매번 재적용) */
.quote {
  margin: 18px 0 8px 0;
  font-size: clamp(28px, 5.4vw, 44px);
  line-height: 1.28;
  font-weight: 800;
  text-align: center;
  background: linear-gradient(90deg, #4fa6e5, #a47ee8, #ff9fc2);
  background-size: 200% 200%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.hint{ text-align:center; color:#76839b; font-size:.98rem; margin-top:.6rem;}
.footer{ text-align:center; color:#8a8fa0; font-size:.9rem; margin-top:20px;}

/* 키보드 포커스용 숨김 앵커 */
#kb-focus-anchor{position:absolute;left:-9999px;top:-9999px;outline:none;}
</style>
""", unsafe_allow_html=True)

# -------------------- DATA --------------------
QUOTES = [
    "작은 용기가 큰 변화를 만든다.","오늘은 스스로를 믿어보자.","길을 몰라도 걷다 보면 보인다.",
    "너무 멀리 보지 말고, 바로 앞을 보자.","한 걸음이라도 나아간다면 충분하다.","누군가의 말보다 내 속삭임에 귀 기울이자.",
    "기적은 어쩌면 꾸준함의 또 다른 이름일지도.","햇살이 조금 따뜻한 날엔 마음도 풀어지기 마련이다.",
    "오늘은 잠시 쉬어도 괜찮다.","내가 내 편이 되어주자.","완벽하지 않아도 괜찮아.",
    "어제보다 1%만 나아져도 그건 성장이다.","스스로에게 친절해지는 연습을 하자.","작은 웃음이 하루를 바꾼다.",
    "오늘의 실패는 내일의 밑그림이다.","할 수 없을 것 같을 때, 진짜 시작이다.","행복은 멀리 있지 않다. 지금 눈앞에도 있다.",
    "천천히, 그러나 멈추지 말자.","가장 단순한 것이 가장 강하다.","한 번의 친절이 세상을 조금 따뜻하게 만든다.",
    "불안함은 새로운 시작의 신호다.","무언가를 포기하기엔 아직 너무 이르다.",
    "오늘은 어제보다 조금 더 나은 내가 되자.","행운은 생각보다 가까이에 있다.","오늘은 웃는 연습을 해보자.",
    "당신은 이미 충분히 잘하고 있다.","때로는 결과보다 과정이 중요하다.","지금 이 순간을 느껴보자.",
    "괜찮아, 잠깐 멈춰도 돼.","작은 성취를 축하해보자.","오늘은 감사할 일을 하나만 찾아보자.",
    "나에게 필요한 건 완벽이 아니라 꾸준함이다.","비 오는 날도 결국은 그친다.","누군가의 하루를 밝히는 빛이 되어보자.",
    "오늘은 어제의 나를 이길 기회다.","실패는 나쁜 게 아니라 과정일 뿐이다.","작은 시도라도 오늘 해보자.",
    "세상은 생각보다 너그럽다.","아무 일도 하지 않는 것도 때로는 용기다.","하루를 웃음으로 시작해보자.",
    "기대하지 않아도 좋은 일이 찾아온다.","오늘은 하늘 한번 올려다보기.","끝이 아니라 새로운 시작이다.",
    "오늘 하루를 기록해보자.","작은 선물 같은 하루가 될지도 모른다.",
    "당신의 노력은 반드시 빛을 볼 거야.","힘내지 않아도 괜찮아, 그래도 해낼 거야.","오늘은 ‘괜찮다’는 말을 스스로에게 해주자."
]

# -------------------- STATE --------------------
if "deck" not in st.session_state:
    st.session_state.deck = list(range(len(QUOTES)))
    random.shuffle(st.session_state.deck)
if "idx" not in st.session_state:
    st.session_state.idx = None
if "render_count" not in st.session_state:
    st.session_state.render_count = 0  # 렌더 번호(스크립트가 매번 다시 붙도록)

# -------------------- UI --------------------
st.title("🌤 오늘의 한 마디")
st.caption("매일 하나, 나에게 건네는 짧은 문장")

# 메인 버튼
if st.button("✨ 한 문장 뽑기", type="primary", use_container_width=True):
    if not st.session_state.deck:
        st.session_state.deck = list(range(len(QUOTES)))
        random.shuffle(st.session_state.deck)
    st.session_state.idx = st.session_state.deck.pop()

# 문장 출력
if st.session_state.idx is not None:
    q = QUOTES[st.session_state.idx]
    # 고유 id로 렌더
    st.session_state.render_count += 1
    q_id = f"quote-{st.session_state.render_count}"
    st.markdown(f"<div id='{q_id}' class='quote'>“{q}”</div>", unsafe_allow_html=True)
else:
    st.markdown("<p class='hint'>버튼을 누르거나 스페이스바를 눌러 첫 문장을 뽑아보세요.</p>", unsafe_allow_html=True)

# 키 이벤트 & 애니메이션 재적용 스크립트
st.markdown(f"""
<div id="kb-focus-anchor" tabindex="0"></div>
<script>
(function(){{
  // 1) 처음 로드/매 렌더마다 포커스 확보: iframe 내부로 키 입력 유도
  const anchor = document.getElementById('kb-focus-anchor');
  if (anchor) {{
    anchor.focus();
    // 포커스가 외부로 나갔을 경우를 대비, 클릭 시에도 다시 포커스 시도
    document.addEventListener('click', ()=>anchor.focus(), {{once:false}});
  }}

  // 2) 스페이스바로 항상 동작 (버튼 포커스와 무관)
  function clickDraw(){{
    const btns = Array.from(document.querySelectorAll('button'));
    const target = btns.find(b => (b.innerText||"").includes("한 문장 뽑기"));
    if (target) target.click();
  }}
  window.onkeydown = function(e){{
    if(e.code === 'Space' && !e.repeat){{ e.preventDefault(); clickDraw(); }}
  }};

  // 3) 애니메이션 매번 재실행: 새로 렌더된 quote 엘리먼트 id로 타깃팅
  const q = document.getElementById("{q_id if st.session_state.idx is not None else ''}");
  if (q) {{
    // gradient는 계속, fadeUp만 재시작: animation 재적용 트릭
    q.style.animation = 'none';
    // 강제 reflow
    void q.offsetWidth;
    // 재적용
    q.style.animation = 'fadeUp 0.7s ease forwards, gradientShift 6s ease infinite';
  }}
}})();
</script>
""", unsafe_allow_html=True)

st.markdown("<div class='footer'>© 오늘의 한 마디</div>", unsafe_allow_html=True)

