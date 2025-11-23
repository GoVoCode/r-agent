import streamlit as st
from frontend.services import api_client
from frontend.core import get_frontend_logger, get_frontend_settings

logger = get_frontend_logger("app")
settings = get_frontend_settings()

st.set_page_config(
    page_title="Restaurant Chat Agent",
    page_icon="🍽️",
    layout="centered"
)


def initialize_session_state():
    if "session_id" not in st.session_state:
        st.session_state.session_id = None
        logger.info("Initialized session_id in session state")
    
    if "conversation_id" not in st.session_state:
        st.session_state.conversation_id = None
        logger.info("Initialized conversation_id in session state")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
        logger.info("Initialized messages in session state")
    
    if "api_status" not in st.session_state:
        st.session_state.api_status = None
    
    if "current_buttons" not in st.session_state:
        st.session_state.current_buttons = []


def check_backend_health():
    logger.debug("Checking backend health")
    return api_client.health_check()


def create_new_session():
    logger.info("Creating new session from UI")
    session_id = api_client.create_session()
    if session_id:
        st.session_state.session_id = session_id
        conversation_data = api_client.create_conversation(session_id)
        if conversation_data:
            st.session_state.conversation_id = conversation_data["conversation_id"]
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": conversation_data["initial_message"]
                }
            ]
            st.session_state.current_buttons = conversation_data.get("buttons", [])
            logger.info(f"New session created with initial greeting: {session_id}")
            return True
    logger.error("Failed to create session/conversation")
    return False


def send_message(user_message: str, action: str = None, widget_data: dict = None):
    if not st.session_state.session_id or not st.session_state.conversation_id:
        logger.warning("Attempted to send message without session/conversation")
        st.error("Please start a new conversation first.")
        return
    
    st.session_state.messages.append({"role": "user", "content": user_message})
    st.session_state.current_buttons = []
    logger.info(f"User message added: {user_message[:50]}...")
    
    with st.spinner("Thinking..."):
        response_data = api_client.send_message(
            st.session_state.session_id,
            st.session_state.conversation_id,
            user_message,
            action=action,
            widget_data=widget_data
        )
    
    if response_data:
        st.session_state.messages.append({
            "role": "assistant",
            "content": response_data["response"]
        })
        st.session_state.current_buttons = response_data.get("buttons", [])
        logger.info(f"Assistant response received")
    else:
        st.error("Failed to get response from the agent.")
        logger.error("Failed to get response from backend")


def main():
    logger.info("Starting Streamlit app")
    initialize_session_state()
    
    st.title("🍽️ Restaurant Chat Agent")
    
    with st.sidebar:
        st.header("Settings")
        
        if st.button("Check Backend Status", use_container_width=True):
            with st.spinner("Checking..."):
                status = check_backend_health()
                st.session_state.api_status = status
        
        if st.session_state.api_status is not None:
            if st.session_state.api_status:
                st.success("✅ Backend is healthy")
            else:
                st.error("❌ Backend is not responding")
        
        st.divider()
        
        if st.button("🆕 New Conversation", use_container_width=True):
            if create_new_session():
                st.success("New conversation started!")
                st.rerun()
            else:
                st.error("Failed to start conversation. Check backend.")
        
        if st.session_state.session_id:
            st.info(f"Session ID: {st.session_state.session_id[:8]}...")
            if st.session_state.conversation_id:
                st.info(f"Conversation ID: {st.session_state.conversation_id[:8]}...")
        
        st.divider()
        st.caption(f"Backend: {settings.backend_api_url}")
    
    if not st.session_state.session_id:
        st.info("👈 Click 'New Conversation' in the sidebar to start chatting!")
        return
    
    for idx, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            if message["role"] == "assistant" and idx == len(st.session_state.messages) - 1:
                if st.session_state.current_buttons:
                    for button in st.session_state.current_buttons:
                        widget_type = button.get("widget_type", "button")
                        widget_config = button.get("widget_config", {})
                        
                        if widget_type == "date":
                            from datetime import date, timedelta
                            min_date = date.today()
                            max_date = date.today() + timedelta(days=widget_config.get("max_days_ahead", 60))
                            
                            selected_date = st.date_input(
                                button["label"],
                                min_value=min_date,
                                max_value=max_date,
                                key=f"date_{idx}"
                            )
                            
                            if st.button("Confirm Date", key=f"confirm_date_{idx}"):
                                widget_data = {
                                    "action": button["action"],
                                    "value": selected_date.strftime("%Y-%m-%d")
                                }
                                send_message(f"Selected date: {selected_date.strftime('%B %d, %Y')}", widget_data=widget_data)
                                st.rerun()
                        
                        elif widget_type == "time":
                            from datetime import time as dt_time
                            
                            selected_time = st.time_input(
                                button["label"],
                                value=dt_time(18, 0),
                                key=f"time_{idx}"
                            )
                            
                            if st.button("Confirm Time", key=f"confirm_time_{idx}"):
                                widget_data = {
                                    "action": button["action"],
                                    "value": selected_time.strftime("%H:%M")
                                }
                                send_message(f"Selected time: {selected_time.strftime('%I:%M %p')}", widget_data=widget_data)
                                st.rerun()
                        
                        elif widget_type == "number":
                            min_val = widget_config.get("min_value", 1)
                            max_val = widget_config.get("max_value", 10)
                            default_val = widget_config.get("default_value", 2)
                            
                            selected_number = st.number_input(
                                button["label"],
                                min_value=min_val,
                                max_value=max_val,
                                value=default_val,
                                step=1,
                                key=f"number_{idx}"
                            )
                            
                            if st.button("Confirm", key=f"confirm_number_{idx}"):
                                widget_data = {
                                    "action": button["action"],
                                    "value": int(selected_number)
                                }
                                send_message(f"{selected_number} guests", widget_data=widget_data)
                                st.rerun()
                        
                        else:
                            if st.button(
                                button["label"],
                                key=f"btn_{button['action']}_{idx}",
                                use_container_width=True
                            ):
                                send_message(button["label"], action=button["action"])
                                st.rerun()
    
    if prompt := st.chat_input("Type your message here..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        
        send_message(prompt)
        st.rerun()


if __name__ == "__main__":
    main()

