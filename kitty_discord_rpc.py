#!/usr/bin/env python3
"""
Discord RPC para Terminal Kitty
Mostra o comando atual e informações do terminal no Discord
"""

import psutil
import time
import os
from pypresence import Presence

# Seu Discord Application ID (você precisa criar um app em https://discord.com/developers/applications)
CLIENT_ID = "YOUR_CLIENT_ID_HERE"

class KittyRPC:
    def __init__(self, client_id):
        self.client_id = client_id
        self.rpc = Presence(client_id)
        self.last_process = None
        self.start_time = time.time()
        
    def connect(self):
        try:
            self.rpc.connect()
            print("✓ Conectado ao Discord!")
            return True
        except Exception as e:
            print(f"✗ Erro ao conectar: {e}")
            return False
    
    def get_kitty_processes(self):
        """Encontra processos rodando em terminais Kitty"""
        kitty_children = []
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                # Procura por processos kitty
                if proc.info['name'] == 'kitty':
                    # Pega processos filhos (comandos rodando no terminal)
                    children = proc.children(recursive=True)
                    for child in children:
                        try:
                            cmdline = child.cmdline()
                            if cmdline and len(cmdline) > 0:
                                # Ignora processos shell básicos
                                if child.name() not in ['bash', 'zsh', 'fish', 'sh']:
                                    kitty_children.append({
                                        'name': child.name(),
                                        'cmdline': ' '.join(cmdline),
                                        'pid': child.pid
                                    })
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            continue
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        return kitty_children
    
    def get_current_shell(self):
        """Pega o shell atual do usuário"""
        shell = os.environ.get('SHELL', 'shell')
        return os.path.basename(shell)
    
    def update_presence(self):
        """Atualiza o Discord Rich Presence"""
        processes = self.get_kitty_processes()
        
        if processes:
            # Mostra o processo mais recente/ativo
            process = processes[0]
            details = f"Rodando: {process['name']}"
            state = f"Terminal: Kitty"
            
            # Limita o tamanho da linha de comando
            cmd_preview = process['cmdline'][:100]
            if len(process['cmdline']) > 100:
                cmd_preview += "..."
            
            large_text = cmd_preview
        else:
            # Sem processos ativos, mostra só o terminal
            shell = self.get_current_shell()
            details = f"Terminal: Kitty"
            state = f"Shell: {shell}"
            large_text = "Esperando comandos..."
        
        try:
            self.rpc.update(
                details=details,
                state=state,
                large_image="terminal",  # Você pode customizar isso
                large_text=large_text,
                start=self.start_time
            )
            
            # Debug info
            if processes:
                print(f"🔄 Atualizando RPC: {process['name']}")
            
        except Exception as e:
            print(f"✗ Erro ao atualizar presence: {e}")
    
    def run(self):
        """Loop principal"""
        if not self.connect():
            return
        
        print("🚀 Monitorando terminal Kitty...")
        print("💡 Pressione Ctrl+C para parar\n")
        
        try:
            while True:
                self.update_presence()
                time.sleep(5)  # Atualiza a cada 5 segundos
        except KeyboardInterrupt:
            print("\n👋 Parando Discord RPC...")
            self.rpc.close()

if __name__ == "__main__":
    # Verifica se o CLIENT_ID foi configurado
    if CLIENT_ID == "YOUR_CLIENT_ID_HERE":
        print("⚠️  ATENÇÃO: Você precisa configurar seu Discord Application ID!")
        print("\n📝 Passos:")
        print("1. Vá em https://discord.com/developers/applications")
        print("2. Crie uma nova aplicação (ou use uma existente)")
        print("3. Copie o 'Application ID'")
        print("4. Edite este script e substitua 'YOUR_CLIENT_ID_HERE' pelo ID")
        print("\n💡 Opcional: Adicione uma imagem chamada 'terminal' nos Rich Presence Assets")
        exit(1)
    
    rpc_client = KittyRPC(CLIENT_ID)
    rpc_client.run()
