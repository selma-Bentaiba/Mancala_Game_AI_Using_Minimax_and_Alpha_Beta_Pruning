# **🌰 Mancala Solver - Adversarial Search**  
### **Master 1 - Visual Computing, USTHB (2024/2025)**  

**📚 Course:** Problem Solving - TP by *Dr. Meriem Sebai*  


<br>  

📄 **[Assignment Support (PDF)](./📄Mancala_game_project.pdf)**  
<br>  

![Mancala Board Example](https://i.pinimg.com/originals/e7/23/07/e72307019ac8c6bf2501877bfb28bafc.gif)  
<br>  

---

## **📌 About**  

**Mancala** is an ancient strategy game where players capture the most seeds 🌱. 
This project implements a smart AI opponent using **Minimax algorithm with Alpha-Beta pruning** to outplay you 🤯.

![explain the game](https://i.pinimg.com/736x/07/f5/66/07f56656594d41042b81aba3d432e15c.jpg)
---

## **🧩 Features**  
<br>
- ✅ **Minimax Algorithm**: Implements adversarial search to determine the best moves.  
- ✅ **Alpha-Beta Pruning**: Optimizes the search by reducing unnecessary computations.  
- ✅ **Two Game Modes**:  
  - **AI vs AI**: Watch two AI opponents compete.  
  - **Human vs AI**: Play against the AI.  
- ✅ **Interactive Gameplay**: Provides a clear interface for both modes.  

---

## **🕹️ How It Works**  
### **1. Mancala Board Representation**  
The game is modeled using a `MancalaBoard` class:  
- **Board Representation**: A dictionary maps each pit and store to its seed count.  
- **Player Pits**: Player 1 controls pits A-F, and Player 2 controls pits G-L.  
- **Stores**: Each player has a store to collect captured seeds.  

### **2. Minimax with Alpha-Beta Pruning**  
The AI uses the Minimax algorithm to evaluate possible moves:  
- **Maximizing Player**: The AI aims to maximize its score.  
- **Minimizing Player**: The opponent (AI or human) aims to minimize the AI's score.  
- **Alpha-Beta Pruning**: Reduces the search space by eliminating suboptimal branches.  

---

## **📦 Installation**  
1️⃣ Clone the repository:  
```bash  
git clone https://github.com/selma-Bentaiba/Mancala_Game_AI_Using_Minimax_and_Alpha_Beta_Pruning.git  
```  

2️⃣ Install dependencies:  
```bash  
pip install pygame  
```  

3️⃣ Run the game:  
- For **AI vs AI**:  
  ```bash  
  python aiVSai/main.py  
  ```  
- For **Human vs AI**:  
  ```bash  
  python aiVsHuman/main.py  
  ```  

---
🌟 Fun Fact!
Mancala dates back thousands of years and is one of the oldest known board games! 🎲


## **🤖 Future Improvements**  
- 🔹 **Enhanced Heuristics**: Improve the evaluation function for smarter AI decisions.  
- 🔹 **GUI**: Add a graphical interface using Pygame for better user experience.  
- 🔹 **Performance Optimization**: Optimize the Minimax algorithm for faster decision-making.  

---
