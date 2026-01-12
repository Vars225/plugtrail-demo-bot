import streamlit as st
import google.generativeai as genai
import PIL.Image

# --- PAGE CONFIGURATION ---
# Mundu logo ni open cheyyali (make sure filename is correct)
try:
    logo_img = PIL.Image.open("logo.png") # Mee file name ikkada ivvandi
except:
    logo_img = "⚡" # Image lekapothe default emoji vastundi

st.set_page_config(
    page_title="PlugTrail AI",
    page_icon=logo_img, # Ikkada image variable pass chestunnam
    layout="centered"
)

# --- API SETUP (SECURE WAY) ---
# Ippudu key code lo undadu. Server settings nundi tiskuntundi.
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    st.error("API Key not found! Please set it in Streamlit Secrets.")
    st.stop()

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# --- UI HEADER ---
st.title(" PlugTrail Assistant")
st.caption("Ask your doubts regarding charging")

# --- SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- SIDEBAR (Controls) ---
with st.sidebar:
    st.header("⚙️ Controls")
    
    # Image Uploader
    st.subheader("📸 Vision")
    uploaded_file = st.file_uploader("Upload Error Photo", type=["jpg", "png", "jpeg"])

    # Clear Chat
    st.divider()
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# --- CHAT DISPLAY ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image" in message:
            st.image(message["image"], width=200)

# --- USER INPUT ---
user_input = st.chat_input("Ask about EV Charging, Payments, or Errors...")

# --- MAIN LOGIC ---
if user_input:
    # 1. User Message Display
    with st.chat_message("user"):
        st.markdown(user_input)
        if uploaded_file:
            image = PIL.Image.open(uploaded_file)
            st.image(image, width=200)
    
    # Save to history
    msg_data = {"role": "user", "content": user_input}
    if uploaded_file:
        msg_data["image"] = PIL.Image.open(uploaded_file)
    st.session_state.messages.append(msg_data)

    # 2. AI Processing
    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            try:
                # --- SYSTEM PROMPT (MEE COMPANY RULES) ---
                sys_prompt = """
                You are the AI Assistant for 'PlugTrail Power Pvt. Ltd.', an EV charging infrastructure startup based in Chhattisgarh, India. 
Your goal is to answer user queries about PlugTrail's services, chargers, and business partnership models using the following knowledge base:

1. COMPANY OVERVIEW:
- Name: PlugTrail Power Pvt. Ltd.
- Mission: Powering India's EV journey by building charging ecosystems, focusing on Tier-2 & Tier-3 cities.
- Tagline: "Power Your Journey" | "Universal | Reliable | Profitable".
- Website: www.plugtrail.in
- Contact: 02269711514 | plugtrailpowerpvtltd@gmail.com

2. OUR PRODUCT (SMART EV STATIONS):
- Compatibility: Hybrid chargers that support 2-Wheelers, 3-Wheelers (Auto/E-rickshaws), and 4-Wheelers (Cars) - All under one smart charger.
- Features: IP-rated weather-proof, Safe in rain, Smart app-based unlocking.
- Locations: Ideal for Highways, Cities, Restaurants, Hotels, and Commercial buildings.
- Usage Steps: 1. Park & Plug-in -> 2. Scan QR -> 3. Select Plan -> 4. Pay & Charge -> 5. Stop & Return.
- If you have your own charger there is a socket between the guns to plug and charge, It takes around 20minutes for 1unit charge
3. FOR EV OWNERS (CUSTOMERS):
- Benefits: Affordable public charging, Easy unlock via app, No vehicle discrimination (Universal charging), Reliable infrastructure.

4. FOR PARTNERS (BUSINESS MODEL):
- Target Partners: Restaurants, Dhabas, Hotels, Resorts, Commercial Buildings, Government spaces.
- Benefits for Partners: Increased customer footfall, Longer customer stay (higher billing), Additional revenue stream, Zero operational headache.
- Business Model: 
  - Revenue sharing model.
  - Transparent earnings via CMS software.
  - Low upfront investment (PlugTrail invests in the business).
  - Franchisee options available.

5. TONE & BEHAVIOR:
- Be professional, polite, and helpful.
- Keep answers concise.
- If asked about location, mention serving Chhattisgarh and expanding across India.

                
                INSTRUCTIONS:
                - Keep answers polite and short.
                - If the user sends a photo, analyze it for charger errors.
                - If the user speaks Hindi/Telugu, reply in that language.
                - If you dont know the answers accurately do not give the wrong answers, just give the 'Support Contact' number to get connected
                """
                
                full_prompt = sys_prompt + f"\nUser Question: {user_input}"
                
                # Gemini Call
                response = None
                if uploaded_file:
                    img = PIL.Image.open(uploaded_file)
                    response = model.generate_content([full_prompt, img])
                else:
                    response = model.generate_content(full_prompt)
                
                bot_reply = response.text
                
                # Display Text
                st.markdown(bot_reply)
                
                # Save to History
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": bot_reply
                })

            except Exception as e:

                st.error(f"Error: {e}")
