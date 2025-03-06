import streamlit as st
import re
import random
import string

# Common passwords to blacklist
COMMON_PASSWORDS = {
    'password123', 'qwerty123', '12345678', 'admin123', 
    'letmein123', 'welcome123', 'monkey123', 'football123'
}

def generate_strong_password(length=12):
    """
    Generate a strong password with specified length
    """
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special = "!@#$%^&*"
    
    # Ensure at least one of each character type
    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
        random.choice(special)
    ]
    
    # Fill the rest with random characters
    remaining_length = length - len(password)
    all_chars = lowercase + uppercase + digits + special
    password.extend(random.choice(all_chars) for _ in range(remaining_length))
    
    # Shuffle the password
    random.shuffle(password)
    return ''.join(password)

def check_password_strength(password):
    """
    Analyze password strength and return score and feedback
    """
    score = 0
    feedback = []
    
    # Check if password is in common password list
    if password.lower() in COMMON_PASSWORDS:
        feedback.append("This is a commonly used password. Please choose something more unique")
        return 0, feedback
    
    # Weighted scoring system
    weights = {
        'length': 2.0,      # Length is most important
        'case': 1.5,        # Case mixing is very important
        'digits': 1.0,      # Digits are important
        'special': 1.5,     # Special characters are very important
        'patterns': 1.0     # Pattern avoidance is important
    }
    
    # Check length (weight: 2.0)
    if len(password) >= 12:
        score += 2 * weights['length']
    elif len(password) >= 8:
        score += 1 * weights['length']
    else:
        feedback.append("Make the password at least 8 characters long (12+ recommended)")
    
    # Check for uppercase and lowercase (weight: 1.5)
    if re.search(r'[A-Z]', password) and re.search(r'[a-z]', password):
        score += 1 * weights['case']
    else:
        feedback.append("Include both uppercase and lowercase letters")
    
    # Check for digits (weight: 1.0)
    if re.search(r'\d', password):
        score += 1 * weights['digits']
    else:
        feedback.append("Add at least one number")
    
    # Check for special characters (weight: 1.5)
    if re.search(r'[!@#$%^&*]', password):
        score += 1 * weights['special']
    else:
        feedback.append("Add at least one special character (!@#$%^&*)")
    
    # Check for common patterns (weight: 1.0)
    if not re.search(r'(.)\1\1', password):  # Check for repeated characters
        score += 1 * weights['patterns']
    else:
        feedback.append("Avoid using repeated characters")
    
    # Normalize score to 0-5 range
    max_possible_score = sum(weights.values())
    normalized_score = (score / max_possible_score) * 5
    
    return min(normalized_score, 5), feedback

def get_strength_label(score):
    """
    Convert numerical score to strength label
    """
    if score <= 2:
        return "Weak", "red"
    elif score <= 4:
        return "Moderate", "orange"
    else:
        return "Strong", "green"

# Page configuration with custom theme
st.set_page_config(
    page_title="Password Strength Meter",
    page_icon="🔒",
    layout="centered"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton > button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 0.5rem;
        border-radius: 5px;
    }
    .stProgress > div > div > div {
        background-color: #4CAF50;
    }
    h1 {
        color: #1E3D59;
        text-align: center;
        padding-bottom: 1rem;
    }
    .password-container {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Main UI
st.title("🔒 Password Strength Meter")
st.markdown("""
    <div style='text-align: center; color: #666; margin-bottom: 2rem;'>
        Create and verify strong passwords to enhance your security
    </div>
""", unsafe_allow_html=True)

# Container for main password input and generation
with st.container():
    st.markdown("<div class='password-container'>", unsafe_allow_html=True)
    
    # Two columns for password input and generation
    col1, col2 = st.columns([2, 1])

    with col1:
        password = st.text_input(
            "Enter your password:",
            type="password",
            help="Type or paste your password here"
        )

    with col2:
        st.markdown("<div style='padding-top: 1.5rem;'>", unsafe_allow_html=True)
        if st.button("🎲 Generate Password"):
            generated_password = generate_strong_password()
            st.code(generated_password, language=None)
            st.info("🔄 Click to copy")
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Results section
if password:
    score, feedback = check_password_strength(password)
    strength, color = get_strength_label(score)
    
    # Create three columns for strength indicators
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(f"""
            <div style='text-align: center; margin: 1rem 0;'>
                <h3 style='color: {color}; margin-bottom: 0;'>{strength}</h3>
                <p style='color: #666; font-size: 0.9rem;'>Password Strength</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Progress bar with custom styling
    progress_percentage = (score / 5) * 100
    st.progress(progress_percentage / 100)
    st.markdown(f"""
        <div style='text-align: center; color: #666;'>
            Score: {int(score)}/5
        </div>
    """, unsafe_allow_html=True)
    
    # Feedback section with better organization
    if feedback:
        st.markdown("""
            <div style='margin-top: 2rem;'>
                <h4 style='color: #1E3D59;'>📝 Improvement Suggestions</h4>
            </div>
        """, unsafe_allow_html=True)
        for suggestion in feedback:
            st.warning(suggestion)
    elif strength == "Strong":
        st.success("✅ Excellent! Your password meets all security criteria.")
    
    # Criteria section with better styling
    with st.expander("📋 Password Strength Criteria"):
        st.markdown("""
            <div style='background-color: #f8f9fa; padding: 1rem; border-radius: 5px;'>
                <h4 style='color: #1E3D59;'>Strong Password Requirements:</h4>
                <ul style='color: #666;'>
                    <li>Minimum 8 characters (12+ recommended)</li>
                    <li>Mix of uppercase & lowercase letters</li>
                    <li>At least one number (0-9)</li>
                    <li>At least one special character (!@#$%^&*)</li>
                    <li>No repeated characters</li>
                    <li>Not a commonly used password</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div style='background-color: #f8f9fa; padding: 1rem; border-radius: 5px; margin-top: 1rem;'>
                <h4 style='color: #1E3D59;'>Scoring Weights:</h4>
                <ul style='color: #666;'>
                    <li>Length: 2.0x</li>
                    <li>Case mixing: 1.5x</li>
                    <li>Special characters: 1.5x</li>
                    <li>Digits: 1.0x</li>
                    <li>Pattern avoidance: 1.0x</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("""
    <div style='text-align: center; color: #666; padding-top: 2rem; font-size: 0.8rem;'>
        🔐 Keep your accounts secure with strong passwords
    </div>
""", unsafe_allow_html=True)