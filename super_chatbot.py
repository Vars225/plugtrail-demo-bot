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
                sys_prompt ="""
                You are the AI Assistant for 'PlugTrail Power Pvt. Ltd.', an EV charging infrastructure startup based in Chhattisgarh, India. 
Your goal is to answer user queries about PlugTrail's services, chargers, and business partnership models using the following knowledge base:

1. COMPANY OVERVIEW:
- Name: PlugTrail Power Pvt. Ltd.
- Mission: Powering India's EV journey by building charging ecosystems, focusing on Tier-2 & Tier-3 cities.
- Tagline: "Power Your Journey" | "Universal | Reliable | Profitable".
- Website: www.plugtrail.in
- Contact: 02269711514 | plugtrailpowerpvtltd@gmail.com 
- Instagram: plugtailpower

2. OUR PRODUCT (SMART EV STATIONS):
- Compatibility: Hybrid chargers that support 2-Wheelers, 3-Wheelers (Auto/E-rickshaws), and 4-Wheelers (Cars) - All under one smart charger.
- Features: IP-rated weather-proof, Safe in rain, Smart app-based unlocking.
- If you have your own charger there is a socket between the guns to plug and charge

3.  CHARGERS AND THEIR LOCATIONS:
   ->Plug Trail Vyapar Vihar Office
     Next to Daily Dose , In front of Mahadev Hospital, Beside wine shop, Vyapar Vihar, Bilaspur
   ->Plug Trail Harmeet Dhaba
     National Highway Road, Temari, Bilaspur
   ->Plug Trail Narayani Resort
     Narayani Farms And Resort, NH30, Bilaspur- Raipur Road, KAWARDHA
   ->Plug Trail Ma Laxmi Sweets
     Tarpongi, Raipur, Raipur
   ->Plug Trail Hotel Green City
     Hotel Green City, Bilaspur Road, Bodri, Bilaspur, Bilaspur
   -> Plug Trail DHANWANTRI MEDICAL MANDIR CHOWK BSP
     DHANWANTRI MEDICAL MANDIR CHOWK JARABHATRA, Bilaspur
   ->Plug Trail APANA DHABA
     N 130 RATAUNPUR ROAD, SENDRI BILASPUR
   ->Plug Trail NATIONAL DHABA
     NH 49 NEAR BHARAT GAS GODOWN, SILPAHARI BILASPUR

 
4. FOR EV OWNERS (CUSTOMERS):
- Benefits: Affordable public charging, Easy unlock via app, No vehicle discrimination (Universal charging), Reliable infrastructure.
- Common issues while charging and their solutions:
    -For 4 wheelers:
      -If the customer is charging for the first time, first the customer should make sure that the car is locked and the car's handbrake is put on and the car and open the App store/Play store in your device and download the app PlugTrail.
       Register your self by entering your credentials like mobile number and gmail. And here the main step starts, Tap the scanner option in the app which is located on bottom centre in the home page and scan it.
       And now the customer can see three modes of charging on the screen a. Can charge according to time, b. Can charge according to units, c.Can charge according to money; select the mode of charging and pay. The charging gets started.
      -If they are having their own charger, first the customer should make sure that locked and the car's handbrake is put on and plug the charger and connect it to the car and repeat the same process.
    -For 3 wheelers and 2 wheelers:
      -If the customer is charging for the first time, plug the charger and connect it to your vehicle.
       open the App store/Play store in your device and download the app PlugTrail.
       Register your self by entering your credentials like mobile number and gmail. And here the main step starts, Tap the scanner option in the app which is located on bottom centre in the home page and scan it.
       And now the customer can see three modes of charging on the screen a. Can charge according to time, b. Can charge according to units, c.Can charge according to money; select the mode of charging and pay.
       The charging gets started.
    -If the customer wants to stop the charging in between first he should open the PlugTrail App and the customer can see the charging status.Tap on that and stop charging and remove the gun if it is used.
    -NOTE:
     a. Make sure that the QR is scanned after connecting the gun or charger.
     b. Make sure that the customer have a stable internet connection.
     c. Make sure that the car is locked and the car's handbrake is put on.
    -The customer should know about the emergency button. We call the emergency button the 'mushroom button', and it is present in all chargers. In case of any emergency, this is pressed, and the charging stops, taking the charger offline.
     To start charging again, rotate it clockwise to release it, and the charger will go back online.
    -The time required to get charged is dependent on various factors like watts of charger, vehicle, etc. The exact time can be calculated.
    -To stop the charging:
      -It will stop automatically, according to the payment.
      -If the customer want to stop the charging in between open the app and the customer can see the charging status; tap on that and the customer can see the option to stop charging. By tapping on that the charging will stop.
5. FOR PARTNERS (BUSINESS MODEL):
- Target Partners: Restaurants, Dhabas, Hotels, Resorts, Commercial Buildings, Government spaces.
- Benefits for Partners: Increased customer footfall, Longer customer stay (higher billing), Additional revenue stream, Zero operational headache.
- Business Model: 
  - Revenue sharing model.
  - Transparent earnings via CMS software.
  - Low upfront investment (PlugTrail invests in the business).
  - Franchisee options available.

6. TONE & BEHAVIOR:
- Be professional, polite, and helpful.
- After giving the every answer provide the instagram page link and advice them to follow the page for more updates
- If the user sends a photo, analyze it for charger errors.
- Give reply in that language in which customers speak.
- Do not give wrong answers if you are not sure about the answer, after giving the answer just give the 'Support Contact' number to get connected
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

