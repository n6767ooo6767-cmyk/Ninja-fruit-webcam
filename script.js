body { margin: 0; background: #0e1621; color: #fff; font-family: 'Arial', sans-serif; text-align: center; }
h1 { padding-top: 20px; text-shadow: 0 0 10px #fff; }

#game-list { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 20px; padding: 40px; }

.neon-btn {
    padding: 20px; cursor: pointer; background: transparent; border: 2px solid #00f3ff;
    color: #00f3ff; font-weight: bold; text-transform: uppercase;
    box-shadow: 0 0 10px #00f3ff, inset 0 0 10px #00f3ff;
    transition: 0.3s; animation: pulse 2s infinite;
}

.neon-btn:hover { background: #00f3ff; color: #000; box-shadow: 0 0 30px #00f3ff; }

@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.7; } }

#game-container { position: relative; }
canvas { display: block; width: 100vw; height: 90vh; background: #000; }
#backBtn { position: absolute; top: 10px; left: 10px; z-index: 10; padding: 10px; cursor: pointer; }
