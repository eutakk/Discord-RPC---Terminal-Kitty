#!/usr/bin/env python3
"""
Discord RPC Simples para Kitty
Versão minimalista - apenas mostra que você está usando o terminal
"""

from pypresence import Presence
import time

CLIENT_ID = "YOUR_CLIENT_ID_HERE"

def main():
    rpc = Presence(CLIENT_ID)
    
    try:
        rpc.connect()
        print("✓ Conectado ao Discord!")
        
        rpc.update(
            details="No terminal Kitty",
            state="Arch Linux",
            large_image="terminal",
            large_text="Terminal Kitty no Arch",
            start=time.time()
        )
        
        print("🚀 RPC ativo! Pressione Ctrl+C para parar")
        
        while True:
            time.sleep(15)
            
    except KeyboardInterrupt:
        print("\n👋 Encerrando...")
        rpc.close()

if __name__ == "__main__":
    if CLIENT_ID == "YOUR_CLIENT_ID_HERE":
        print("⚠️  Configure seu Discord Application ID primeiro!")
        exit(1)
    main()
