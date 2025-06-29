import streamlit as st
import random

def reset_game():
    st.session_state.target_number = random.randint(1, 100)
    st.session_state.guesses = []
    st.session_state.game_over = False

def check_guess(guess):
    if guess == st.session_state.target_number:
        st.session_state.game_over = True
        return "correct"
    elif guess < st.session_state.target_number:
        return "too low"
    else:
        return "too high"

def main():
    st.title("🎯 Number Guessing Game")
    st.write("Try to guess the secret number between 1 and 100!")

    # Initialize game state
    if 'target_number' not in st.session_state:
        reset_game()

    # Game controls
    col1, col2 = st.columns([3, 1])
    with col1:
        guess = st.number_input("Enter your guess:", 
                               min_value=1, 
                               max_value=100, 
                               step=1,
                               key="guess_input")
    with col2:
        st.write("")  # For alignment
        submit_guess = st.button("Submit Guess")

    # Handle guess submission
    if submit_guess and not st.session_state.game_over:
        st.session_state.guesses.append(guess)
        result = check_guess(guess)
        
        if result == "correct":
            st.balloons()
            st.success(f"🎉 Congratulations! You guessed it in {len(st.session_state.guesses)} attempts!")
        elif result == "too low":
            st.warning("⬆️ Too low! Try a higher number.")
        else:
            st.warning("⬇️ Too high! Try a lower number.")

    # Display game history
    if st.session_state.guesses:
        st.write("")
        st.subheader("Your Guesses:")
        for i, g in enumerate(st.session_state.guesses, 1):
            st.write(f"Attempt {i}: {g}")

    # Reset button
    if st.session_state.game_over or st.button("Reset Game"):
        reset_game()
        st.rerun()

if __name__ == "__main__":
    main()