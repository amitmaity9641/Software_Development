import streamlit as st
import numpy as np

def is_valid(board, row, col, num):
    # Check row
    if num in board[row]:
        return False
    
    # Check column
    if num in [board[i][col] for i in range(9)]:
        return False
    
    # Check 3x3 box
    box_row, box_col = row // 3 * 3, col // 3 * 3
    if num in [board[box_row + i][box_col + j] for i in range(3) for j in range(3)]:
        return False
    
    return True

def solve_sudoku(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def main():
    st.title("🧩 Sudoku Solver")
    st.write("Enter your Sudoku puzzle below (use 0 for empty cells) and click 'Solve'")
    
    # Initialize board
    if 'board' not in st.session_state:
        st.session_state.board = [[0 for _ in range(9)] for _ in range(9)]
    
    # Create input grid
    with st.form("sudoku_grid"):
        cols = st.columns(9)
        for row in range(9):
            for col in range(9):
                with cols[col]:
                    st.session_state.board[row][col] = st.number_input(
                        f"R{row+1}C{col+1}", 
                        min_value=0, 
                        max_value=9, 
                        value=st.session_state.board[row][col],
                        key=f"cell_{row}_{col}",
                        step=1
                    )
        
        solve_btn = st.form_submit_button("Solve Puzzle")
        reset_btn = st.form_submit_button("Reset Board")
    
    if solve_btn:
        # Convert to numpy array for easier manipulation
        board_copy = np.array(st.session_state.board)
        
        if solve_sudoku(board_copy):
            st.success("✅ Puzzle solved successfully!")
            st.session_state.board = board_copy.tolist()
            st.rerun()
        else:
            st.error("❌ No solution exists for this puzzle configuration")
    
    if reset_btn:
        st.session_state.board = [[0 for _ in range(9)] for _ in range(9)]
        st.rerun()
    
    # Display the current board in a nice grid format
    st.subheader("Current Sudoku Board:")
    st.markdown("<style>table {border-collapse: collapse;} td {border: 1px solid black; width: 40px; height: 40px; text-align: center;}</style>", unsafe_allow_html=True)
    
    html_table = "<table>"
    for row in range(9):
        html_table += "<tr>"
        for col in range(9):
            value = st.session_state.board[row][col] if st.session_state.board[row][col] != 0 else ""
            # Add thicker borders for 3x3 boxes
            border_class = ""
            if row % 3 == 0 and row != 0:
                border_class += " border-top-3"
            if col % 3 == 0 and col != 0:
                border_class += " border-left-3"
            html_table += f"<td class='{border_class}'>{value}</td>"
        html_table += "</tr>"
    html_table += "</table>"
    
    st.markdown(html_table, unsafe_allow_html=True)

if __name__ == "__main__":
    main()