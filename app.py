# main.py
import streamlit as st
import random

st.set_page_config(page_title="오늘의 한 마디", page_icon="🌤", layout="centered")

# --------- 스타일 ---------
st.markdown("""
<style>
.quote {
  font-size: 1.9rem;
  font-weight: 600;
  text-align: center;
  color: #333;
  margin: 1.6rem 0 .8rem 0;
}
.subtle {
  text-align:center;
  color:#777;
  font-size:.9rem;
}
.card {
  background: #ffffffcc;
  border-radius: 18px;
  padding: 1.2rem 1.2rem;
  box-shadow: 0 6px 24px rgba(0,0,0,.06);
}
</style>
""", unsafe_allow_html=True)

# --------- 문장 데이터 ---------
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

# --------- 세션 상태 ---------
if "deck" not in st.session_state:
    st.session_state.deck = list(range(len(QUOTES)))
    random.shuffle(st.session_state.deck)
if "last_idx" not in st.session_state:
    st.session_state.last_idx = None

# --------- UI ---------
st.title("🌤 오늘의 한 마디")
st.caption("버튼을 누를 때마다 한 문장을 뽑아요. 모두 보면 알아서 다시 섞입니다.")

# 뽑기 버튼(유일한 인터랙션)
if st.button("✨ 한 문장 뽑기", type="primary", use_container_width=True):
    if not st.session_state.deck:
        st.session_state.deck = list(range(len(QUOTES)))
        random.shuffle(st.session_state.deck)
    st.session_state.last_idx = st.session_state.deck.pop()

st.markdown(" ")
st.markdown('<div class="card">', unsafe_allow_html=True)

if st.session_state.last_idx is not None:
    quote = QUOTES[st.session_state.last_idx]
    st.markdown(f"<div class='quote'>“{quote}”</div>", unsafe_allow_html=True)
else:
    st.markdown("<div class='quote' style='opacity:.6;'>버튼을 눌러 첫 문장을 뽑아보세요.</div>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown("<div class='subtle'>© 오늘의 한 마디</div>", unsafe_allow_html=True)
