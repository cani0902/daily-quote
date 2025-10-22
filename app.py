# main.py
import streamlit as st
import random

st.set_page_config(page_title="오늘의 한 문장 뽑기", page_icon="🌤", layout="centered")

# ------- 스타일(선택) -------
st.markdown("""
<style>
.quote {
  font-size: 1.9rem;
  font-weight: 600;
  text-align: center;
  color: #333;
  margin: 1.5rem 0 0.5rem 0;
}
.subtle {
  text-align:center;
  color:#777;
  font-size:.9rem;
}
.card {
  background: #ffffffaa;
  border-radius: 18px;
  padding: 1.2rem 1.2rem;
  box-shadow: 0 6px 24px rgba(0,0,0,.06);
}
</style>
""", unsafe_allow_html=True)

# ------- 문장 데이터 -------
QUOTES = [
    "작은 용기가 큰 변화를 만든다.",
    "오늘은 스스로를 믿어보자.",
    "길을 몰라도 걷다 보면 보인다.",
    "너무 멀리 보지 말고, 바로 앞을 보자.",
    "한 걸음이라도 나아간다면 충분하다.",
    "누군가의 말보다 내 속삭임에 귀 기울이자.",
    "기적은 어쩌면 꾸준함의 또 다른 이름일지도.",
    "햇살이 조금 따뜻한 날엔 마음도 풀어지기 마련이다.",
    "오늘은 잠시 쉬어도 괜찮다.",
    "내가 걷는 속도가 곧 나의 리듬이다.",
    "어제보다 1%만 나아져도 그건 성장이다.",
    "스스로에게 친절해지는 연습을 하자.",
    "작은 웃음이 하루를 바꾼다.",
    "오늘의 실패는 내일의 밑그림이다.",
    "할 수 없을 것 같을 때, 진짜 시작이다.",
    "행복은 멀리 있지 않다. 지금 눈앞에도 있다.",
    "천천히, 그러나 멈추지 말자.",
    "가장 단순한 것이 가장 강하다.",
    "한 번의 친절이 세상을 조금 따뜻하게 만든다.",
    "불안함은 새로운 시작의 신호다.",
    "무언가를 포기하기엔 아직 너무 이르다.",
    "오늘은 어제보다 조금 더 나은 내가 되자.",
    "행운은 생각보다 가까이에 있다.",
    "오늘은 웃는 연습을 해보자.",
    "당신은 이미 충분히 잘하고 있다.",
    "때로는 결과보다 과정이 중요하다.",
    "지금 이 순간을 느껴보자.",
    "괜찮아, 잠깐 멈춰도 돼.",
    "작은 성취를 축하해보자.",
    "오늘은 감사할 일을 하나만 찾아보자.",
    "나에게 필요한 건 완벽이 아니라 꾸준함이다.",
    "비 오는 날도 결국은 그친다.",
    "누군가의 하루를 밝히는 빛이 되어보자.",
    "오늘은 어제의 나를 이길 기회다.",
    "실패는 나쁜 게 아니라 과정일 뿐이다.",
    "작은 시도라도 오늘 해보자.",
    "세상은 생각보다 너그럽다.",
    "아무 일도 하지 않는 것도 때로는 용기다.",
    "하루를 웃음으로 시작해보자.",
    "기대하지 않아도 좋은 일이 찾아온다.",
    "오늘은 하늘 한번 올려다보기.",
    "완벽하지 않아도 괜찮아.",
    "내가 내 편이 되어주자.",
    "조급해하지 말고, 지금을 즐기자.",
    "어제의 걱정은 오늘의 걸음이 되었다.",
    "끝이 아니라 새로운 시작이다.",
    "오늘 하루를 기록해보자.",
    "작은 선물 같은 하루가 될지도 모른다.",
    "당신의 노력은 반드시 빛을 볼 거야.",
    "힘내지 않아도 괜찮아, 그래도 해낼 거야.",
    "오늘은 ‘괜찮다’는 말을 스스로에게 해주자."
]

# ------- 세션 스테이트 초기화 -------
if "deck" not in st.session_state:
    # deck: 아직 뽑지 않은 문장들의 인덱스
    st.session_state.deck = list(range(len(QUOTES)))
    random.shuffle(st.session_state.deck)
if "history" not in st.session_state:
    st.session_state.history = []   # 이미 뽑은 인덱스
if "last_quote_idx" not in st.session_state:
    st.session_state.last_quote_idx = None
if "seed" not in st.session_state:
    st.session_state.seed = None

# ------- 헤더 -------
st.title("🌤 오늘의 한 문장 — 뽑기")
st.caption("버튼을 누를 때마다 새로운 문장을 뽑아요. 한 바퀴 다 보면 자동으로 다시 섞입니다.")

# 재현 가능하게 하고 싶다면 시드 입력(선택)
with st.expander("옵션: 셔플 시드 고정하기 (선택)"):
    seed_input = st.text_input("시드(아무 문자열 가능):", value=st.session_state.seed or "")
    col_opt1, col_opt2 = st.columns([1,1])
    with col_opt1:
        if st.button("현재 덱 재셔플", use_container_width=True):
            rnd = random.Random(seed_input) if seed_input else random
            st.session_state.seed = seed_input or None
            st.session_state.deck = list(range(len(QUOTES)))
            rnd.shuffle(st.session_state.deck)
            st.session_state.history = []
            st.session_state.last_quote_idx = None
    with col_opt2:
        if st.button("초기화(완전 리셋)", use_container_width=True):
            st.session_state.clear()
            st.rerun()

# ------- 본문: 뽑기 버튼 -------
col1, col2, col3 = st.columns([1.2,1,1])
with col1:
    draw = st.button("✨ 한 문장 뽑기", type="primary", use_container_width=True)
with col2:
    reshuffle = st.button("🔄 다시 섞기", use_container_width=True)
with col3:
    show_history = st.toggle("히스토리 보기", value=False)

if reshuffle:
    rnd = random.Random(st.session_state.seed) if st.session_state.seed else random
    st.session_state.deck = list(range(len(QUOTES)))
    rnd.shuffle(st.session_state.deck)
    st.session_state.history = []
    st.session_state.last_quote_idx = None

if draw:
    if not st.session_state.deck:
        # 모두 소진했으면 자동으로 새로 섞기
        rnd = random.Random(st.session_state.seed) if st.session_state.seed else random
        st.session_state.deck = list(range(len(QUOTES)))
        rnd.shuffle(st.session_state.deck)
        st.session_state.history = []
    idx = st.session_state.deck.pop()  # 덱의 마지막에서 하나 뽑기
    st.session_state.history.append(idx)
    st.session_state.last_quote_idx = idx

# ------- 출력 영역 -------
st.markdown(" ")
st.markdown('<div class="card">', unsafe_allow_html=True)

if st.session_state.last_quote_idx is not None:
    q = QUOTES[st.session_state.last_quote_idx]
    st.markdown(f"<div class='quote'>“{q}”</div>", unsafe_allow_html=True)
else:
    st.markdown("<div class='quote' style='opacity:.6;'>버튼을 눌러 첫 문장을 뽑아보세요.</div>", unsafe_allow_html=True)

remain = len(st.session_state.deck)
total = len(QUOTES)
st.markdown(f"<div class='subtle'>남은 문장: <b>{remain}</b> / 전체 {total}</div>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ------- 히스토리(선택) -------
if show_history and st.session_state.history:
    st.write("#### 지금까지 뽑은 문장")
    for i, idx in enumerate(reversed(st.session_state.history), 1):
        st.write(f"{i}. {QUOTES[idx]}")
